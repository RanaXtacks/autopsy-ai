import React, { useState, useEffect } from 'react';
import { User, Activity, AlertOctagon, TrendingUp, Cpu } from 'lucide-react';

const MasterDashboard = () => {
  const [state, setState] = useState(null);
  const [loading, setLoading] = useState(true);

  // Mocking the God-Endpoint fetch
  const fetchUnifiedState = async () => {
    try {
      setTimeout(() => {
        setState({
          archetype: {
            primary: "Deep Worker",
            secondary: "Night Owl",
            riskProfile: "High Context Switcher"
          },
          segmentation: "Your current 7-day behavior closely matches your 'Finals Week Overload' segment from last semester.",
          burnoutRisk: 75,
          focusAvg: 82,
          trajectoryStatus: "At Risk",
          prescriptions: [
            "Re-establish 9 AM coding block to recover 3 hours."
          ]
        });
        setLoading(false);
      }, 800);
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUnifiedState();
  }, []);

  if (loading) return <div className="text-white p-6">Loading MVP Master State...</div>;

  return (
    <div className="p-6 text-white space-y-6">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-4xl font-black bg-clip-text text-transparent bg-gradient-to-r from-yellow-400 to-orange-500 flex items-center gap-3">
            <Cpu className="text-orange-500" size={32} />
            Autopsy AI <span className="text-gray-500 text-2xl font-normal ml-2">MVP v1.0</span>
          </h1>
          <p className="text-gray-400 mt-2">Unified Behavioral Intelligence State</p>
        </div>
      </div>
      
      {state && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          {/* User Archetype Badge */}
          <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 md:col-span-1 shadow-lg shadow-orange-900/10">
             <div className="flex items-center justify-between mb-6">
                 <h3 className="text-gray-400 text-sm uppercase tracking-wider font-semibold">User Archetype</h3>
                 <User className="text-orange-400" size={20} />
             </div>
             
             <div className="space-y-4">
                 <div>
                    <p className="text-xs text-gray-500 uppercase">Primary</p>
                    <p className="text-2xl font-bold text-white">{state.archetype.primary}</p>
                 </div>
                 <div>
                    <p className="text-xs text-gray-500 uppercase">Secondary</p>
                    <p className="text-lg font-medium text-purple-400">{state.archetype.secondary}</p>
                 </div>
                 <div className="pt-2 border-t border-gray-700">
                    <p className="text-xs text-gray-500 uppercase">Risk Profile</p>
                    <p className="text-sm font-medium text-red-400">{state.archetype.riskProfile}</p>
                 </div>
             </div>
          </div>

          {/* Unified State Summary */}
          <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 md:col-span-2 space-y-6">
             <div className="grid grid-cols-3 gap-4 border-b border-gray-700 pb-6">
                 <div>
                     <h3 className="text-gray-400 text-xs uppercase tracking-wider mb-1 flex items-center gap-1"><Activity size={14}/> Focus</h3>
                     <span className="text-3xl font-bold text-white">{state.focusAvg}</span><span className="text-gray-500 text-sm">/100</span>
                 </div>
                 <div>
                     <h3 className="text-gray-400 text-xs uppercase tracking-wider mb-1 flex items-center gap-1"><AlertOctagon size={14}/> Burnout Risk</h3>
                     <span className="text-3xl font-bold text-red-400">{state.burnoutRisk}%</span>
                 </div>
                 <div>
                     <h3 className="text-gray-400 text-xs uppercase tracking-wider mb-1 flex items-center gap-1"><TrendingUp size={14}/> Trajectory</h3>
                     <span className="text-xl font-bold text-yellow-400">{state.trajectoryStatus}</span>
                 </div>
             </div>
             
             <div>
                 <h3 className="text-gray-400 text-xs uppercase tracking-wider mb-2">Behavior Segmentation</h3>
                 <p className="text-blue-200 bg-blue-900/30 p-4 rounded-lg border border-blue-800/50">
                    {state.segmentation}
                 </p>
             </div>
             
             <div>
                 <h3 className="text-gray-400 text-xs uppercase tracking-wider mb-2">AI Prescriptions</h3>
                 <ul className="space-y-2">
                     {state.prescriptions.map((p, idx) => (
                         <li key={idx} className="flex items-center gap-2 text-emerald-300 bg-emerald-900/20 p-3 rounded-lg border border-emerald-800/30">
                            <span className="h-2 w-2 bg-emerald-400 rounded-full"></span>
                            {p}
                         </li>
                     ))}
                 </ul>
             </div>
          </div>
          
        </div>
      )}
    </div>
  );
};

export default MasterDashboard;
