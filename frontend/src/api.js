import axios from 'axios'

// In production, set VITE_API_URL to the deployed backend URL
// e.g. https://career-pathfinder-api.onrender.com
// In local dev, Vite's proxy rewrites /api → http://127.0.0.1:8000
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: { 'Content-Type': 'application/json' },
})

export async function onboard(skills, interests) {
  const { data } = await api.post('/onboard', { skills, interests })
  return data
}

export async function recommend(userId) {
  const { data } = await api.post('/recommend', { user_id: userId })
  return data
}

export async function getPath(userId, career) {
  const { data } = await api.post('/path', { user_id: userId, career })
  return data
}
