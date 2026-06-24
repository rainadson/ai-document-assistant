import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000',
})

export async function uploadDocument(file) {
  const formData = new FormData()
  formData.append('file', file)
  const { data } = await api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

export async function askQuestion(question) {
  const { data } = await api.post('/ask', { question })
  return data
}
