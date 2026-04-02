import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { TooltipProvider } from "@/components/ui/tooltip";
import { Toaster as Sonner } from "@/components/ui/sonner";
import Index from "./pages/Index";
import DocumentsPage from "./pages/DocumentsPage";
import UploadPage from "./pages/UploadPage";
import DocumentDetailPage from "./pages/DocumentDetailPage";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Index />} />
          <Route path="/documents" element={<DocumentsPage />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/documents/:id" element={<DocumentDetailPage />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;