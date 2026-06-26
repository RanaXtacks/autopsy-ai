import React from 'react';
import { Radar } from 'lucide-react';

const TrendRadar = ({ correlations }) => {
  // Placeholder for an interactive radar or network graph
  return (
    <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
      <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
        <Radar className="text-orange-400" /> Strongest Behavioral Trends
      </h2>
      <p className="text-sm text-gray-400 mb-6">Visual mapping of the most statistically significant behaviors affecting your productivity.</p>
      
      <div className="flex flex-wrap gap-4 justify-center py-8">
        {correlations.length === 0 && (
            <p className="text-gray-500">Not enough data to map trends.</p>
        )}
        {correlations.map((corr, idx) => {
            // Visualize size based on confidence score
            const size = Math.max(60, corr.confidence_score * 1.5);
            const isPositive = corr.correlation_strength > 0;
            return (
                <div 
                    key={corr.id} 
                    className={`flex items-center justify-center rounded-full border-2 
                        ${isPositive ? 'border-green-500 bg-green-500/20' : 'border-red-500 bg-red-500/20'}
                        hover:scale-110 transition-transform cursor-help shadow-lg`}
                    style={{ width: `${size}px`, height: `${size}px` }}
                    title={`${corr.factor} -> ${corr.outcome}\nStrength: ${corr.correlation_strength.toFixed(2)}`}
                >
                    <span className="text-[10px] text-center font-bold px-2 text-white line-clamp-2">
                        {corr.factor}
                    </span>
                </div>
            );
        })}
      </div>
      <div className="mt-4 flex justify-center gap-4 text-xs text-gray-400">
          <div className="flex items-center gap-1"><div className="w-3 h-3 bg-green-500/20 border border-green-500 rounded"></div> Positive Outcome</div>
          <div className="flex items-center gap-1"><div className="w-3 h-3 bg-red-500/20 border border-red-500 rounded"></div> Negative Outcome</div>
          <div className="flex items-center gap-1 ml-4">Size = Confidence Score</div>
      </div>
    </div>
  );
};

export default TrendRadar;
