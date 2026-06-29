import React, { useState, useEffect } from 'react';
import { Calendar, TrendingUp, TrendingDown, Clock, AlertCircle } from 'lucide-react';

const ReportingDashboard = () => {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);

  // Mocking the fetch for presentation purposes
  const fetchDashboardData = async () => {
    try {
      // Simulate API call
      setTimeout(() => {
        setReport({
          period: "June 22 - June 28, 2026",
          focusAvg: 78,
          focusDelta: "+4%",
          lostTime: 4.2,
          lostTimeDelta: "-12%",
          baselineShift: "Your focus threshold is stabilizing 1.2 points higher than your Q1 baseline.",
          topDistraction: "Procrastination"
        });
        setLoading(false);
      }, 800);
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  if (loading) return <div className="text-white p-6">Compiling period intelligence...</div>;

  return (
    <div className="p-6 text-white space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-cyan-500">
            Intelligence Reporting
          </h1>
          <p className="text-gray-400 mt-2">Periodic comparative analytics and baseline shifts.</p>
        </div>
        <div className="flex items-center gap-2 bg-gray-800 px-4 py-2 rounded-lg border border-gray-700">
          <Calendar size={18} className="text-cyan-400" />
          <span className="font-medium">{report.period}</span>
        </div>
      </div>
      
      {report && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          
          {/* Focus Metrics */}
          <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
             <h3 className="text-gray-400 text-sm uppercase tracking-wider flex items-center gap-2 mb-4">
                <TrendingUp size={16}/> Focus Average
             </h3>
             <div className="flex items-end gap-4">
                <span className="text-5xl font-bold text-white">{report.focusAvg}</span>
                <span className="text-gray-500 text-xl mb-1">/100</span>
                <div className="flex items-center gap-1 text-emerald-400 bg-emerald-900/30 px-2 py-1 rounded-full text-sm mb-2">
                   <TrendingUp size={14} /> {report.focusDelta} vs last week
                </div>
             </div>
          </div>

          {/* Lost Time Metrics */}
          <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
             <h3 className="text-gray-400 text-sm uppercase tracking-wider flex items-center gap-2 mb-4">
                <Clock size={16}/> Lost Time
             </h3>
             <div className="flex items-end gap-4">
                <span className="text-5xl font-bold text-red-400">{report.lostTime}h</span>
                <span className="text-gray-500 text-sm mb-2">to {report.topDistraction}</span>
                <div className="flex items-center gap-1 text-emerald-400 bg-emerald-900/30 px-2 py-1 rounded-full text-sm mb-2">
                   <TrendingDown size={14} /> {report.lostTimeDelta} vs last week
                </div>
             </div>
          </div>
          
          {/* Baseline Shift */}
          <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 md:col-span-2">
             <h3 className="text-gray-400 text-sm uppercase tracking-wider mb-4 flex items-center gap-2">
                <AlertCircle size={16}/> Baseline Shift Analysis
             </h3>
             <div className="flex items-center gap-4 p-4 bg-cyan-900/20 rounded-lg border border-cyan-900/50">
                <div className="h-10 w-10 rounded-full bg-cyan-900/50 flex items-center justify-center shrink-0">
                  <TrendingUp className="text-cyan-400" size={20} />
                </div>
                <p className="text-cyan-100 text-lg">{report.baselineShift}</p>
             </div>
          </div>
          
        </div>
      )}
    </div>
  );
};

export default ReportingDashboard;
