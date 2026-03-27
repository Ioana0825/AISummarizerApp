import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import AppHeader from "@/components/AppHeader";

const Index = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <AppHeader />
      <main className="flex-1 flex items-center justify-center px-8">
        <div className="max-w-6xl w-full grid md:grid-cols-2 gap-12 items-center">
          {/* Left: hero text */}
          <div className="space-y-6">
            <h1 className="text-4xl md:text-5xl font-bold text-foreground leading-tight">
              Let's study together!
            </h1>
            <p className="text-lg text-muted-foreground max-w-md">
              Upload your files and transform complex content into focused summaries
              designed for smarter studying
            </p>
            <Button
              size="lg"
              className="px-10 text-base font-semibold"
              onClick={() => navigate("/documents")}
            >
              START
            </Button>
          </div>

          {/* Right: decorative card */}
          <div className="flex justify-center">
            <div className="w-full max-w-md rounded-2xl border border-border p-8 bg-card flex flex-col gap-4">
              <div className="h-3 w-2/3 rounded bg-accent" />
              <div className="h-3 w-full rounded bg-muted" />
              <div className="h-3 w-5/6 rounded bg-muted" />
              <div className="h-3 w-3/4 rounded bg-muted" />
              <div className="mt-4 h-10 w-32 rounded-lg bg-primary/20 border border-primary/30 flex items-center justify-center">
                <span className="text-xs font-semibold text-primary">AI Summary</span>
              </div>
              <div className="h-3 w-full rounded bg-accent/60" />
              <div className="h-3 w-4/5 rounded bg-accent/60" />
              <div className="h-3 w-2/3 rounded bg-accent/40" />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;