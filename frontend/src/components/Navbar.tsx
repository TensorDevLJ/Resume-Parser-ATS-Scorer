import { Link } from 'react-router-dom'
import { FileText, Zap, Target, TrendingUp } from 'lucide-react'

export default function Navbar() {
  return (
    <nav className="bg-white shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center gap-2 font-bold text-xl text-blue-600">
            <FileText size={28} />
            Resume Parser
          </Link>
          
          <div className="flex gap-8 items-center">
            <Link to="/parse" className="flex items-center gap-2 hover:text-blue-600 transition">
              <FileText size={20} /> Parse
            </Link>
            <Link to="/ats" className="flex items-center gap-2 hover:text-blue-600 transition">
              <Zap size={20} /> ATS Score
            </Link>
            <Link to="/skills" className="flex items-center gap-2 hover:text-blue-600 transition">
              <Target size={20} /> Skills
            </Link>
            <Link to="/auth" className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition">
              Login
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}
