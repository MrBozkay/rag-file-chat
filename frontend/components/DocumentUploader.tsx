"use client";

import { useState, useRef } from "react";
import { Upload, X, File, CheckCircle, AlertCircle } from "lucide-react";
import axios from "axios";
import { cn } from "@/lib/utils";

interface DocumentUploaderProps {
  isOpen: boolean;
  onClose: () => void;
  onUploadComplete: () => void;
}

export function DocumentUploader({ isOpen, onClose, onUploadComplete }: DocumentUploaderProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<"idle" | "success" | "error">("idle");
  const fileInputRef = useRef<HTMLInputElement>(null);

  if (!isOpen) return null;

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
      setUploadStatus("idle");
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setUploadStatus("idle");
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setIsUploading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      await axios.post("http://localhost:8000/api/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setUploadStatus("success");
      setTimeout(() => {
        onUploadComplete();
        onClose();
        setFile(null);
        setUploadStatus("idle");
      }, 1500);
    } catch (error) {
      console.error("Upload failed", error);
      setUploadStatus("error");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-fade-in">
      <div className="glass-strong rounded-2xl shadow-2xl w-full max-w-md overflow-hidden border border-white/20 animate-slide-up">
        <div className="p-4 border-b border-white/10 flex justify-between items-center">
          <h3 className="font-semibold text-slate-100">Doküman Yükle</h3>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-200 transition-colors">
            <X size={20} />
          </button>
        </div>

        <div className="p-6">
          {!file ? (
            <div
              className={cn(
                "border-2 border-dashed rounded-xl p-8 text-center transition-all cursor-pointer",
                isDragging 
                  ? "border-primary-500 bg-primary-500/10 scale-[1.02]" 
                  : "border-white/20 hover:border-white/30 hover:bg-white/5"
              )}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <input
                type="file"
                ref={fileInputRef}
                className="hidden"
                onChange={handleFileSelect}
                accept=".pdf,.txt,.md,.csv"
              />
              <div className="w-12 h-12 bg-gradient-secondary rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg shadow-primary-500/30">
                <Upload size={24} className="text-white" />
              </div>
              <p className="text-sm font-medium text-slate-200">
                Dosyayı buraya sürükleyin veya seçin
              </p>
              <p className="text-xs text-slate-500 mt-1">PDF, TXT, MD, CSV (Max 10MB)</p>
            </div>
          ) : (
            <div className="glass rounded-xl p-4 border border-white/10">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 glass-strong border border-white/10 rounded-lg flex items-center justify-center text-slate-400">
                  <File size={20} />
                </div>
                <div className="flex-1 overflow-hidden">
                  <p className="text-sm font-medium text-slate-200 truncate">{file.name}</p>
                  <p className="text-xs text-slate-500">{(file.size / 1024).toFixed(1)} KB</p>
                </div>
                <button 
                  onClick={() => setFile(null)} 
                  className="text-slate-400 hover:text-red-400 transition-colors"
                  disabled={isUploading}
                >
                  <X size={18} />
                </button>
              </div>

              {uploadStatus === "error" && (
                <div className="mb-4 p-3 bg-red-500/10 border border-red-500/20 text-red-400 text-sm rounded-lg flex items-center gap-2">
                  <AlertCircle size={16} />
                  Yükleme başarısız oldu. Lütfen tekrar deneyin.
                </div>
              )}

              {uploadStatus === "success" && (
                <div className="mb-4 p-3 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-sm rounded-lg flex items-center gap-2">
                  <CheckCircle size={16} />
                  Dosya başarıyla yüklendi!
                </div>
              )}

              <button
                onClick={handleUpload}
                disabled={isUploading || uploadStatus === "success"}
                className={cn(
                  "w-full py-2.5 rounded-lg font-medium text-sm transition-all flex items-center justify-center gap-2",
                  isUploading
                    ? "bg-white/5 text-slate-500 cursor-not-allowed"
                    : uploadStatus === "success"
                    ? "bg-emerald-600 text-white"
                    : "bg-gradient-secondary hover:opacity-90 text-white shadow-lg shadow-primary-500/30 hover:scale-[1.02]"
                )}
              >
                {isUploading ? (
                  <>
                    <div className="w-4 h-4 border-2 border-slate-500 border-t-transparent rounded-full animate-spin" />
                    Yükleniyor...
                  </>
                ) : uploadStatus === "success" ? (
                  "Tamamlandı"
                ) : (
                  "Yüklemeyi Başlat"
                )}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
