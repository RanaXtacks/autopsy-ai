import React from 'react';
import Card from '../Card';

const ScoreCard = ({ title, score, icon: Icon, colorClass }) => {
  return (
    <Card className="p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-slate-500 font-medium">{title}</p>
          <div className="flex items-baseline mt-1">
            <span className="text-3xl font-bold text-slate-900">{score}</span>
            <span className="text-sm text-slate-500 ml-1">/ 100</span>
          </div>
        </div>
        <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${colorClass}`}>
          {Icon && <Icon size={24} />}
        </div>
      </div>
      {/* Mini Progress Bar */}
      <div className="w-full bg-slate-100 h-2 mt-4 rounded-full overflow-hidden">
        <div 
          className="h-full bg-slate-900 transition-all duration-500"
          style={{ width: `${score}%` }}
        ></div>
      </div>
    </Card>
  );
};

export default ScoreCard;
