// All API calls to your FastAPI backend running at http://localhost:8000
const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

// ─── Types ────────────────────────────────────────────────────────────────────
// These match exactly what your FastAPI DocumentResponse schema returns
export interface Document {
  id: string;
  title: string;
  fileType: string;   // your backend uses camelCase
  status: string;
  createdAt: string;  // your backend uses camelCase
}

// This matches your FastAPI SummaryResponse schema
export interface SummaryResponse {
  documentId: string;
  title: string;
  summary: string;
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

// Upload uses multipart/form-data — cannot use apiFetch (no JSON header)
export async function uploadDocument(
  title: string,
  file: File,
  fileType: string
): Promise<{ id: string; message: string }> {
  const formData = new FormData();
  formData.append("title", title);
  formData.append("file", file);
  formData.append("fileType", fileType); // your backend expects "fileType" (camelCase)

  const res = await fetch(`${BASE_URL}/api/documents`, {
    method: "POST",
    body: formData,
    // Do NOT set Content-Type — browser sets it automatically with the boundary
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

// Download the actual file
export async function downloadDocumentFile(id: string): Promise<void> {
  const res = await fetch(`${BASE_URL}/api/documents/${id}/file`);
  if (!res.ok) throw new Error("Download failed");

  const disposition = res.headers.get("Content-Disposition");
  let filename = "document";
  if (disposition) {
    const match = disposition.match(/filename="?(.+?)"?$/);
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

// Your backend expects: { "summaryType": "concise" } (camelCase)
export async function summarizeDocument(
  id: string,
  summaryType: SummaryType
): Promise<{ message: string; documentId: string }> {
  return apiFetch(`/api/documents/${id}/summarize`, {
    method: "POST",
    body: JSON.stringify({ summaryType }), // camelCase — matches your SummaryRequest schema
  });
}

export async function fetchSummary(id: string): Promise<SummaryResponse | null> {
  try {
    return await apiFetch<SummaryResponse>(`/api/documents/${id}/summary`);
  } catch {
    return null;
  }
}

// Regenerate calls PATCH /api/documents/{id}/summary
export async function regenerateSummary(
  id: string,
  summaryType: SummaryType
): Promise<void> {
  await apiFetch(`/api/documents/${id}/summary`, {
    method: "PATCH",
    body: JSON.stringify({ summaryType }), // camelCase
  });
}