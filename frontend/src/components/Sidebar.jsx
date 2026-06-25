import { NavLink } from 'react-router-dom'
import { 
  Home, 
  Upload, 
  FileText, 
  Settings, 
  Shield, 
  Brain,
  Menu,
  X,
  Clock,
  Activity
} from 'lucide-react'
import { useState } from 'react'

const Sidebar = () => {
  const [isOpen, setIsOpen] = useState(false)

  const navItems = [
    { 
      path: '/', 
      label: 'Dashboard', 
      icon: Home 
    },
    { 
      path: '/upload', 
      label: 'Upload Data', 
      icon: Upload 
    },
    { 
      path: '/sessions', 
      label: 'Sessions', 
      icon: Clock 
    },
    { 
      path: '/productivity', 
      label: 'Productivity', 
      icon: Activity 
    },
    { 
      path: '/reports', 
      label: 'Reports', 
      icon: FileText 
    },
    { 
      path: '/settings', 
      label: 'Settings', 
      icon: Settings 
    }
  ]

  return (
    <>
      {/* Mobile Menu Toggle */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="md:hidden fixed top-4 left-4 z-50 p-2 bg-white rounded-lg shadow-lg"
      >
        {isOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      {/* Sidebar Overlay (mobile) */}
      {isOpen && (
        <div
          className="md:hidden fixed inset-0 bg-black/50 z-40"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside className={`
        fixed top-0 left-0 h-full bg-slate-900 text-white z-40
        transition-all duration-300 ease-in-out
        ${isOpen ? 'w-64 translate-x-0' : 'w-64 -translate-x-full md:translate-x-0 md:w-64'}
      `}>
        {/* Logo */}
        <div className="p-6 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-emerald-400 to-cyan-500 rounded-xl flex items-center justify-center">
              <Brain className="text-white" size={24} />
            </div>
            <div>
              <h1 className="font-bold text-lg">Autopsy AI</h1>
              <p className="text-xs text-slate-400">Privacy-First</p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="p-4 space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon
            return (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={() => setIsOpen(false)}
                className={({ isActive }) => `
                  flex items-center gap-3 px-4 py-3 rounded-lg transition-all
                  ${isActive 
                    ? 'bg-slate-800 text-emerald-400 border-l-4 border-emerald-400' 
                    : 'text-slate-300 hover:bg-slate-800 hover:text-white'}
                `}
              >
                <Icon size={20} />
                <span className="font-medium">{item.label}</span>
              </NavLink>
            )
          })}
        </nav>

        {/* Footer */}
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-slate-800">
          <div className="flex items-center gap-3 p-3 bg-slate-800/50 rounded-lg">
            <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center">
              <Shield size={20} />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium truncate">Secure Mode</p>
              <p className="text-xs text-slate-400 truncate">Data stays local</p>
            </div>
          </div>
        </div>
      </aside>
    </>
  )
}

export default Sidebar
