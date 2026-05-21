import { Link, useNavigate } from "react-router-dom";
import { removeToken } from "@/lib/api";
import { Button } from "@/components/ui/button";

const AppHeader = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    removeToken();
    navigate("/login");
  };

  return (
    <header className="w-full px-8 py-4 flex items-center justify-between">
      <Link to="/" className="inline-block">
        <span className="text-xl font-bold text-primary tracking-tight">powerr</span>
        <span className="block text-xs text-primary font-medium -mt-1">AI Study Summarizer</span>
      </Link>

      <Button variant="outline" size="sm" onClick={handleLogout}>
        Log out
      </Button>
    </header>
  );
};

export default AppHeader;