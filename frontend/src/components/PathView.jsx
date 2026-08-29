import { useEffect, useState } from 'react'
import ReactMarkdown from 'react-markdown'
import { useNavigate } from 'react-router-dom'
import { getPath } from '../api'

export default function PathView({ userId, selectedCareer }) {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [pathData, setPathData] = useState(null)

  useEffect(() => {
    if (!userId || !selectedCareer) {
      setLoading(false)
      return
    }

    let cancelled = false

    async function fetchPath() {
      setLoading(true)
      setError('')
      try {
        const data = await getPath(userId, selectedCareer.role)
        if (!cancelled) setPathData(data)
      } catch (err) {
        if (!cancelled) {
          setError(err.response?.data?.detail || 'Failed to load learning path.')
        }
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    fetchPath()
    return () => {
      cancelled = true
    }
  }, [userId, selectedCareer])

  if (!userId || !selectedCareer) {
    return (
      <section className="mx-auto max-w-3xl px-6 py-16 text-center">
        <p className="mb-4 text-slate-600">Select a career from recommendations to view your path.</p>
        <button
          type="button"
          onClick={() => navigate('/recommendations')}
          className="rounded-lg bg-indigo-600 px-5 py-2.5 font-medium text-white hover:bg-indigo-700"
        >
          Back to Recommendations
        </button>
      </section>
    )
  }

  return (
    <section className="mx-auto max-w-3xl px-6 py-12">
      <button
        type="button"
        onClick={() => navigate('/recommendations')}
        className="mb-6 text-sm font-medium text-indigo-600 hover:text-indigo-800"
      >
        ← Back to recommendations
      </button>

      <div className="mb-8">
        <h2 className="text-3xl font-bold text-slate-900">{selectedCareer.role}</h2>
        <p className="mt-2 text-slate-600">Your personalized 6-month learning timeline</p>
        {pathData?.source && (
          <span className="mt-3 inline-block rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600">
            Generated via {pathData.source === 'gemini' ? 'Gemini' : 'template (demo mode)'}
          </span>
        )}
      </div>

      {loading && (
        <div className="rounded-2xl bg-white p-8 text-center shadow-md">
          <p className="text-slate-600">Building your learning path…</p>
        </div>
      )}

      {error && (
        <div className="rounded-2xl bg-red-50 p-6 text-red-700 shadow-md">{error}</div>
      )}

      {!loading && !error && pathData && (
        <article className="rounded-2xl bg-white p-6 shadow-md shadow-slate-200/60 sm:p-8">
          <ReactMarkdown
            components={{
              h2: ({ children }) => <h2 className="mb-6 text-2xl font-bold text-slate-900">{children}</h2>,
              h3: ({ children }) => <h3 className="mb-3 mt-8 text-lg font-semibold text-slate-900 first:mt-0">{children}</h3>,
              p: ({ children }) => <p className="mb-4 text-sm leading-relaxed text-slate-600">{children}</p>,
              ul: ({ children }) => <ul className="mb-4 list-disc space-y-2 pl-5 text-sm leading-relaxed text-slate-600">{children}</ul>,
              li: ({ children }) => <li className="pl-1">{children}</li>,
              hr: () => <hr className="my-6 border-slate-200" />,
              strong: ({ children }) => <strong className="font-semibold text-slate-800">{children}</strong>,
            }}
          >
            {pathData.learning_path}
          </ReactMarkdown>
        </article>
      )}
    </section>
  )
}
