import { 
  FileText, 
  Download, 
  Eye, 
  Trash2, 
  Search,
  Filter,
  Calendar,
  ChevronDown
} from 'lucide-react'
import Card from '../components/Card'
import Button from '../components/Button'
import { useState } from 'react'
import { useIntelligence } from '../context/IntelligenceContext'

const Reports = () => {
  const { globalState } = useIntelligence();
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedStatus, setSelectedStatus] = useState('All')

  const reports = globalState?.reports || [
    { 
      id: 1, 
      name: 'User Behavior Analysis Q2', 
      date: '2024-06-15', 
      status: 'Completed',
      fileSize: '2.4 MB',
      type: 'Behavioral'
    },
    { 
      id: 2, 
      name: 'Engagement Metrics Dashboard', 
      date: '2024-06-14', 
      status: 'Processing',
      fileSize: '1.8 MB',
      type: 'Engagement'
    },
    { 
      id: 3, 
      name: 'Retention Study Report', 
      date: '2024-06-12', 
      status: 'Completed',
      fileSize: '3.1 MB',
      type: 'Retention'
    },
    { 
      id: 4, 
      name: 'Conversion Funnel Analysis', 
      date: '2024-06-10', 
      status: 'Completed',
      fileSize: '1.2 MB',
      type: 'Conversion'
    },
    { 
      id: 5, 
      name: 'User Segmentation', 
      date: '2024-06-08', 
      status: 'Failed',
      fileSize: '0.5 MB',
      type: 'Segmentation'
    }
  ]

  const statusColors = {
    Completed: 'bg-emerald-100 text-emerald-700',
    Processing: 'bg-yellow-100 text-yellow-700',
    Failed: 'bg-red-100 text-red-700'
  }

  const filteredReports = reports.filter(report => {
    const matchesSearch = report.name.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesStatus = selectedStatus === 'All' || report.status === selectedStatus
    return matchesSearch && matchesStatus
  })

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Reports</h1>
          <p className="text-slate-500 mt-1">View and manage your analysis reports</p>
        </div>
      </div>

      {/* Filters */}
      <Card className="p-4">
        <div className="flex flex-col md:flex-row gap-4">
          {/* Search */}
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
            <input
              type="text"
              placeholder="Search reports..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
            />
          </div>

          {/* Status Filter */}
          <div className="relative">
            <Button variant="outline" className="w-full md:w-auto">
              <Filter size={18} className="mr-2" />
              {selectedStatus}
              <ChevronDown size={16} className="ml-2" />
            </Button>
          </div>
        </div>
      </Card>

      {/* Reports List */}
      <div className="space-y-4">
        {filteredReports.map((report) => (
          <Card key={report.id} className="p-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 bg-slate-100 text-slate-600 rounded-xl flex items-center justify-center shrink-0">
                  <FileText size={24} />
                </div>
                <div className="min-w-0">
                  <h3 className="text-lg font-semibold text-slate-900 truncate">{report.name}</h3>
                  <div className="flex items-center gap-4 mt-2 text-sm text-slate-500">
                    <span className="flex items-center gap-1">
                      <Calendar size={16} />
                      {report.date}
                    </span>
                    <span>•</span>
                    <span>{report.type}</span>
                    <span>•</span>
                    <span>{report.fileSize}</span>
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <span className={`px-3 py-1 text-xs font-medium rounded-full ${statusColors[report.status]}`}>
                  {report.status}
                </span>
                <div className="flex items-center gap-2">
                  {report.status === 'Completed' && (
                    <>
                      <Button variant="outline" size="sm" onClick={() => alert('View report feature coming soon.')}>
                        <Eye size={16} className="mr-1" />
                        View
                      </Button>
                      <Button variant="outline" size="sm" onClick={() => alert('Download report feature coming soon.')}>
                        <Download size={16} className="mr-1" />
                        Download
                      </Button>
                    </>
                  )}
                  <Button variant="outline" size="sm" onClick={() => alert('Delete report feature coming soon.')} className="text-red-600 hover:text-red-700 hover:bg-red-50 border-red-200">
                    <Trash2 size={16} />
                  </Button>
                </div>
              </div>
            </div>
          </Card>
        ))}

        {filteredReports.length === 0 && (
          <Card className="p-12 text-center">
            <FileText size={48} className="mx-auto text-slate-300" />
            <h3 className="mt-4 text-lg font-medium text-slate-900">No reports found</h3>
            <p className="text-slate-500 mt-2">Try adjusting your search or filters</p>
          </Card>
        )}
      </div>
    </div>
  )
}

export default Reports
