import React from 'react';
import { Clock } from 'lucide-react';

const TomorrowSchedule = ({ predictions }) => {
  return (
    <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 h-full">
      <h2 className="text-xl font-bold mb-6 text-white flex items-center gap-2">
        <Clock className="text-indigo-400" /> Tomorrow's Focus Forecast
      </h2>
      
      <div className="space-y-4">
        {predictions.map((p, idx) => {
          const startTime = new Date(p.optimal_start_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
          const endTime = new Date(p.optimal_end_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
          
          const isDip = p.activity_type.includes("Dip");
          const bgClass = isDip ? "bg-red-900/20 border-red-500/30" : "bg-indigo-900/20 border-indigo-500/30";
          const textClass = isDip ? "text-red-400" : "text-indigo-400";
          const title = isDip ? "Energy Dip" : p.activity_type;

          return (
            <div key={idx} className={`p-4 border rounded-lg flex flex-col sm:flex-row sm:items-center justify-between gap-4 ${bgClass}`}>
               <div>
                 <h3 className={`font-bold ${textClass}`}>{title}</h3>
                 <p className="text-gray-300 text-sm mt-1">{startTime} - {endTime}</p>
               </div>
               <div className="text-right">
                 <p className="text-xs text-gray-500">Confidence</p>
                 <p className="text-lg font-black text-gray-200">{p.confidence_score.toFixed(0)}%</p>
               </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default TomorrowSchedule;
