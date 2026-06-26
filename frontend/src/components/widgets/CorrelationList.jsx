import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

const CorrelationList = ({ title, correlations, type }) => {
  const isPositive = type === 'positive';
  const Icon = isPositive ? TrendingUp : TrendingDown;
  const colorClass = isPositive ? 'text-green-400' : 'text-red-400';
  const borderClass = isPositive ? 'border-green-500/30' : 'border-red-500/30';
  const bgClass = isPositive ? 'bg-green-500/10' : 'bg-red-500/10';

  return (
    <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
      <h2 className={`text-xl font-bold mb-4 flex items-center gap-2 ${colorClass}`}>
        <Icon /> {title}
      </h2>
      <div className="space-y-4">
        {correlations.length === 0 && (
          <p className="text-gray-500 text-sm">No correlations detected in this category.</p>
        )}
        {correlations.map(corr => (
          <div key={corr.id} className={`p-4 rounded-lg border ${borderClass} ${bgClass} transition-colors`}>
            <div className="flex justify-between items-start mb-2">
              <h3 className="font-semibold text-lg text-gray-100">{corr.factor} <span className="text-gray-500">→</span> {corr.outcome}</h3>
              <span className={`text-xs font-bold px-2 py-1 rounded-full ${isPositive ? 'text-green-300 bg-green-900/50' : 'text-red-300 bg-red-900/50'}`}>
                {corr.confidence_score.toFixed(0)}% Confidence
              </span>
            </div>
            <p className="text-sm text-gray-300 mb-2">{corr.explanation}</p>
            <div className="flex gap-2">
                <span className="text-xs bg-gray-900 text-gray-400 px-2 py-1 rounded">
                    r = {corr.correlation_strength.toFixed(2)}
                </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CorrelationList;
