import { Settings, User, Bell, Shield, Database, Palette } from 'lucide-react'
import Card from '../components/Card'
import Button from '../components/Button'
import LoadingSpinner from '../components/LoadingSpinner'

const SettingsPage = () => {
  const [isExporting, setIsExporting] = useState(false);

  const handleExportData = async () => {
    setIsExporting(true);
    try {
      const response = await fetch('http://127.0.0.1:5000/api/export/data');
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'autopsy_ai_export.json';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Export failed", error);
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Settings</h1>
        <p className="text-slate-500 mt-1">Manage your preferences and configurations</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Settings Navigation */}
        <div className="space-y-2">
          {[
            { icon: User, label: 'Profile' },
            { icon: Bell, label: 'Notifications' },
            { icon: Shield, label: 'Privacy & Security' },
            { icon: Database, label: 'Data Management' },
            { icon: Palette, label: 'Appearance' }
          ].map((item, idx) => {
            const Icon = item.icon
            return (
              <button
                key={idx}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left transition-all ${
                  idx === 0
                    ? 'bg-emerald-50 text-emerald-700 border-l-4 border-emerald-600'
                    : 'text-slate-600 hover:bg-slate-50'
                }`}
              >
                <Icon size={20} />
                <span className="font-medium">{item.label}</span>
              </button>
            )
          })}
        </div>

        {/* Settings Content */}
        <div className="lg:col-span-2 space-y-6">
          <Card className="p-6">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 bg-emerald-100 text-emerald-600 rounded-xl flex items-center justify-center">
                <User size={24} />
              </div>
              <h3 className="text-lg font-semibold text-slate-900">Profile</h3>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Display Name
                </label>
                <input
                  type="text"
                  defaultValue="Autopsy AI User"
                  className="w-full px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Email Address
                </label>
                <input
                  type="email"
                  defaultValue="user@autopsyai.local"
                  className="w-full px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
                />
              </div>

              <div className="flex justify-end pt-4">
                <Button>Save Changes</Button>
              </div>
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 bg-blue-100 text-blue-600 rounded-xl flex items-center justify-center">
                <Shield size={24} />
              </div>
              <h3 className="text-lg font-semibold text-slate-900">Privacy</h3>
            </div>

            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-slate-900">Local Processing Only</p>
                  <p className="text-sm text-slate-500">All data stays on your machine</p>
                </div>
                <div className="w-12 h-6 bg-emerald-600 rounded-full relative cursor-pointer">
                  <div className="w-4 h-4 bg-white rounded-full absolute right-1 top-1"></div>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-slate-900">Analytics</p>
                  <p className="text-sm text-slate-500">Send anonymous usage data</p>
                </div>
                <div className="w-12 h-6 bg-slate-300 rounded-full relative cursor-pointer">
                  <div className="w-4 h-4 bg-white rounded-full absolute left-1 top-1"></div>
                </div>
              </div>
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 bg-purple-100 text-purple-600 rounded-xl flex items-center justify-center">
                <Database size={24} />
              </div>
              <h3 className="text-lg font-semibold text-slate-900">Data Export</h3>
            </div>

            <div className="space-y-4">
              <div>
                <p className="font-medium text-slate-900">Download Autopsy AI Dataset</p>
                <p className="text-sm text-slate-500 mb-4">Export all your personal benchmarks, risks, and trajectories in JSON format.</p>
                <button 
                  onClick={handleExportData}
                  disabled={isExporting}
                  className="bg-purple-600 hover:bg-purple-500 text-white px-4 py-2 rounded transition flex items-center gap-2 font-medium disabled:opacity-50"
                >
                  {isExporting ? 'Exporting...' : 'Export Data'}
                </button>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default SettingsPage
