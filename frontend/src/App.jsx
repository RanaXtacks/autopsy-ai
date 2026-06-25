import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Upload from './pages/Upload'
import Reports from './pages/Reports'
import Settings from './pages/Settings'
import Sessions from './pages/Sessions'
import Productivity from './pages/Productivity'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/sessions" element={<Sessions />} />
          <Route path="/productivity" element={<Productivity />} />
        </Route>
      </Routes>
    </Router>
  )
}

export default App
