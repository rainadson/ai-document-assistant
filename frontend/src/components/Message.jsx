import { FileText, BrainCircuit, User } from 'lucide-react'

export default function Message({ message }) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex gap-3 items-start ${isUser ? 'flex-row-reverse' : ''}`}>
      {/* Avatar */}
      <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
        isUser ? 'bg-gray-700' : 'bg-violet-600'
      }`}>
        {isUser
          ? <User size={16} className="text-gray-300" />
          : <BrainCircuit size={16} className="text-white" />
        }
      </div>

      {/* Bubble */}
      <div className={`max-w-[75%] ${isUser ? 'items-end' : 'items-start'} flex flex-col gap-2`}>
        <div className={`px-4 py-3 rounded-2xl text-sm leading-relaxed ${
          isUser
            ? 'bg-violet-600 text-white rounded-tr-none'
            : message.error
              ? 'bg-red-900/40 border border-red-800 text-red-300 rounded-tl-none'
              : 'bg-gray-800 text-gray-100 rounded-tl-none'
        }`}>
          {message.content}
        </div>

        {/* Sources */}
        {message.sources?.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {message.sources.map(source => (
              <span
                key={source}
                className="flex items-center gap-1 text-xs bg-gray-800 border border-gray-700 text-gray-400 px-2 py-1 rounded-full"
              >
                <FileText size={11} />
                {source}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
