import { useState, useCallback, useRef } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { format } from "date-fns";
import { DropdownMenu } from "radix-ui";
import {
  Upload, Trash2, Eye, FileText, Download,
  CloudUpload, X, AlertTriangle, MoreVertical, Sparkles,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import {
  AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent,
  AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { toast } from "sonner";
import AppHeader from "@/components/AppHeader";
import { fetchDocuments, deleteDocument, downloadDocumentFile, summarizeDocument, uploadDocument } from "@/lib/api";
import type { Document } from "@/lib/api";

const ALLOWED = ["pdf", "docx", "txt"];

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function formatFileSize(bytes: number | null | undefined): string {
  if (!bytes) return "—";
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function FileTypeBadge({ type }: { type: string }) {
  const styles: Record<string, string> = {
    pdf:  "bg-blue-100 text-blue-700 border-blue-200",
    docx: "bg-green-100 text-green-700 border-green-200",
    txt:  "bg-gray-100 text-gray-600 border-gray-200",
  };
  const cls = styles[type?.toLowerCase()] ?? "bg-muted text-muted-foreground border-border";
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold border ${cls}`}>
      {type?.toUpperCase()}
    </span>
  );
}

function SkeletonRow() {
  return (
    <TableRow>
      {[1, 2, 3, 4, 5, 6].map((i) => (
        <TableCell key={i}>
          <div
            className="h-4 bg-muted rounded animate-pulse"
            style={{ width: i === 1 ? "60%" : i === 6 ? "80%" : "40%" }}
          />
        </TableCell>
      ))}
    </TableRow>
  );
}

// ---------------------------------------------------------------------------
// Actions kebab menu
// ---------------------------------------------------------------------------

function ActionMenu({
  doc,
  onView,
  onSummarize,
  onDownload,
  onDelete,
  summarizePending,
}: {
  doc: Document;
  onView: () => void;
  onSummarize: () => void;
  onDownload: () => void;
  onDelete: () => void;
  summarizePending: boolean;
}) {
  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger asChild>
        <Button size="icon" variant="ghost" className="h-8 w-8" aria-label="Actions">
          <MoreVertical className="w-4 h-4" />
        </Button>
      </DropdownMenu.Trigger>
      <DropdownMenu.Portal>
        <DropdownMenu.Content
          align="end"
          sideOffset={4}
          className="z-50 min-w-[160px] rounded-xl border border-border bg-popover p-1 shadow-md animate-in fade-in-0 zoom-in-95"
        >
          <DropdownMenu.Item
            onSelect={onView}
            className="flex items-center gap-2 px-3 py-2 text-sm rounded-lg cursor-pointer hover:bg-accent outline-none"
          >
            <Eye className="w-4 h-4 text-muted-foreground" />
            View
          </DropdownMenu.Item>

          {doc.status === "pending" ? (
            <DropdownMenu.Item
              onSelect={onSummarize}
              disabled={summarizePending}
              className="flex items-center gap-2 px-3 py-2 text-sm rounded-lg cursor-pointer hover:bg-accent outline-none disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Sparkles className="w-4 h-4 text-muted-foreground" />
              Summarize
            </DropdownMenu.Item>
          ) : (
            <DropdownMenu.Item
              onSelect={onDownload}
              className="flex items-center gap-2 px-3 py-2 text-sm rounded-lg cursor-pointer hover:bg-accent outline-none"
            >
              <Download className="w-4 h-4 text-muted-foreground" />
              Download
            </DropdownMenu.Item>
          )}

          <DropdownMenu.Separator className="my-1 h-px bg-border" />

          <DropdownMenu.Item
            onSelect={onDelete}
            className="flex items-center gap-2 px-3 py-2 text-sm rounded-lg cursor-pointer hover:bg-destructive/10 text-destructive outline-none"
          >
            <Trash2 className="w-4 h-4" />
            Delete
          </DropdownMenu.Item>
        </DropdownMenu.Content>
      </DropdownMenu.Portal>
    </DropdownMenu.Root>
  );
}

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------

const DocumentsPage = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [showUpload, setShowUpload] = useState(false);
  const [deleteTarget, setDeleteTarget] = useState<Document | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);
  const [file, setFile] = useState<File | null>(null);
  const [title, setTitle] = useState("");
  const [dragOver, setDragOver] = useState(false);

  const getExt = (f: File) => f.name.split(".").pop()?.toLowerCase() || "";

  const handleFile = useCallback((f: File) => {
    const ext = f.name.split(".").pop()?.toLowerCase() || "";
    if (!ALLOWED.includes(ext)) {
      toast.error("Only PDF, DOCX, and TXT files are allowed");
      return;
    }
    setFile(f);
    if (!title) setTitle(f.name.replace(/\.[^.]+$/, ""));
  }, [title]);

  const { data: documents = [], isLoading } = useQuery({
    queryKey: ["documents"],
    queryFn: fetchDocuments,
  });

  const deleteMutation = useMutation({
    mutationFn: deleteDocument,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["documents"] });
      toast.success("Document deleted");
      setDeleteTarget(null);
    },
    onError: () => toast.error("Failed to delete document"),
  });

  const summarizeMutation = useMutation({
    mutationFn: (id: string) => summarizeDocument(id, "concise"),
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: ["documents"] });
      toast.success("Summarization started");
      navigate(`/documents/${id}`);
    },
    onError: () => toast.error("Failed to summarize"),
  });

  const uploadMutation = useMutation({
    mutationFn: () => {
      if (!file) throw new Error("No file");
      return uploadDocument(title, file, getExt(file));
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["documents"] });
      toast.success("Document uploaded successfully!");
      setFile(null);
      setTitle("");
      setShowUpload(false);
    },
    onError: (error: Error) => {
      try {
        const parsed = JSON.parse(error.message);
        toast.error(parsed.detail || "Upload failed");
      } catch {
        toast.error(error.message || "Upload failed");
      }
    },
  });

  const formatDate = (dateStr: string) => {
    try {
      const date = new Date(dateStr.endsWith("Z") ? dateStr : dateStr + "Z");
      return format(date, "dd.MM.yyyy HH:mm");
    } catch {
      return dateStr;
    }
  };

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <AppHeader />
      <main className="flex-1 px-4 md:px-8 py-6 max-w-7xl mx-auto w-full">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold text-foreground">My documents</h1>
          <Button
            size="sm"
            variant={showUpload ? "secondary" : "default"}
            onClick={() => setShowUpload((v) => !v)}
            className="gap-2"
          >
            <Upload className="w-4 h-4" />
            {showUpload ? "Hide upload" : "Upload file"}
          </Button>
        </div>

        <div className="flex gap-6 items-start">

          {/* Documents table */}
          <div className={`${showUpload ? "flex-1 min-w-0" : "w-full"}`}>
            {isLoading ? (
              <div className="rounded-xl border border-border overflow-hidden bg-card">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Title</TableHead>
                      <TableHead>Type</TableHead>
                      <TableHead>Size</TableHead>
                      <TableHead>Date</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead></TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {[1, 2, 3].map((i) => <SkeletonRow key={i} />)}
                  </TableBody>
                </Table>
              </div>
            ) : documents.length === 0 ? (
              <div className="text-center py-20 text-muted-foreground">
                <FileText className="w-12 h-12 mx-auto mb-4 opacity-40" />
                <p className="mb-4">No documents yet. Upload your first file!</p>
                <Button onClick={() => setShowUpload(true)}>
                  <Upload className="w-4 h-4 mr-2" />
                  Upload a file
                </Button>
              </div>
            ) : (
              <div className="rounded-xl border border-border overflow-hidden bg-card">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead className="font-semibold text-foreground">Title</TableHead>
                      <TableHead className="font-semibold text-foreground">Type</TableHead>
                      <TableHead className="font-semibold text-foreground">Size</TableHead>
                      <TableHead className="font-semibold text-foreground">Date</TableHead>
                      <TableHead className="font-semibold text-foreground">Status</TableHead>
                      <TableHead className="w-12"></TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {documents.map((doc: Document) => (
                      <TableRow
                        key={doc.id}
                        className="cursor-pointer hover:bg-accent/30 transition-colors"
                        onClick={() => navigate(`/documents/${doc.id}`)}
                      >
                        <TableCell>
                          <span className="text-primary font-medium hover:underline">
                            {doc.title}
                          </span>
                        </TableCell>
                        <TableCell>
                          <FileTypeBadge type={doc.fileType} />
                        </TableCell>
                        <TableCell className="text-sm text-muted-foreground">
                          {formatFileSize(doc.fileSize)}
                        </TableCell>
                        <TableCell className="text-sm text-muted-foreground">
                          {formatDate(doc.createdAt)}
                        </TableCell>
                        <TableCell>
                          <Badge variant={doc.status === "summarized" ? "default" : "secondary"}>
                            {doc.status === "summarized" ? "Summarized" : "Pending"}
                          </Badge>
                        </TableCell>
                        <TableCell onClick={(e) => e.stopPropagation()}>
                          <ActionMenu
                            doc={doc}
                            onView={() => navigate(`/documents/${doc.id}`)}
                            onSummarize={() => summarizeMutation.mutate(doc.id)}
                            onDownload={() =>
                              downloadDocumentFile(doc.id).catch(() => toast.error("Download failed"))
                            }
                            onDelete={() => setDeleteTarget(doc)}
                            summarizePending={summarizeMutation.isPending}
                          />
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            )}
          </div>

          {/* Upload panel */}
          {showUpload && (
            <div className="w-80 shrink-0 rounded-2xl border border-border bg-card p-5 space-y-4">
              <h2 className="text-lg font-semibold text-foreground">Upload file</h2>

              <div
                className={`border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-all ${
                  dragOver
                    ? "border-primary bg-accent/40 ring-2 ring-primary ring-offset-2"
                    : "border-border hover:border-primary/50 hover:bg-accent/10"
                }`}
                onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
                onDragLeave={() => setDragOver(false)}
                onDrop={(e) => {
                  e.preventDefault();
                  setDragOver(false);
                  if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
                }}
                onClick={() => fileInputRef.current?.click()}
              >
                <CloudUpload className="w-8 h-8 mx-auto mb-2 text-primary/40" />
                <p className="text-sm text-muted-foreground">Drag & drop or</p>
                <Button variant="outline" size="sm" type="button" className="mt-1">Browse</Button>
                <p className="text-xs text-muted-foreground mt-2">PDF, DOCX, TXT · max 20MB</p>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".pdf,.docx,.txt"
                  className="hidden"
                  onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
                />
              </div>

              {file && (
                <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-accent/30 text-sm">
                  <span className="flex-1 truncate font-medium">{file.name}</span>
                  <span className="text-xs text-muted-foreground">{formatFileSize(file.size)}</span>
                  <button onClick={() => setFile(null)} className="text-muted-foreground hover:text-foreground">
                    <X className="w-4 h-4" />
                  </button>
                </div>
              )}

              <Input
                placeholder="Document title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
              />

              <Button
                className="w-full"
                onClick={() => uploadMutation.mutate()}
                disabled={!file || !title.trim() || uploadMutation.isPending}
              >
                <Upload className="w-4 h-4 mr-2" />
                {uploadMutation.isPending ? "Uploading..." : "Upload"}
              </Button>
            </div>
          )}
        </div>
      </main>

      {/* Delete confirmation dialog */}
      <AlertDialog open={!!deleteTarget} onOpenChange={(open) => { if (!open) setDeleteTarget(null); }}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle className="flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-destructive" />
              Delete document
            </AlertDialogTitle>
            <AlertDialogDescription>
              Are you sure you want to delete <span className="font-semibold">"{deleteTarget?.title}"</span>?
              This will also remove any generated summaries. This action cannot be undone.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
              onClick={() => deleteTarget && deleteMutation.mutate(deleteTarget.id)}
              disabled={deleteMutation.isPending}
            >
              {deleteMutation.isPending ? "Deleting..." : "Delete"}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
};

export default DocumentsPage;