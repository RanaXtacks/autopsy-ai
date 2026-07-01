import React from 'react';
import { useIntelligence } from '../context/IntelligenceContext';
import { Target, Activity, CheckCircle, AlertTriangle, XCircle } from 'lucide-react';

const MacroDashboard = () => {
  const { globalState, loading: contextLoading } = useIntelligence();

  // Map trajectory from global state or fallback to null
  const trajectory = globalState?.trajectory || null;

  if (contextLoading) return <div className="text-white p-6">Analyzing macro trajectories...</div>;

  return (
    <div className="p-6 text-white space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-600">
            Macro Intelligence
          </h1>
          <p className="text-gray-400 mt-2">Unified trajectory and goal engine.</p>
        </div>
      </div>
      
      {trajectory && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 flex flex-col justify-center">
             <div className="flex items-center justify-between mb-4">
                 <h3 className="text-gray-400 text-sm uppercase tracking-wider flex items-center gap-2">
                    <Target size={16}/> Target Goal
                 </h3>
                 <span className="bg-yellow-900/50 text-yellow-500 text-xs px-2 py-1 rounded-full border border-yellow-700/50">
                    {trajectory.status}
                 </span>
             </div>
             <span className="text-2xl font-bold text-white">{trajectory.goal}</span>
             <p className="text-gray-500 mt-2">Projected Completion: <span className="text-red-400">{trajectory.projected}</span></p>
          </div>

          <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
             <h3 className="text-gray-400 text-sm uppercase tracking-wider mb-4 flex items-center gap-2">
                <Activity size={16}/> 30-Day Trend Shifts
             </h3>
             <div className="flex items-start gap-3 p-3 bg-red-900/20 rounded-lg border border-red-900/50">
                <AlertTriangle className="text-red-400 mt-1 shrink-0" size={18} />
                <div>
                   <p className="text-red-200 text-sm">{trajectory.trendDetected}</p>
                </div>
             </div>
          </div>
          
          <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 md:col-span-2">
             <h3 className="text-gray-400 text-sm uppercase tracking-wider mb-4 flex items-center gap-2">
                <CheckCircle size={16}/> AI Course Correction
             </h3>
             <p className="text-blue-300 text-lg font-medium">{trajectory.courseCorrection}</p>
          </div>
          
          <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 md:col-span-2">
             <h3 className="text-gray-400 text-sm uppercase tracking-wider mb-4">Consistency Survival</h3>
             <div className="w-full bg-gray-700 rounded-full h-4 mb-2">
               <div className="bg-gradient-to-r from-green-400 to-emerald-600 h-4 rounded-full" style={{ width: `${trajectory.consistencyProb}%` }}></div>
             </div>
             <p className="text-right text-sm text-gray-400">{trajectory.consistencyProb}% probability of maintaining current streak</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default MacroDashboard;
