# AI Document Assistant

> Chatbot inteligente que responde perguntas sobre documentos usando RAG (Retrieval Augmented Generation). Faça upload de um PDF, DOCX ou TXT e converse com o conteúdo do arquivo em tempo real.

![Dashboard](screenshots/dashboard.png)

---

## Demonstração

| Upload de documento | Resposta com fontes |
|---|---|
| ![Upload](screenshots/upload.png) | ![Chat](screenshots/chat.png) |

---

## Arquitetura

```
Usuário
   │
   ▼
React Frontend (Vite + Tailwind)
   │
   ▼  HTTP REST
FastAPI Backend
   │
   ├── POST /upload
   │     └── LangChain → chunks → HuggingFace Embeddings → ChromaDB
   │
   └── POST /ask
         └── HuggingFace Embeddings → ChromaDB (busca) → Groq LLaMA 3 → Resposta
```

**Fluxo completo:**

1. Usuário faz upload de um documento
2. O texto é extraído e dividido em chunks de 1000 caracteres
3. Cada chunk é convertido em vetores numéricos (embeddings) pelo HuggingFace
4. Os vetores são armazenados localmente no ChromaDB
5. Usuário faz uma pergunta
6. A pergunta é convertida em vetor e os 4 chunks mais relevantes são recuperados
7. O Groq (LLaMA 3) gera uma resposta baseada exclusivamente nesses chunks
8. A resposta é exibida junto com os arquivos usados como fonte

---

## Tecnologias

### Backend
| Tecnologia | Função |
|---|---|
| Python 3.12 | Linguagem principal |
| FastAPI | API REST |
| LangChain | Orquestração do pipeline RAG |
| ChromaDB | Banco de dados vetorial local |
| HuggingFace | Embeddings gratuitos (roda localmente) |
| Groq + LLaMA 3 | Geração de respostas (API gratuita) |
| PyPDF / python-docx | Leitura de PDF e DOCX |

### Frontend
| Tecnologia | Função |
|---|---|
| React 19 | Interface de usuário |
| Vite | Build tool |
| Tailwind CSS | Estilização |
| Axios | Requisições HTTP |
| Lucide React | Ícones |

---

## Instalação

### Pré-requisitos
- Python 3.12+
- Node.js 18+
- Conta gratuita no [Groq](https://console.groq.com)

### Backend

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/ai-document-assistant.git
cd ai-document-assistant

# Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows

# Instale as dependências
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

---

## Configuração

```bash
# Na pasta raiz do projeto
cp .env.example .env
```

Edite o arquivo `.env`:
```
GROQ_API_KEY=sua-chave-groq-aqui
```

Obtenha sua chave gratuita em: https://console.groq.com

---

## Executando localmente

**Terminal 1 — Backend:**
```bash
uvicorn main:app --reload
```
API disponível em: http://localhost:8000

Documentação interativa: http://localhost:8000/docs

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```
Interface disponível em: http://localhost:5173

---

## Endpoints

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/upload` | Upload e processamento de documento |
| `POST` | `/ask` | Pergunta sobre os documentos |

### POST /upload

```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@documento.pdf"
```

Resposta:
```json
{
  "message": "Document processed successfully"
}
```

### POST /ask

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Quais são as habilidades técnicas do candidato?"}'
```

Resposta:
```json
{
  "answer": "O candidato possui habilidades em Java, React, TypeScript e Engenharia de IA...",
  "sources": ["curriculo.pdf"]
}
```

---

## Estrutura de pastas

```
ai-document-assistant/
├── app/
│   ├── api/
│   │   ├── upload.py          # POST /upload
│   │   └── chat.py            # POST /ask
│   ├── services/
│   │   ├── document_loader.py # Leitura e chunking de documentos
│   │   ├── embeddings.py      # HuggingFace embeddings
│   │   ├── vector_store.py    # ChromaDB
│   │   └── rag_service.py     # Pipeline RAG
│   └── schemas/
│       ├── ask_request.py
│       └── ask_response.py
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── Sidebar.jsx    # Upload + lista de documentos
│       │   ├── ChatArea.jsx   # Área de conversa
│       │   └── Message.jsx    # Bolha de mensagem
│       └── services/
│           └── api.js         # Integração com o backend
├── data/
│   ├── uploads/               # Arquivos enviados
│   └── vectordb/              # ChromaDB (persistência local)
├── tests/
├── main.py
├── requirements.txt
└── .env.example
```

---

## Testes

```bash
pytest tests/ -v
```

---

## Melhorias futuras

- [ ] Autenticação com JWT
- [ ] Suporte a múltiplos usuários com coleções separadas no ChromaDB
- [ ] Streaming da resposta token a token
- [ ] Deduplicação de documentos já indexados
- [ ] Endpoint para deletar documentos
- [ ] Deploy com Docker Compose
- [ ] Histórico de conversas persistido

---

## Autor

**Rainadson Angelo**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/seu-perfil)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/seu-usuario)

---

## Licença

MIT
