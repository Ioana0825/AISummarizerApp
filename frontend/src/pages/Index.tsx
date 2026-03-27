import { useState, useCallback, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { CloudUpload, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { toast } from "sonner";
import AppHeader from "@/components/AppHeader";
import { uploadDocument } from "@/lib/api";

const ALLOWED = ["pdf", "docx", "txt"];

const Index = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const [file, setFile] = useState<File | null>(null);
  const [title, setTitle] = useState("");
  const [dragOver, setDragOver] = useState(false);

  const getExt = (f: File) => f.name.split(".").pop()?.toLowerCase() || "";

  const handleFile = useCallback(
    (f: File) => {
      const ext = getExt(f);

      if (!ALLOWED.includes(ext)) {
        toast.error("Only PDF, DOCX, and TXT files are allowed");
        return;
      }

      setFile(f);

      if (!title) {
        setTitle(f.name.replace(/\.[^.]+$/, ""));
      }
    },
    [title]
  );

  const uploadMutation = useMutation({
    mutationFn: () => {
      if (!file) throw new Error("No file");
      return uploadDocument(title, file, getExt(file));
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["documents"] });
      toast.success("Document uploaded successfully!");
      navigate("/documents");
    },
    onError: () => {
      toast.error("Upload failed");
    },
  });

  return (
    <div className="min-h-screen bg-background">
      <AppHeader />

      <main className="container mx-auto px-6 py-16">
        <div className="grid items-center gap-12 lg:grid-cols-2">
          {/* Left side */}
          <div className="max-w-xl">
            <h1 className="mb-6 text-5xl font-extrabold tracking-tight text-foreground md:text-6xl">
              Let's study together!
            </h1>

            <p className="mb-8 text-xl leading-relaxed text-muted-foreground">
              Upload your files and transform complex content into focused
              summaries designed for smarter studying
            </p>

            <Button
              size="lg"
              className="px-8"
              onClick={() => {
                if (file && title.trim() && !uploadMutation.isPending) {
                  uploadMutation.mutate();
                } else {
                  fileInputRef.current?.click();
                }
              }}
            >
              {uploadMutation.isPending ? "Uploading..." : file ? "Upload now" : "START"}
            </Button>
          </div>

          {/* Right side - real upload box */}
          <div className="rounded-3xl border bg-card p-8 shadow-sm">
            <div
              className={`rounded-2xl border-2 border-dashed p-8 text-center transition-colors cursor-pointer ${
                dragOver
                  ? "border-primary bg-primary/5"
                  : "border-border hover:border-primary/50"
              }`}
              onDragOver={(e) => {
                e.preventDefault();
                setDragOver(true);
              }}
              onDragLeave={() => setDragOver(false)}
              onDrop={(e) => {
                e.preventDefault();
                setDragOver(false);
                if (e.dataTransfer.files[0]) {
                  handleFile(e.dataTransfer.files[0]);
                }
              }}
              onClick={() => fileInputRef.current?.click()}
            >
              <CloudUpload className="mx-auto mb-4 h-10 w-10 text-primary" />
              <p className="mb-2 text-lg font-medium text-foreground">
                Drag or drop files here
              </p>
              <p className="mb-4 text-sm text-muted-foreground">- OR -</p>

              <Button type="button" variant="outline">
                Browse
              </Button>

              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,.docx,.txt"
                className="hidden"
                onChange={(e) => {
                  if (e.target.files?.[0]) {
                    handleFile(e.target.files[0]);
                  }
                }}
              />
            </div>

            {file && (
              <div className="mt-4 flex items-center justify-between rounded-xl border bg-muted/30 px-4 py-3">
                <div className="min-w-0">
                  <p className="truncate font-medium text-foreground">{file.name}</p>
                  <p className="text-sm text-muted-foreground uppercase">
                    {getExt(file)}
                  </p>
                </div>

                <button
                  type="button"
                  onClick={() => setFile(null)}
                  className="text-muted-foreground transition-colors hover:text-foreground"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
            )}

            <div className="mt-4 space-y-3">
              <Input
                placeholder="Document title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
              />

              <div className="flex gap-3">
                <Button
                  className="flex-1"
                  onClick={() => uploadMutation.mutate()}
                  disabled={!file || !title.trim() || uploadMutation.isPending}
                >
                  {uploadMutation.isPending ? "Uploading..." : "Upload"}
                </Button>

                <Button
                  type="button"
                  variant="outline"
                  onClick={() => navigate("/documents")}
                >
                  My documents
                </Button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;