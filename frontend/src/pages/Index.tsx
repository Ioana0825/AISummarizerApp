import { useState, useCallback, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { CloudUpload, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { toast } from "sonner";
import AppHeader from "@/components/AppHeader";
import { uploadDocument, loginUser, registerUser, isLoggedIn, setToken } from "@/lib/api";
import heroImage from "../assets/hero-study.png";

const ALLOWED = ["pdf", "docx", "txt"];

const Index = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const fileInputRef = useRef<HTMLInputElement>(null);

  // ─── Auth state ───────────────────────────────────────────────────────────
  const [loggedIn, setLoggedIn] = useState(false); // temporary debug
  const [authMode, setAuthMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [authLoading, setAuthLoading] = useState(false);
  const [transitioning, setTransitioning] = useState(false);

  // ─── Upload state ─────────────────────────────────────────────────────────
  const [file, setFile] = useState<File | null>(null);
  const [title, setTitle] = useState("");
  const [dragOver, setDragOver] = useState(false);

  const getExt = (f: File) => f.name.split(".").pop()?.toLowerCase() || "";

  const handleFile = useCallback((f: File) => {
    const ext = getExt(f);
    if (!ALLOWED.includes(ext)) {
      toast.error("Only PDF, DOCX, and TXT files are allowed");
      return;
    }
    setFile(f);
    if (!title) setTitle(f.name.replace(/\.[^.]+$/, ""));
  }, [title]);

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
    onError: () => toast.error("Upload failed"),
  });

  // ─── Auth handler ─────────────────────────────────────────────────────────
  const handleAuth = async () => {
    if (!email || !password) {
      toast.error("Please fill in all fields");
      return;
    }
    if (authMode === "register" && password !== confirmPassword) {
      toast.error("Passwords do not match");
      return;
    }
    if (authMode === "register" && password.length < 6) {
      toast.error("Password must be at least 6 characters");
      return;
    }

    setAuthLoading(true);
    try {
      if (authMode === "register") {
        await registerUser(email, password);
        await loginUser(email, password);
        toast.success("Account created! Welcome!");
      } else {
        await loginUser(email, password);
        toast.success("Welcome back!");
      }
      // trigger slide transition
      setTransitioning(true);
      setTimeout(() => {
        setLoggedIn(true);
        setTransitioning(false);
      }, 400);
    } catch {
      toast.error(authMode === "login" ? "Invalid email or password" : "Registration failed");
    } finally {
      setAuthLoading(false);
    }
  };

  // ─── Render ───────────────────────────────────────────────────────────────
  return (
    <div className="min-h-screen bg-background flex flex-col">
      <AppHeader />
      <main className="flex-1 flex items-center justify-center px-8 py-8">
        <div className="max-w-6xl w-full grid md:grid-cols-2 gap-12 items-center">

          {/* Left: hero */}
          <div className="space-y-6">
            <div className="space-y-4">
              <h1 className="text-4xl md:text-5xl font-bold text-foreground leading-tight">
                Let's study together!
              </h1>
              <p className="text-lg text-muted-foreground max-w-md">
                Upload your files and transform complex content into focused summaries
                designed for smarter studying
              </p>
            </div>
            <div className="pt-4">
              <div className="w-full max-w-md h-48 rounded-lg flex items-center justify-center">
                <img
                  src={heroImage}
                  alt=""
                  className="w-full max-w-lg"
                  style={{ mixBlendMode: "multiply" }}
                />
              </div>
            </div>
          </div>

          {/* Right: animated card */}
          <div
            className="rounded-2xl border border-border bg-card p-8 min-h-[480px] flex flex-col justify-center overflow-hidden"
            style={{
              transition: "opacity 0.4s ease, transform 0.4s ease",
              opacity: transitioning ? 0 : 1,
              transform: transitioning ? "translateX(30px)" : "translateX(0)",
            }}
          >

            {/* ── LOGIN / REGISTER form ── */}
            {!loggedIn && (
              <div className="space-y-6">
                <div className="space-y-1 text-center">
                  <h2 className="text-2xl font-bold text-foreground">
                    {authMode === "login" ? "Welcome back" : "Create an account"}
                  </h2>
                  <p className="text-muted-foreground text-sm">
                    {authMode === "login"
                      ? "Log in to start summarizing"
                      : "Sign up to get started"}
                  </p>
                </div>

                <div className="space-y-4">
                  <div className="space-y-1">
                    <label className="text-sm font-medium text-foreground">Email</label>
                    <Input
                      type="email"
                      placeholder="you@example.com"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                    />
                  </div>
                  <div className="space-y-1">
                    <label className="text-sm font-medium text-foreground">Password</label>
                    <Input
                      type="password"
                      placeholder="••••••••"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                    />
                  </div>
                  {authMode === "register" && (
                    <div className="space-y-1">
                      <label className="text-sm font-medium text-foreground">Confirm Password</label>
                      <Input
                        type="password"
                        placeholder="••••••••"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        onKeyDown={(e) => e.key === "Enter" && handleAuth()}
                      />
                    </div>
                  )}
                </div>

                <Button className="w-full" onClick={handleAuth} disabled={authLoading}>
                  {authLoading
                    ? authMode === "login" ? "Logging in..." : "Creating account..."
                    : authMode === "login" ? "Log in" : "Register"}
                </Button>

                <p className="text-center text-sm text-muted-foreground">
                  {authMode === "login" ? "Don't have an account? " : "Already have an account? "}
                  <button
                    className="text-primary font-medium hover:underline"
                    onClick={() => setAuthMode(authMode === "login" ? "register" : "login")}
                  >
                    {authMode === "login" ? "Register" : "Log in"}
                  </button>
                </p>
              </div>
            )}

            {/* ── UPLOAD form ── */}
            {loggedIn && (
              <div className="space-y-6">
                <div
                  className={`border-2 border-dashed rounded-xl p-16 text-center cursor-pointer transition-colors ${
                    dragOver ? "border-primary bg-accent/40" : "border-border"
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
                  <CloudUpload className="w-10 h-10 mx-auto mb-3 text-primary/60" />
                  <p className="font-medium text-foreground">Drag or drop files here</p>
                  <p className="text-xs text-muted-foreground my-2">- OR -</p>
                  <Button variant="outline" size="sm" type="button">Browse</Button>
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
                    <span className="uppercase text-xs text-muted-foreground font-semibold">{getExt(file)}</span>
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

                <div className="flex gap-3">
                  <Button
                    className="flex-1"
                    onClick={() => uploadMutation.mutate()}
                    disabled={!file || !title.trim() || uploadMutation.isPending}
                  >
                    {uploadMutation.isPending ? "Uploading..." : "Upload"}
                  </Button>
                  <Button variant="outline" className="flex-1" onClick={() => navigate("/documents")}>
                    My documents
                  </Button>
                </div>
              </div>
            )}

          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;