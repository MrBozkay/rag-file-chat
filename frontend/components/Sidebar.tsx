"use client";

import { useState, useEffect } from "react";
import { Upload, FileText, MessageSquare, Settings, Plus, Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";
import axios from "axios";

interface Document {
  name: string;
  display_name: string;
  uri: string;
}

export function Sidebar({ onUploadClick }: { onUploadClick: () => void }) {
  const [documents, setDocuments] = useState<Document[]>([]);

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const response = await axios.get("http://localhost:8000/api/documents");
      setDocuments(response.data);
    } catch (error) {
      console.error("Failed to fetch documents", error);
    }
  };

  return (
    <div className="w-64 glass-strong h-screen flex flex-col border-r border-white/10 animate-fade-in">
      <div className="p-4 border-b border-white/10">
        <h1 className="text-xl font-bold flex items-center gap-2">
          <div className="w-8 h-8 bg-gradient-secondary rounded-lg flex items-center justify-center shadow-lg shadow-primary-500/20">
            <Sparkles size={18} className="text-white" />
          </div>
          <span className="bg-gradient-to-r from-primary-400 to-accent-purple bg-clip-text text-transparent">
            KABP
          </span>
        </h1>
        <p className="text-xs text-slate-400 mt-1">Kurumsal Akıllı Bilgi Platformu</p>
      </div>

      <div className="p-4">
        <button
          onClick={onUploadClick}
          className="w-full bg-gradient-secondary hover:opacity-90 text-white rounded-lg p-3 flex items-center justify-center gap-2 transition-all shadow-lg shadow-primary-500/20 hover:shadow-primary-500/30 hover:scale-[1.02]"
        >
          <Plus size={18} />
          <span className="font-medium">Yeni Doküman</span>
        </button>
      </div>

      <div className="flex-1 overflow-y-auto px-2">
        <div className="mb-6">
          <h2 className="text-xs font-semibold text-slate-500 uppercase tracking-wider px-2 mb-2">
            Menü
          </h2>
          <nav className="space-y-1">
            <a href="#" className="flex items-center gap-3 px-3 py-2.5 text-slate-300 hover:bg-white/5 rounded-lg group transition-all">
              <MessageSquare size={18} className="group-hover:text-primary-400 transition-colors" />
              <span className="group-hover:text-white transition-colors">Sohbet</span>
            </a>
            <a href="#" className="flex items-center gap-3 px-3 py-2.5 text-slate-300 hover:bg-white/5 rounded-lg group transition-all">
              <Settings size={18} className="group-hover:text-primary-400 transition-colors" />
              <span className="group-hover:text-white transition-colors">Ayarlar</span>
            </a>
          </nav>
        </div>

        <div>
          <h2 className="text-xs font-semibold text-slate-500 uppercase tracking-wider px-2 mb-2">
            Dokümanlar ({documents.length})
          </h2>
          <div className="space-y-1">
            {documents.map((doc, idx) => (
              <div key={idx} className="flex items-center gap-3 px-3 py-2.5 text-slate-400 hover:bg-white/5 rounded-lg text-sm truncate group transition-all cursor-pointer">
                <FileText size={16} className="shrink-0 group-hover:text-primary-400 transition-colors" />
                <span className="truncate group-hover:text-slate-200 transition-colors">{doc.display_name || doc.name}</span>
              </div>
            ))}
            {documents.length === 0 && (
              <div className="px-3 py-4 text-center text-slate-600 text-sm">
                Henüz doküman yok
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="p-4 border-t border-white/10">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-gradient-accent rounded-full flex items-center justify-center shadow-md">
            <span className="text-xs font-bold text-white">U</span>
          </div>
          <div className="flex-1 overflow-hidden">
            <p className="text-sm font-medium truncate text-slate-200">Kullanıcı</p>
            <p className="text-xs text-slate-500 truncate">user@company.com</p>
          </div>
        </div>
      </div>
    </div>
  );
}
