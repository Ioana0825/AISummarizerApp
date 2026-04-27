// All API calls to your FastAPI backend running at http://localhost:8000
const BASE_URL = "http://localhost:8000";

// ─── Types ────────────────────────────────────────────────────────────────────

export interface Document {
  id: string;
  title: string;
  fileType: string;
  status: string;
  createdAt: string;
}

export interface SummaryResponse {
  documentId: string;
  title: string;
  summary: string;
  summaryType: string;
  generatedAt: string;
}

export type SummaryType = "concise" | "detailed";

// ─── Helper ───────────────────────────────────────────────────────────────────

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!res.ok) {
    const errorBody = await res.text();
    throw new Error(errorBody || `Request failed: ${res.status}`);
  }
  return res.json();
}

// ─── Documents ────────────────────────────────────────────────────────────────

export async function fetchDocuments(): Promise<Document[]> {
  return apiFetch<Document[]>("/api/documents");
}

export async function fetchDocumentById(id: string): Promise<Document> {
  return apiFetch<Document>(`/api/documents/${id}`);
}

export async function uploadDocument(
  title: string,
  file: File,
  fileType: string
): Promise<{ id: string; message: string }> {
  const formData = new FormData();
  formData.append("title", title);
  formData.append("file", file);
  formData.append("fileType", fileType);

  const res = await fetch(`${BASE_URL}/api/documents`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    const errorBody = await res.text();
    throw new Error(errorBody || `Upload failed: ${res.status}`);
  }
  return res.json();
}

export async function deleteDocument(id: string): Promise<void> {
  await apiFetch(`/api/documents/${id}`, { method: "DELETE" });
}

export async function downloadDocumentFile(id: string): Promise<void> {
  const res = await fetch(`${BASE_URL}/api/documents/${id}/file`);
  if (!res.ok) throw new Error("Download failed");

  const disposition = res.headers.get("Content-Disposition");
  let filename = "document";
  if (disposition) {
    const match = disposition.match(/filename="?(.+?)\"?$/);
    if (match) filename = match[1];
  }

  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

// ─── Summaries ────────────────────────────────────────────────────────────────

export async function summarizeDocument(
  id: string,
  summaryType: SummaryType
): Promise<{ message: string; documentId: string; estimatedSeconds?: number }> {
  return apiFetch(`/api/documents/${id}/summarize`, {
    method: "POST",
    body: JSON.stringify({ summaryType }),
  });
}

/**
 * Fetch the summary for a specific type (concise or detailed).
 * Returns null if that type hasn't been generated yet.
 */
export async function fetchSummary(
  id: string,
  summaryType: SummaryType
): Promise<SummaryResponse | null> {
  try {
    return await apiFetch<SummaryResponse>(
      `/api/documents/${id}/summary?type=${summaryType}`
    );
  } catch {
    return null;
  }
}

export async function regenerateSummary(
  id: string,
  summaryType: SummaryType
): Promise<{ message: string; documentId: string; estimatedSeconds?: number }> {
  return apiFetch(`/api/documents/${id}/summary`, {
    method: "PATCH",
    body: JSON.stringify({ summaryType }),
  });
}

// ─── Streaming summarization ──────────────────────────────────────────────────

/**
 * Starts a streaming summarization request.
 * Calls onToken for each text chunk as it arrives.
 * Calls onDone when the full summary has been received and saved.
 * Calls onError if something goes wrong.
 * Returns a cancel() function you can call to abort mid-stream.
 */
export function streamSummary(
  id: string,
  summaryType: SummaryType,
  onToken: (token: string) => void,
  onDone: () => void,
  onError: (e: Error) => void
): () => void {
  const controller = new AbortController();

  (async () => {
    try {
      const res = await fetch(`${BASE_URL}/api/documents/${id}/summarize-stream`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ summaryType }),
        signal: controller.signal,
      });

      if (!res.ok) {
        throw new Error(`Request failed: ${res.status}`);
      }

      const reader = res.body!.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop()!;

        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;
          const raw = line.slice(6).trim();
          if (!raw) continue;

          try {
            const parsed = JSON.parse(raw);
            if (parsed.token) onToken(parsed.token);
            if (parsed.done) onDone();
          } catch {
            // skip malformed chunks
          }
        }
      }
    } catch (e: unknown) {
      if (e instanceof Error && e.name === "AbortError") return;
      onError(e instanceof Error ? e : new Error("Unknown error"));
    }
  })();

  return () => controller.abort();
}