import { useState } from 'react'
import Sidebar from './components/Sidebar'
import ChatArea from './components/ChatArea'
import { PanelLeftOpen, PanelLeftClose } from 'lucide-react'

export default function App() {
  const [documents, setDocuments] = useState([])
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content: 'Olá! Faça upload de um documento na barra lateral e depois me faça perguntas sobre ele.',
      sources: [],
    },
  ])

  function addDocument(name) {
    setDocuments(prev => {
      if (prev.find(d => d.name === name)) return prev
      return [...prev, { name, uploadedAt: new Date().toLocaleTimeString('pt-BR') }]
    })
  }

  function addMessage(message) {
    setMessages(prev => [...prev, message])
  }

  return (
    <div className="flex h-screen bg-gray-950 text-gray-100 overflow-hidden">
      {/* Overlay mobile */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/60 z-20 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`
        fixed md:static inset-y-0 left-0 z-30
        transform transition-transform duration-300 ease-in-out
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
        md:translate-x-0
      `}>
        <Sidebar
          documents={documents}
          onUpload={name => { addDocument(name); setSidebarOpen(false) }}
        />
      </div>

      {/* Main */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Mobile header */}
        <div className="md:hidden flex items-center gap-3 px-4 py-3 bg-gray-900 border-b border-gray-800">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="text-gray-400 hover:text-white transition-colors"
          >
            {sidebarOpen ? <PanelLeftClose size={22} /> : <PanelLeftOpen size={22} />}
          </button>
          <span className="text-sm font-semibold text-white">AI Document Assistant</span>
        </div>

        <ChatArea messages={messages} onSend={addMessage} />
      </div>
    </div>
  )
}
