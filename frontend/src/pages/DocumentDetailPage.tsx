import { useState, useEffect, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { ChevronLeft, Eye, EyeOff, Trash2, Copy, Download } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { toast } from "sonner";
import { format } from "date-fns";
import AppHeader from "@/components/AppHeader";
import {
  fetchDocumentById,
  fetchSummary,
  deleteDocument,
  downloadDocumentFile,
  streamSummary,
} from "@/lib/api";
import type { SummaryType } from "@/lib/api";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function splitWarningAndSummary(text: string): { warning: string | null; summary: string } {
  const match = text.match(/^(⚠️[^\n]+\n\n?)([\s\S]*)$/);
  if (match) return { warning: match[1].trim(), summary: match[2] };
  return { warning: null, summary: text };
}

function hasRealContent(text: string): boolean {
  const { summary } = splitWarningAndSummary(text);
  return summary.trim().length > 0;
}

// Skeleton that mirrors the info bar layout
function InfoBarSkeleton() {
  return (
    <div className="rounded-xl surface-highlight px-6 py-3 flex flex-wrap items-center gap-3 animate-pulse">
      <div className="h-4 w-32 bg-muted rounded" />
      <div className="h-4 w-10 bg-muted rounded" />
      <div className="h-4 w-24 bg-muted rounded" />
      <div className="h-6 w-16 bg-muted rounded-full ml-auto" />
    </div>
  );
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

const DocumentDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const [summaryType, setSummaryType] = useState<SummaryType>("concise");
  const [showSummary, setShowSummary] = useState(true);
  const [summarizing, setSummarizing] = useState(false);
  const [streamedSummary, setStreamedSummary] = useState("");

  const cancelStreamRef = useRef<(() => void) | null>(null);
  const [secondsLeft, setSecondsLeft] = useState<number | null>(null);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
      if (cancelStreamRef.current) cancelStreamRef.current();
    };
  }, []);

  const startTimer = (totalSeconds: number) => {
    if (timerRef.current) clearInterval(timerRef.current);
    setSecondsLeft(totalSeconds);
    timerRef.current = setInterval(() => {
      setSecondsLeft((prev) => {
        if (prev === null || prev <= 1) return 0;
        return prev - 1;
      });
    }, 1000);
  };

  const stopTimer = () => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
    setSecondsLeft(null);
  };

  const formatTime = (s: number) => {
    const mins = Math.floor(s / 60);
    const secs = s % 60;
    if (mins > 0) return `~${mins}m ${secs.toString().padStart(2, "0")}s remaining`;
    return `~${secs}s remaining`;
  };

  // ---------------------------------------------------------------------------
  // Data fetching
  // ---------------------------------------------------------------------------

  const { data: doc, isLoading: docLoading } = useQuery({
    queryKey: ["document", id],
    queryFn: () => fetchDocumentById(id!),
    enabled: !!id,
  });

  const {
    data: summary,
    isLoading: summaryLoading,
    refetch: refetchSummary,
  } = useQuery({
    queryKey: ["summary", id, summaryType],
    queryFn: () => fetchSummary(id!, summaryType),
    enabled: !!id && !summarizing,
    retry: false,
  });

  // Update page title whenever the document loads
  useEffect(() => {
    if (doc?.title) {
      document.title = `${doc.title} — Powerr`;
    }
    return () => {
      document.title = "Powerr - AI Study Summarizer";
    };
  }, [doc?.title]);

  useEffect(() => {
    if (!summarizing) {
      setStreamedSummary("");
    }
  }, [summaryType]);

  // ---------------------------------------------------------------------------
  // Streaming helper
  // ---------------------------------------------------------------------------

  const startStream = (onSuccess: () => void, onFailure: (e: Error) => void) => {
    setStreamedSummary("");
    setSummarizing(true);
    setShowSummary(true);

    const roughEstimate = summaryType === "concise" ? 30 : 60;
    startTimer(roughEstimate);

    cancelStreamRef.current = streamSummary(
      id!,
      summaryType,
      (token) => {
        setStreamedSummary((prev) => {
          const next = prev + token;
          if (hasRealContent(next)) stopTimer();
          return next;
        });
      },
      () => {
        setSummarizing(false);
        queryClient.invalidateQueries({ queryKey: ["document", id] });
        queryClient.invalidateQueries({ queryKey: ["summary", id, summaryType] });
        refetchSummary();
        onSuccess();
      },
      (e) => {
        stopTimer();
        setSummarizing(false);
        onFailure(e);
      }
    );
  };

  // ── Mutations ──────────────────────────────────────────────────────────────

  const summarizeMut = useMutation({
    mutationFn: () =>
      new Promise<void>((resolve, reject) => {
        startStream(
          () => { toast.success("Summary generated!"); resolve(); },
          (e) => { toast.error("Summarization failed"); reject(e); }
        );
      }),
  });

  const regenMut = useMutation({
    mutationFn: () =>
      new Promise<void>((resolve, reject) => {
        startStream(
          () => { toast.success("Summary regenerated!"); resolve(); },
          (e) => { toast.error("Regeneration failed"); reject(e); }
        );
      }),
  });

  const deleteMut = useMutation({
    mutationFn: () => deleteDocument(id!),
    onSuccess: () => {
      toast.success("Document deleted");
      navigate("/documents");
    },
  });

  // ---------------------------------------------------------------------------
  // Copy / export
  // ---------------------------------------------------------------------------

  const getRawText = () => {
    if (summarizing) return streamedSummary;
    return summary?.summary ?? "";
  };

  const copySummary = () => {
    const text = getRawText();
    if (text) {
      navigator.clipboard.writeText(text);
      toast.success("Copied to clipboard");
    }
  };

  const exportSummary = () => {
    const text = getRawText();
    const title = summary?.title || "summary";
    if (!text) return;
    const blob = new Blob([text], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${title}_${summaryType}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // ---------------------------------------------------------------------------
  // Loading / not found states
  // ---------------------------------------------------------------------------

  if (docLoading) {
    return (
      <div className="min-h-screen bg-background flex flex-col">
        <AppHeader />
        <main className="flex-1 px-4 md:px-8 py-6 max-w-5xl mx-auto w-full space-y-6">
          <div className="h-8 w-24 bg-muted rounded animate-pulse" />
          <InfoBarSkeleton />
          <div className="rounded-xl border border-border bg-card p-6 space-y-4 animate-pulse">
            {[80, 60, 90, 50, 75].map((w, i) => (
              <div key={i} className="h-4 bg-muted rounded" style={{ width: `${w}%` }} />
            ))}
          </div>
        </main>
      </div>
    );
  }

  if (!doc) {
    return (
      <div className="min-h-screen bg-background flex flex-col">
        <AppHeader />
        <div className="flex-1 flex items-center justify-center text-muted-foreground">
          Document not found
        </div>
      </div>
    );
  }

  // ---------------------------------------------------------------------------
  // Derived values
  // ---------------------------------------------------------------------------

  const formatDate = (d: string) => {
    try {
      const date = new Date(d.endsWith("Z") ? d : d + "Z");
      return format(date, "dd.MM.yyyy HH:mm");
    } catch { return d; }
  };

  const isSummarized = doc.status === "summarized" || showSummary;
  const { warning: streamedWarning, summary: streamedContent } = splitWarningAndSummary(streamedSummary);
  const showSpinner = summarizing && !hasRealContent(streamedSummary);
  const showStreamingContent = summarizing && streamedSummary.length > 0;

  const thisTypeExists = !summarizing && summary !== null;
  const thisTypeNotGenerated = !summarizing && !summaryLoading && summary === null;

  const hasText = !!getRawText();

  // ---------------------------------------------------------------------------
  // Render
  // ---------------------------------------------------------------------------

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <AppHeader />
      <main className="flex-1 px-4 md:px-8 py-6 max-w-5xl mx-auto w-full space-y-6">
        <Button variant="ghost" onClick={() => navigate("/documents")} className="gap-1">
          <ChevronLeft className="w-4 h-4" /> Back
        </Button>

        {/* Document info bar */}
        <div className="rounded-xl surface-highlight px-6 py-3 flex flex-wrap items-center gap-3">
          <span className="font-semibold text-primary">{doc.title}</span>
          <span className="uppercase text-xs font-semibold text-muted-foreground">{doc.fileType}</span>
          <span className="text-sm text-muted-foreground">{formatDate(doc.createdAt)}</span>
          <Badge variant={isSummarized ? "default" : "secondary"}>
            {summarizing ? "Summarizing..." : isSummarized ? "Summarized" : "Pending"}
          </Badge>

          <div className="flex gap-2 ml-auto items-center flex-wrap">
            <Select value={summaryType} onValueChange={(v) => setSummaryType(v as SummaryType)}>
              <SelectTrigger className="w-30 h-8 text-sm">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="concise">Concise</SelectItem>
                <SelectItem value="detailed">Detailed</SelectItem>
              </SelectContent>
            </Select>

            <Button
              size="sm"
              className="h-8 text-sm px-3"
              variant="secondary"
              onClick={() => summarizeMut.mutate()}
              disabled={summarizing || summarizeMut.isPending}
            >
              {summarizing ? "Generating..." : thisTypeExists ? "Regenerate" : "Summarize"}
            </Button>

            <Tooltip>
              <TooltipTrigger asChild>
                <span>
                  <Button
                    size="icon" className="h-8 w-8" variant="outline"
                    onClick={() => setShowSummary((v) => !v)}
                  >
                    {showSummary ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </Button>
                </span>
              </TooltipTrigger>
              <TooltipContent>{showSummary ? "Hide summary" : "Show summary"}</TooltipContent>
            </Tooltip>

            <Tooltip>
              <TooltipTrigger asChild>
                <span>
                  <Button
                    size="icon" className="h-8 w-8" variant="outline"
                    onClick={() => downloadDocumentFile(doc.id).catch(() => toast.error("Download failed"))}
                  >
                    <Download className="w-4 h-4" />
                  </Button>
                </span>
              </TooltipTrigger>
              <TooltipContent>Download original file</TooltipContent>
            </Tooltip>

            <Tooltip>
              <TooltipTrigger asChild>
                <span>
                  <Button
                    size="icon"
                    className="h-8 w-8 text-destructive border-destructive/30 hover:bg-destructive/10"
                    variant="outline"
                    onClick={() => deleteMut.mutate()}
                    disabled={deleteMut.isPending}
                  >
                    <Trash2 className="w-4 h-4" />
                  </Button>
                </span>
              </TooltipTrigger>
              <TooltipContent>Delete document</TooltipContent>
            </Tooltip>
          </div>
        </div>

        {/* Spinner */}
        {showSpinner && (
          <div className="space-y-3">
            <div className="h-2 w-full rounded-full bg-secondary overflow-hidden">
              <div className="h-full bg-primary rounded-full" style={{ animation: "indeterminate 1.5s ease-in-out infinite" }} />
            </div>
            <div className="text-center space-y-1">
              <p className="text-sm font-medium text-foreground">
                {secondsLeft !== null && secondsLeft > 0 ? "Generating your summary..." : "Almost done..."}
              </p>
              {secondsLeft !== null && secondsLeft > 0 && (
                <p className="text-xs text-muted-foreground">{formatTime(secondsLeft)}</p>
              )}
              <p className="text-xs text-muted-foreground">Brewing your study notes... this takes a moment</p>
            </div>
          </div>
        )}

        {/* Summary section */}
        {showSummary && (
          <div className="space-y-4">

            {/* Type indicator + action buttons */}
            <div className="flex flex-wrap items-center gap-2">
              {!summarizing && thisTypeExists && (
                <span className="text-xs font-medium px-2 py-1 rounded-full bg-primary/10 text-primary capitalize">
                  {summaryType} summary
                </span>
              )}
              <div className="flex gap-2 ml-auto">
                <Tooltip>
                  <TooltipTrigger asChild>
                    <span>
                      <Button
                        size="sm" className="h-8 text-sm px-3" variant="outline"
                        onClick={exportSummary}
                        disabled={!hasText}
                      >
                        <Download className="w-3.5 h-3.5 mr-1" /> Export
                      </Button>
                    </span>
                  </TooltipTrigger>
                  {!hasText && (
                    <TooltipContent>Generate a summary first</TooltipContent>
                  )}
                </Tooltip>

                <Tooltip>
                  <TooltipTrigger asChild>
                    <span>
                      <Button
                        size="sm" className="h-8 text-sm px-3" variant="outline"
                        onClick={copySummary}
                        disabled={!hasText}
                      >
                        <Copy className="w-3.5 h-3.5 mr-1" /> Copy
                      </Button>
                    </span>
                  </TooltipTrigger>
                  {!hasText && (
                    <TooltipContent>Generate a summary first</TooltipContent>
                  )}
                </Tooltip>
              </div>
            </div>

            {/* Warning banner — uses design tokens instead of hardcoded amber */}
            {streamedWarning && (
              <div className="flex items-start gap-2 rounded-lg border border-yellow-200 bg-yellow-50 px-4 py-3 text-sm text-yellow-800">
                <span>⚠️</span>
                <span>{streamedWarning.replace(/^⚠️\s*/, "")}</span>
              </div>
            )}

            {/* Summary scroll area — height fills available viewport */}
            <ScrollArea className="rounded-xl border border-border bg-card p-6 h-[calc(100vh-340px)] min-h-[300px]">
              {showStreamingContent ? (
                <p className="text-foreground whitespace-pre-wrap leading-relaxed">
                  {streamedContent}
                  <span
                    className="inline-block w-[2px] h-[1em] bg-primary ml-0.5 align-middle"
                    style={{ animation: "blink 0.7s step-end infinite" }}
                  />
                </p>
              ) : summaryLoading ? (
                <p className="text-muted-foreground">Loading summary...</p>
              ) : thisTypeNotGenerated ? (
                <div className="flex flex-col items-center justify-center h-full gap-3 text-center">
                  <p className="text-muted-foreground">
                    No <span className="font-medium capitalize">{summaryType}</span> summary yet.
                  </p>
                  <Button
                    size="sm"
                    variant="secondary"
                    onClick={() => summarizeMut.mutate()}
                    disabled={summarizing}
                  >
                    Generate {summaryType} summary
                  </Button>
                </div>
              ) : summary ? (
                <div>
                  <h2 className="text-xl font-bold text-primary mb-4">{summary.title}</h2>
                  <p className="text-foreground whitespace-pre-wrap leading-relaxed">
                    {summary.summary}
                  </p>
                </div>
              ) : (
                <p className="text-muted-foreground">No summary available yet. Generate one above.</p>
              )}
            </ScrollArea>
          </div>
        )}
      </main>

      <style>{`
        @keyframes blink { 50% { opacity: 0; } }
      `}</style>
    </div>
  );
};

export default DocumentDetailPage;