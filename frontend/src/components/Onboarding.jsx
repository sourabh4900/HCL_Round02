import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { onboard, recommend } from '../api'

const INTEREST_OPTIONS = [
  'Data Science',
  'Software Engineering',
  'Business & Management',
  'Product & Design',
  'Healthcare',
  'Finance',
  'Cybersecurity',
  'Marketing',
]

export default function Onboarding({ setUserId, setCareers }) {
  const navigate = useNavigate()
  const [skillsInput, setSkillsInput] = useState('')
  const [skills, setSkills] = useState([])
  const [interests, setInterests] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const addSkill = () => {
    const value = skillsInput.trim()
    if (!value) return
    const newSkills = value
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean)
      .filter((s) => !skills.includes(s))
    if (newSkills.length) {
      setSkills((prev) => [...prev, ...newSkills])
    }
    setSkillsInput('')
  }

  const removeSkill = (skill) => {
    setSkills((prev) => prev.filter((s) => s !== skill))
  }

  const toggleInterest = (interest) => {
    setInterests((prev) =>
      prev.includes(interest) ? prev.filter((i) => i !== interest) : [...prev, interest],
    )
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')

    if (skills.length === 0) {
      setError('Add at least one skill before continuing.')
      return
    }

    setLoading(true)
    try {
      const { user_id } = await onboard(skills, interests)
      const { careers } = await recommend(user_id)
      setUserId(user_id)
      setCareers(careers)
      navigate('/recommendations')
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit profile. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="mx-auto max-w-3xl px-6 py-16">
      <p className="mb-3 text-sm font-bold uppercase tracking-[0.16em] text-[#ef7656]">Step 01 / Your starting point</p>
      <h2 className="mb-3 text-4xl font-bold text-slate-900">Let&apos;s map where you are.</h2>
      <p className="mb-8 text-slate-600">
        Add your current skills and interests so we can recommend the best career matches.
      </p>

      <form onSubmit={handleSubmit} className="space-y-8 rounded-3xl border border-slate-900/10 bg-white/80 p-8 shadow-xl shadow-slate-300/20 backdrop-blur sm:p-10">
        <div>
          <label htmlFor="skills" className="mb-2 block text-sm font-semibold text-slate-700">
            Skills
          </label>
          <div className="flex gap-2">
            <input
              id="skills"
              type="text"
              value={skillsInput}
              onChange={(e) => setSkillsInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault()
                  addSkill()
                }
              }}
              placeholder="e.g. Python, SQL, Communication"
              className="flex-1 rounded-xl border border-slate-300 bg-[#fbfcf8] px-4 py-3 outline-none ring-[#ef7656] focus:ring-2"
            />
            <button
              type="button"
              onClick={addSkill}
              className="rounded-xl border border-[#ef7656]/30 bg-[#fff0ea] px-4 py-2.5 font-semibold text-[#c95135] transition hover:bg-[#ffe2d8]"
            >
              Add
            </button>
          </div>
          <p className="mt-2 text-xs text-slate-500">Press Enter or Add. Separate multiple skills with commas.</p>
          <div className="mt-3 flex flex-wrap gap-2">
            {skills.map((skill) => (
              <span
                key={skill}
                className="inline-flex items-center gap-1 rounded-full bg-slate-100 px-3 py-1 text-sm text-slate-700"
              >
                {skill}
                <button
                  type="button"
                  onClick={() => removeSkill(skill)}
                  className="text-slate-400 hover:text-slate-700"
                  aria-label={`Remove ${skill}`}
                >
                  ×
                </button>
              </span>
            ))}
          </div>
        </div>

        <div>
          <label className="mb-2 block text-sm font-semibold text-slate-700">Interests</label>
          <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
            {INTEREST_OPTIONS.map((interest) => {
              const selected = interests.includes(interest)
              return (
                <button
                  key={interest}
                  type="button"
                  onClick={() => toggleInterest(interest)}
                  className={`rounded-lg border px-4 py-2.5 text-left text-sm transition ${
                    selected
                      ? 'border-[#2a9d8f] bg-[#e7f5ef] text-[#176b63]'
                      : 'border-slate-200 bg-white text-slate-700 hover:border-[#2a9d8f]'
                  }`}
                >
                  {interest}
                </button>
              )
            })}
          </div>
        </div>

        {error && (
          <p className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">{error}</p>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-xl bg-[#172033] py-3.5 font-semibold text-white transition hover:bg-[#ef7656] disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? 'Analyzing profile…' : 'Get Recommendations'}
        </button>
      </form>
    </section>
  )
}
