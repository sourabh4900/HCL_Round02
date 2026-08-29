import { useNavigate } from 'react-router-dom'

export default function Recommendations({ userId, careers, setSelectedCareer }) {
  const navigate = useNavigate()

  const handleViewPath = (career) => {
    setSelectedCareer(career)
    navigate('/path')
  }

  if (!userId || !careers?.length) {
    return (
      <section className="mx-auto max-w-3xl px-6 py-16 text-center">
        <p className="mb-4 text-slate-600">No recommendations yet. Complete onboarding first.</p>
        <button
          type="button"
          onClick={() => navigate('/onboard')}
          className="rounded-lg bg-indigo-600 px-5 py-2.5 font-medium text-white hover:bg-indigo-700"
        >
          Go to Onboarding
        </button>
      </section>
    )
  }

  return (
    <section className="mx-auto max-w-6xl px-6 py-16">
      <div className="mb-8">
        <p className="mb-3 text-sm font-bold uppercase tracking-[0.16em] text-[#ef7656]">Step 02 / Explore</p>
        <h2 className="text-4xl font-bold text-slate-900">Roles worth exploring.</h2>
        <p className="mt-2 text-slate-600">
          Based on your skills and interests, these roles are the closest fit.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {careers.map((career) => {
          const matchPercent = Math.round(career.similarity_score * 100)
          return (
            <article
              key={career.role}
              className="flex flex-col rounded-3xl border border-slate-900/10 bg-white/85 p-7 shadow-lg shadow-slate-300/15 transition hover:-translate-y-1 hover:shadow-xl"
            >
              <div className="mb-4 flex items-start justify-between gap-4">
                <h3 className="text-xl font-semibold text-slate-900">{career.role}</h3>
                <span className="rounded-full bg-[#e7f5ef] px-3 py-1 text-sm font-semibold text-[#176b63]">
                  {matchPercent}% match
                </span>
              </div>
              <p className="mb-4 flex-1 text-sm leading-relaxed text-slate-600 line-clamp-4">
                {career.description}
              </p>
              <p className="mb-5 text-xs text-slate-500">
                Key skills: {career.required_skills.split(',').slice(0, 6).join(', ')}…
              </p>
              <button
                type="button"
                onClick={() => handleViewPath(career)}
                className="rounded-xl bg-[#172033] px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-[#ef7656]"
              >
                View Path
              </button>
            </article>
          )
        })}
      </div>
    </section>
  )
}
