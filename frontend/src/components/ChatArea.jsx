import { useState, useRef, useEffect } from 'react'
import { Send, Loader2 } from 'lucide-react'
import { askQuestion } from '../services/api'
import Message from './Message'

export default function ChatArea({ messages, onSend }) {
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  async function handleSubmit(e) {
    e.preventDefault()
    const question = input.trim()
    if (!question || loading) return

    setInput('')
    onSend({ id: Date.now(), role: 'user', content: question, sources: [] })
    setLoading(true)

    try {
      const data = await askQuestion(question)
      onSend({
        id: Date.now() + 1,
        role: 'assistant',
        content: data.answer,
        sources: data.sources,
      })
    } catch (err) {
      onSend({
        id: Date.now() + 1,
        role: 'assistant',
        content: 'Erro ao buscar a resposta. Verifique se o servidor está rodando.',
        sources: [],
        error: true,
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="flex-1 flex flex-col min-w-0">
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-800 bg-gray-900">
        <h2 className="text-sm font-semibold text-white">Conversa</h2>
        <p className="text-xs text-gray-400">Faça perguntas sobre os documentos enviados</p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-6 space-y-6">
        {messages.map(msg => (
          <Message key={msg.id} message={msg} />
        ))}
        {loading && (
          <div className="flex gap-3 items-start">
            <div className="w-8 h-8 rounded-full bg-violet-600 flex items-center justify-center shrink-0">
              <Loader2 size={16} className="animate-spin text-white" />
            </div>
            <div className="bg-gray-800 rounded-2xl rounded-tl-none px-4 py-3">
              <p className="text-sm text-gray-400">Buscando resposta...</p>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="px-6 py-4 border-t border-gray-800 bg-gray-900">
        <form onSubmit={handleSubmit} className="flex gap-3">
          <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Faça uma pergunta sobre o documento..."
            className="flex-1 bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-violet-500 transition-colors"
          />
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="bg-violet-600 hover:bg-violet-500 disabled:bg-gray-700 disabled:cursor-not-allowed text-white rounded-xl px-4 py-3 transition-colors flex items-center gap-2"
          >
            <Send size={16} />
          </button>
        </form>
      </div>
    </main>
  )
}
