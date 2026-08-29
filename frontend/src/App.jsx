import { useState } from 'react'
import { BrowserRouter, Link, Route, Routes } from 'react-router-dom'
import Landing from './components/Landing'
import Onboarding from './components/Onboarding'
import PathView from './components/PathView'
import Recommendations from './components/Recommendations'

function AppShell({ children }) {
  return (
    <div className="min-h-screen">
      <header className="border-b border-slate-900/10 bg-[#f6f7f2]/85 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
          <Link to="/" className="flex items-center gap-3 text-lg font-bold text-slate-900">
            <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#ef7656] text-sm text-white shadow-sm">P</span>
            <span>PathFinder<span className="text-[#ef7656]">.</span></span>
          </Link>
          <nav className="flex gap-5 text-sm font-semibold text-slate-600">
            <Link to="/onboard" className="transition hover:text-[#ef7656]">
              Onboard
            </Link>
            <Link to="/recommendations" className="transition hover:text-[#ef7656]">
              Recommendations
            </Link>
          </nav>
        </div>
      </header>
      <main>{children}</main>
    </div>
  )
}

export default function App() {
  const [userId, setUserId] = useState('')
  const [careers, setCareers] = useState([])
  const [selectedCareer, setSelectedCareer] = useState(null)

  return (
    <BrowserRouter>
      <AppShell>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route
            path="/onboard"
            element={
              <Onboarding setUserId={setUserId} setCareers={setCareers} />
            }
          />
          <Route
            path="/recommendations"
            element={
              <Recommendations
                userId={userId}
                careers={careers}
                setSelectedCareer={setSelectedCareer}
              />
            }
          />
          <Route
            path="/path"
            element={
              <PathView userId={userId} selectedCareer={selectedCareer} />
            }
          />
        </Routes>
      </AppShell>
    </BrowserRouter>
  )
}
