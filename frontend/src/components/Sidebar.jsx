import { useState, useRef } from 'react'
import { Upload, FileText, Loader2, BrainCircuit } from 'lucide-react'
import { uploadDocument } from '../services/api'

export default function Sidebar({ documents, onUpload }) {
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState('')
  const inputRef = useRef(null)

  async function handleFile(file) {
    if (!file) return
    setError('')
    setUploading(true)
    try {
      await uploadDocument(file)
      onUpload(file.name)
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao enviar o arquivo.')
    } finally {
      setUploading(false)
    }
  }

  function handleDrop(e) {
    e.preventDefault()
    handleFile(e.dataTransfer.files[0])
  }

  return (
    <aside className="w-72 min-w-[288px] h-full bg-gray-900 border-r border-gray-800 flex flex-col">
      {/* Logo — hidden on mobile (shown in App header instead) */}
      <div className="hidden md:flex p-5 border-b border-gray-800 items-center gap-3">
        <BrainCircuit className="text-violet-400" size={24} />
        <div>
          <h1 className="text-sm font-semibold text-white leading-tight">AI Document Assistant</h1>
          <p className="text-xs text-gray-400">Powered by Groq + LangChain</p>
        </div>
      </div>

      {/* Upload area */}
      <div className="p-4">
        <p className="text-xs font-medium text-gray-400 uppercase tracking-wider mb-3">Upload de Documento</p>
        <div
          className="border-2 border-dashed border-gray-700 rounded-xl p-5 text-center cursor-pointer hover:border-violet-500 hover:bg-violet-500/5 transition-all"
          onClick={() => inputRef.current?.click()}
          onDrop={handleDrop}
          onDragOver={e => e.preventDefault()}
        >
          {uploading ? (
            <Loader2 className="mx-auto text-violet-400 animate-spin mb-2" size={24} />
          ) : (
            <Upload className="mx-auto text-gray-500 mb-2" size={24} />
          )}
          <p className="text-sm text-gray-400">
            {uploading ? 'Processando...' : 'Clique ou arraste um arquivo'}
          </p>
          <p className="text-xs text-gray-600 mt-1">PDF, DOCX ou TXT</p>
          <input
            ref={inputRef}
            type="file"
            accept=".pdf,.docx,.txt"
            className="hidden"
            onChange={e => handleFile(e.target.files[0])}
          />
        </div>
        {error && <p className="text-xs text-red-400 mt-2">{error}</p>}
      </div>

      {/* Documents list */}
      <div className="px-4 flex-1 overflow-y-auto">
        <p className="text-xs font-medium text-gray-400 uppercase tracking-wider mb-3">
          Documentos ({documents.length})
        </p>
        {documents.length === 0 ? (
          <p className="text-xs text-gray-600 text-center mt-4">Nenhum documento enviado</p>
        ) : (
          <ul className="space-y-2">
            {documents.map(doc => (
              <li key={doc.name} className="flex items-start gap-2 bg-gray-800 rounded-lg p-3">
                <FileText className="text-violet-400 mt-0.5 shrink-0" size={16} />
                <div className="min-w-0">
                  <p className="text-sm text-gray-200 truncate">{doc.name}</p>
                  <p className="text-xs text-gray-500">{doc.uploadedAt}</p>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-gray-800">
        <p className="text-xs text-gray-600 text-center">
          RAG · ChromaDB · HuggingFace
        </p>
      </div>
    </aside>
  )
}
