import { Link, useLocation } from "react-router-dom";

const AppHeader = () => {
  const location = useLocation();

  return (
    <header className="w-full px-4 md:px-8 py-4 flex items-center justify-between border-b border-border bg-card/80 backdrop-blur-sm sticky top-0 z-10">
      <Link to="/" className="inline-block">
        <span className="text-xl font-bold text-primary tracking-tight">powerr</span>
        <span className="block text-xs text-primary font-medium -mt-1">AI Study Summarizer</span>
      </Link>

      <nav className="flex items-center gap-6">
        <Link
          to="/documents"
          className={`text-sm font-medium transition-colors hover:text-foreground ${
            location.pathname.startsWith("/documents")
              ? "text-foreground"
              : "text-muted-foreground"
          }`}
        >
          My Documents
        </Link>
      </nav>
    </header>
  );
};

export default AppHeader;