import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import ResumeParse from './pages/ResumeParse'
import ATSScore from './pages/ATSScore'
import Auth from './pages/Auth'
import SkillGap from './pages/SkillGap'

export default function App() {
  return (
    <>
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/auth" element={<Auth />} />
          <Route path="/parse" element={<ResumeParse />} />
          <Route path="/ats" element={<ATSScore />} />
          <Route path="/skills" element={<SkillGap />} />
        </Routes>
      </BrowserRouter>
      <Toaster position="top-right" />
    </>
  )
}
