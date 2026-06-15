import { useState } from 'react'
import { Activity, Shield, BarChart3, Upload } from 'lucide-react'

function App() {
  const [file, setFile] = useState(null)

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
  }

  return (
    <div className="min-h-screen w-full bg-slate-900 text-slate-100 p-8">
      <header className="max-w-6xl mx-auto mb-12 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <Activity className="w-8 h-8 text-blue-500" />
          <h1 className="text-2xl font-bold">Autopsy AI</h1>
        </div>
        <nav className="flex gap-6">
          <a href="#" className="hover:text-blue-400 transition-colors">Dashboard</a>
          <a href="#" className="hover:text-blue-400 transition-colors">Privacy</a>
          <a href="#" className="hover:text-blue-400 transition-colors">Settings</a>
        </nav>
      </header>

      <main className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-8">
        <section className="bg-slate-800 p-8 rounded-2xl shadow-xl border border-slate-700">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Shield className="text-green-500" /> Privacy First Analysis
          </h2>
          <p className="text-slate-400 mb-6">
            Upload your digital footprints (browser history, app logs) to uncover behavioral patterns. 
            All processing is done with privacy in mind.
          </p>
          
          <div className="border-2 border-dashed border-slate-600 rounded-xl p-8 text-center hover:border-blue-500 transition-colors cursor-pointer group">
            <input 
              type="file" 
              id="file-upload" 
              className="hidden" 
              onChange={handleFileChange}
            />
            <label htmlFor="file-upload" className="cursor-pointer">
              <Upload className="w-12 h-12 mx-auto mb-4 text-slate-500 group-hover:text-blue-500 transition-colors" />
              <p className="font-medium">
                {file ? file.name : "Click to upload or drag and drop"}
              </p>
              <p className="text-sm text-slate-500 mt-2">CSV, JSON (max 10MB)</p>
            </label>
          </div>
          
          <button 
            disabled={!file}
            className="w-full mt-6 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 text-white font-bold py-3 px-6 rounded-lg transition-colors"
          >
            Start Investigation
          </button>
        </section>

        <section className="bg-slate-800 p-8 rounded-2xl shadow-xl border border-slate-700">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <BarChart3 className="text-blue-500" /> Insights Preview
          </h2>
          <div className="h-64 flex items-center justify-center border border-slate-700 rounded-xl bg-slate-900/50">
            <p className="text-slate-500 italic">No data analyzed yet.</p>
          </div>
          <div className="mt-6 grid grid-cols-2 gap-4">
            <div className="bg-slate-700/50 p-4 rounded-lg border border-slate-600">
              <p className="text-xs text-slate-400 uppercase tracking-wider">Total Events</p>
              <p className="text-2xl font-bold">0</p>
            </div>
            <div className="bg-slate-700/50 p-4 rounded-lg border border-slate-600">
              <p className="text-xs text-slate-400 uppercase tracking-wider">Anomalies</p>
              <p className="text-2xl font-bold">0</p>
            </div>
          </div>
        </section>
      </main>

      <footer className="max-w-6xl mx-auto mt-16 text-center text-slate-500 text-sm">
        &copy; 2026 Autopsy AI. Built with privacy by design.
      </footer>
    </div>
  )
}

export default App
