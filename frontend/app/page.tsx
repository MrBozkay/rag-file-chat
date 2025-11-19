"use client";

import { useState } from "react";
import { Sidebar } from "@/components/Sidebar";
import { ChatInterface } from "@/components/ChatInterface";
import { DocumentUploader } from "@/components/DocumentUploader";

export default function Home() {
  const [isUploaderOpen, setIsUploaderOpen] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleUploadComplete = () => {
    // Trigger sidebar refresh
    setRefreshTrigger((prev) => prev + 1);
  };

  return (
    <main className="flex h-screen overflow-hidden bg-gradient-dark">
      <Sidebar key={refreshTrigger} onUploadClick={() => setIsUploaderOpen(true)} />
      
      <div className="flex-1 flex flex-col h-full relative">
        <ChatInterface />
      </div>

      <DocumentUploader 
        isOpen={isUploaderOpen} 
        onClose={() => setIsUploaderOpen(false)}
        onUploadComplete={handleUploadComplete}
      />
    </main>
  );
}
