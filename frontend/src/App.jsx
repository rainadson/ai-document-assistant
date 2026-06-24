import { useState } from 'react'
import Sidebar from './components/Sidebar'
import ChatArea from './components/ChatArea'

export default function App() {
  const [documents, setDocuments] = useState([])
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
    <div className="flex h-screen bg-gray-950 text-gray-100">
      <Sidebar documents={documents} onUpload={addDocument} />
      <ChatArea messages={messages} onSend={addMessage} />
    </div>
  )
}
