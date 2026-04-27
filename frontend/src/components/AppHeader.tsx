import { Link } from "react-router-dom";

const AppHeader = () => {
  return (
    <header className="w-full px-8 py-4 flex items-center justify-between">
      <Link to="/" className="inline-block">
        <span className="text-xl font-bold text-primary tracking-tight">powerr</span>
        <span className="block text-xs text-primary font-medium -mt-1">AI Study Summarizer</span>
      </Link>
    </header>
  );
};

export default AppHeader;