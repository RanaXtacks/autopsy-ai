import { useState } from 'react'
import axios from 'axios'
import { Upload, FileText, CheckCircle, AlertCircle } from 'lucide-react'
import Card from '../components/Card'
import Button from '../components/Button'
import FileUpload from '../components/FileUpload'

const UploadPage = () => {
  const [files, setFiles] = useState([])
  const [isProcessing, setIsProcessing] = useState(false)
  const [uploadStatus, setUploadStatus] = useState(null)

  const handleFileSelect = (selectedFiles) => {
    setFiles(selectedFiles)
    setUploadStatus(null)
  }

  const handleUpload = async () => {
    if (files.length === 0) return
    
    setIsProcessing(true)
    setUploadStatus(null)

    try {
      const formData = new FormData();
      files.forEach((file) => {
        formData.append("file", file); // Backend expects "file"
      });

      const token = localStorage.getItem('token');
      const headers = { 
        'Content-Type': 'multipart/form-data',
        ...(token && { 'Authorization': `Bearer ${token}` })
      };

      const res = await axios.post('/api/v1/data/upload', formData, { headers });
      
      setIsProcessing(false)
      setUploadStatus('success')
      
      // Refresh global state so dashboard picks up new data
      setTimeout(() => {
        window.location.reload();
      }, 1000);
      
    } catch (err) {
      console.error(err);
      setIsProcessing(false);
      setUploadStatus('error');
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Upload Data</h1>
        <p className="text-slate-500 mt-1">Upload your datasets for analysis</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Upload Area */}
        <div className="lg:col-span-2">
          <Card className="p-6">
            <h3 className="text-lg font-semibold text-slate-900 mb-4">Select Files</h3>
            <FileUpload
              accept=".csv,.json,.xlsx,.xls"
              multiple
              onFileSelect={handleFileSelect}
            />
            
            {uploadStatus === 'success' && (
              <div className="mt-6 p-4 bg-emerald-50 border border-emerald-200 rounded-lg flex items-center gap-3">
                <CheckCircle className="text-emerald-600" size={24} />
                <div>
                  <p className="font-medium text-emerald-800">Upload Successful!</p>
                  <p className="text-sm text-emerald-700">Your files are ready for analysis</p>
                </div>
              </div>
            )}

            {uploadStatus === 'error' && (
              <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center gap-3">
                <AlertCircle className="text-red-600" size={24} />
                <div>
                  <p className="font-medium text-red-800">Upload Failed</p>
                  <p className="text-sm text-red-700">Please try again later</p>
                </div>
              </div>
            )}

            {files.length > 0 && (
              <div className="mt-6 flex gap-3">
                <Button
                  onClick={handleUpload}
                  disabled={isProcessing}
                  className="flex-1"
                >
                  {isProcessing ? (
                    <>
                      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                      Processing...
                    </>
                  ) : (
                    <>
                      <Upload size={20} className="mr-2" />
                      Upload & Analyze
                    </>
                  )}
                </Button>
                <Button
                  variant="outline"
                  onClick={() => {
                    setFiles([])
                    setUploadStatus(null)
                  }}
                >
                  Clear
                </Button>
              </div>
            )}
          </Card>
        </div>

        {/* Sidebar Info */}
        <div className="space-y-6">
          <Card className="p-6">
            <h3 className="text-lg font-semibold text-slate-900 mb-4">Supported Formats</h3>
            <ul className="space-y-3">
              {['CSV (.csv)', 'JSON (.json)', 'Excel (.xlsx, .xls)'].map((format, idx) => (
                <li key={idx} className="flex items-center gap-3 text-slate-600">
                  <div className="w-8 h-8 bg-slate-100 rounded-lg flex items-center justify-center">
                    <FileText size={16} className="text-slate-500" />
                  </div>
                  <span>{format}</span>
                </li>
              ))}
            </ul>
          </Card>

          <Card className="p-6">
            <h3 className="text-lg font-semibold text-slate-900 mb-4">Processing Info</h3>
            <div className="space-y-3 text-sm text-slate-600">
              <p className="flex items-start gap-2">
                <span className="text-emerald-600 mt-0.5">•</span>
                All processing happens locally
              </p>
              <p className="flex items-start gap-2">
                <span className="text-emerald-600 mt-0.5">•</span>
                No data leaves your machine
              </p>
              <p className="flex items-start gap-2">
                <span className="text-emerald-600 mt-0.5">•</span>
                Max file size: 100MB
              </p>
            </div>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default UploadPage
