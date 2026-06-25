import React from 'react';
import { Lightbulb } from 'lucide-react';

const InsightsList = ({ insights }) => {
  if (!insights || insights.length === 0) {
    return <p className="text-sm text-slate-500">No new insights available today.</p>;
  }

  return (
    <div className="space-y-4">
      {insights.map((insight, idx) => (
        <div key={idx} className="flex items-start gap-3 p-4 bg-indigo-50/50 border border-indigo-100 rounded-xl">
          <div className="mt-0.5">
            <Lightbulb size={20} className="text-indigo-600" />
          </div>
          <p className="text-sm text-slate-700 leading-relaxed">{insight}</p>
        </div>
      ))}
    </div>
  );
};

export default InsightsList;
