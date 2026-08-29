import { Link } from 'react-router-dom'

export default function Landing() {
  return (
    <section className="mx-auto grid min-h-[calc(100vh-78px)] max-w-6xl items-center gap-12 px-6 py-16 lg:grid-cols-[1.1fr_0.9fr]">
      <div className="max-w-2xl">
        <span className="mb-6 inline-flex items-center gap-2 rounded-full border border-[#ef7656]/25 bg-[#fff0ea] px-4 py-2 text-sm font-semibold text-[#c95135]">
          <span className="h-2 w-2 rounded-full bg-[#ef7656]" /> AI-powered career guidance
        </span>
        <h1 className="mb-6 text-5xl font-bold leading-[1.05] text-slate-900 sm:text-7xl">
          Your next chapter starts with a <span className="text-[#ef7656]">direction.</span>
      </h1>
        <p className="mb-10 max-w-xl text-lg leading-relaxed text-slate-600">
          Turn the skills you already have into a practical six-month roadmap for work you will care about.
        </p>
        <Link to="/onboard" className="inline-flex rounded-xl bg-[#172033] px-7 py-3.5 text-base font-semibold text-white shadow-lg shadow-slate-300 transition hover:-translate-y-0.5 hover:bg-[#ef7656]">
          Find my path <span className="ml-3">-&gt;</span>
        </Link>
      </div>
      <div className="relative rounded-[2rem] bg-[#173f43] p-8 text-white shadow-2xl shadow-[#173f43]/20 sm:p-10">
        <p className="mb-16 text-sm font-semibold uppercase tracking-[0.18em] text-[#a8d8c8]">A clearer way forward</p>
        <div className="space-y-7">
          <div className="border-l-2 border-[#ef7656] pl-5"><p className="text-sm text-[#a8d8c8]">01 / Know yourself</p><p className="mt-1 text-xl font-semibold">Map your skills and interests</p></div>
          <div className="border-l-2 border-[#f4c95d] pl-5"><p className="text-sm text-[#a8d8c8]">02 / Explore options</p><p className="mt-1 text-xl font-semibold">See roles that fit your profile</p></div>
          <div className="border-l-2 border-[#e8f1e8] pl-5"><p className="text-sm text-[#a8d8c8]">03 / Make it real</p><p className="mt-1 text-xl font-semibold">Build a roadmap you can follow</p></div>
        </div>
        <div className="mt-14 border-t border-white/15 pt-5 text-sm text-[#a8d8c8]">Built around your starting point, not a blank slate.</div>
      </div>
    </section>
  )
}
