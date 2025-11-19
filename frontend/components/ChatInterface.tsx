"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Bot, User, Paperclip, Loader2 } from "lucide-react";
import axios from "axios";
import { cn } from "@/lib/utils";

interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Merhaba! Ben KABP asistanıyım. Kurumsal dokümanlarınızla ilgili sorularınızı cevaplamaya hazırım.",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      role: "user",
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      // In a real app, we would pass selected file URIs here
      const response = await axios.post("http://localhost:8000/api/chat", {
        query: userMessage.content,
        file_uris: [], // TODO: Add selected file context
      });

      const botMessage: Message = {
        role: "assistant",
        content: response.data.response,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Chat failed", error);
      const errorMessage: Message = {
        role: "assistant",
        content: "Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-screen">
      {/* Chat Header */}
      <div className="glass border-b border-white/10 px-6 py-4 flex items-center justify-between backdrop-blur-xl">
        <div>
          <h2 className="text-lg font-semibold text-slate-100">Kurumsal Asistan</h2>
          <p className="text-xs text-slate-400 flex items-center gap-1">
            <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></span>
            Çevrimiçi
          </p>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={cn(
              "flex gap-4 max-w-3xl mx-auto animate-slide-up",
              msg.role === "user" ? "flex-row-reverse" : "flex-row"
            )}
          >
            <div
              className={cn(
                "w-8 h-8 rounded-full flex items-center justify-center shrink-0 shadow-lg",
                msg.role === "user" 
                  ? "bg-gradient-secondary" 
                  : "bg-gradient-accent"
              )}
            >
              {msg.role === "user" ? <User size={16} className="text-white" /> : <Bot size={16} className="text-white" />}
            </div>
            
            <div
              className={cn(
                "rounded-2xl px-6 py-4 shadow-lg max-w-[80%] backdrop-blur-sm",
                msg.role === "user" 
                  ? "bg-gradient-secondary text-white rounded-tr-none shadow-primary-500/20" 
                  : "glass-strong text-slate-100 rounded-tl-none border border-white/10"
              )}
            >
              <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>
              <span 
                className={cn(
                  "text-[10px] mt-2 block opacity-70",
                  msg.role === "user" ? "text-blue-100" : "text-slate-400"
                )}
              >
                {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </span>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="flex gap-4 max-w-3xl mx-auto animate-slide-up">
            <div className="w-8 h-8 rounded-full bg-gradient-accent flex items-center justify-center shrink-0 shadow-lg">
              <Bot size={16} className="text-white" />
            </div>
            <div className="glass-strong rounded-2xl rounded-tl-none px-6 py-4 shadow-lg border border-white/10">
              <div className="flex gap-1">
                <div className="w-2 h-2 bg-primary-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                <div className="w-2 h-2 bg-primary-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                <div className="w-2 h-2 bg-primary-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="glass border-t border-white/10 p-4 backdrop-blur-xl">
        <div className="max-w-3xl mx-auto relative">
          <div className="absolute left-3 bottom-3 flex items-center gap-2">
            <button className="p-2 text-slate-400 hover:text-primary-400 hover:bg-white/5 rounded-full transition-all">
              <Paperclip size={20} />
            </button>
          </div>
          
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Bir soru sorun..."
            className="w-full glass-strong border border-white/10 rounded-xl pl-12 pr-12 py-3 min-h-[52px] max-h-32 focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500/50 resize-none text-sm text-slate-100 placeholder-slate-500"
            rows={1}
          />
          
          <button
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
            className={cn(
              "absolute right-3 bottom-2.5 p-2 rounded-lg transition-all",
              input.trim() && !isLoading
                ? "bg-gradient-secondary text-white hover:opacity-90 shadow-lg shadow-primary-500/30 hover:scale-105" 
                : "bg-white/5 text-slate-600 cursor-not-allowed"
            )}
          >
            {isLoading ? <Loader2 size={18} className="animate-spin" /> : <Send size={18} />}
          </button>
        </div>
        <p className="text-center text-xs text-slate-500 mt-2">
          KABP yapay zeka asistanı hata yapabilir. Önemli bilgileri kontrol edin.
        </p>
      </div>
    </div>
  );
}
