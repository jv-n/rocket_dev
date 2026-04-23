import { useEffect, useRef, useState } from "react"
import { HugeiconsIcon } from "@hugeicons/react"
import { BubbleChatIcon, ArrowRight01Icon } from "@hugeicons/core-free-icons"
import { Button } from "@/components/atoms/Button/button"
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetDescription,
} from "@/components/atoms/sheet"
import { cn } from "@/lib/utils"

const API_BASE = "http://localhost:8000"

type Role = "user" | "assistant"

type Message = {
  role: Role
  text: string
}

export default function ChatWidget() {
  const [open, setOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const [sessionId, setSessionId] = useState<string | null>(null)
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages, loading])

  async function sendMessage() {
    const question = input.trim()
    if (!question || loading) return

    setInput("")
    setMessages((prev) => [...prev, { role: "user", text: question }])
    setLoading(true)

    try {
      const res = await fetch(`${API_BASE}/api/agent/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, question }),
      })

      if (!res.ok) throw new Error("Erro ao contatar o assistente.")

      const data: { session_id: string; answer: string } = await res.json()
      setSessionId(data.session_id)
      setMessages((prev) => [...prev, { role: "assistant", text: data.answer }])
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: "Ocorreu um erro. Tente novamente." },
      ])
    } finally {
      setLoading(false)
    }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        className="fixed bottom-6 right-6 z-50 flex h-14 w-14 items-center justify-center rounded-full bg-primary text-primary-foreground shadow-lg hover:opacity-90 transition-opacity"
        aria-label="Abrir assistente"
      >
        <HugeiconsIcon icon={BubbleChatIcon} size={24} strokeWidth={2} />
      </button>

      <Sheet open={open} onOpenChange={setOpen}>
        <SheetContent side="right" className="flex flex-col w-full sm:max-w-md p-0">
          <SheetHeader className="px-5 pt-5 pb-3 border-b">
            <SheetTitle>Assistente IA</SheetTitle>
            <SheetDescription>
              Faça perguntas sobre as vendas e produtos da sua loja.
            </SheetDescription>
          </SheetHeader>

          <div className="flex-1 overflow-y-auto px-4 py-4 flex flex-col gap-3">
            {messages.length === 0 && (
              <p className="text-sm text-muted-foreground text-center mt-8">
                Olá! Como posso ajudar você hoje?
              </p>
            )}
            {messages.map((msg, i) => (
              <div
                key={i}
                className={cn(
                  "max-w-[85%] rounded-xl px-4 py-2.5 text-sm whitespace-pre-wrap",
                  msg.role === "user"
                    ? "self-end bg-primary text-primary-foreground"
                    : "self-start bg-muted text-foreground"
                )}
              >
                {msg.text}
              </div>
            ))}
            {loading && (
              <div className="self-start bg-muted rounded-xl px-4 py-2.5 text-sm text-muted-foreground animate-pulse">
                Analisando...
              </div>
            )}
            <div ref={bottomRef} />
          </div>

          <div className="flex items-center gap-2 border-t px-4 py-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Faça uma pergunta..."
              disabled={loading}
              className="flex-1 rounded-lg border border-input bg-background px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-ring disabled:opacity-50"
            />
            <Button
              size="icon-sm"
              onClick={sendMessage}
              disabled={loading || !input.trim()}
            >
              <HugeiconsIcon icon={ArrowRight01Icon} size={16} strokeWidth={2} />
            </Button>
          </div>
        </SheetContent>
      </Sheet>
    </>
  )
}
