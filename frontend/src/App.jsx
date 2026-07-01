import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import { IntelligenceProvider } from './context/IntelligenceContext'
import Dashboard from './pages/Dashboard'
import Upload from './pages/Upload'
import Reports from './pages/Reports'
import Settings from './pages/Settings'
import Sessions from './pages/Sessions'
import Productivity from './pages/Productivity'
import Habits from './pages/Habits'
import Correlations from './pages/Correlations'
import Procrastination from './pages/Procrastination'
import Burnout from './pages/Burnout'

function App() {
  return (
    <IntelligenceProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Dashboard />} />
            <Route path="/upload" element={<Upload />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/sessions" element={<Sessions />} />
            <Route path="/productivity" element={<Productivity />} />
            <Route path="/habits" element={<Habits />} />
            <Route path="/correlations" element={<Correlations />} />
            <Route path="/procrastination" element={<Procrastination />} />
            <Route path="/burnout" element={<Burnout />} />
          </Route>
        </Routes>
      </Router>
    </IntelligenceProvider>
  )
}

export default App
