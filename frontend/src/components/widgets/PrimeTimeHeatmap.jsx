import React from 'react';

const PrimeTimeHeatmap = () => {
  // Hardcoded visual representation of the rolling average prediction model
  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];
  const times = ['Morning', 'Afternoon', 'Evening'];
  
  const intensityMap = {
    'Mon': [80, 40, 20],
    'Tue': [90, 30, 10],
    'Wed': [70, 50, 80],
    'Thu': [60, 60, 40],
    'Fri': [40, 20, 10]
  };

  return (
    <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 h-full">
      <h2 className="text-xl font-bold mb-6 text-white">Weekly Prime Time</h2>
      
      <div className="flex">
        {/* Y Axis */}
        <div className="flex flex-col justify-around mr-4 text-sm text-gray-500 pt-8">
          {times.map(t => <div key={t}>{t}</div>)}
        </div>
        
        {/* Grid */}
        <div className="flex-1 flex justify-between">
          {days.map(day => (
            <div key={day} className="flex flex-col gap-2 items-center w-full">
              <div className="text-sm text-gray-400 mb-2">{day}</div>
              {intensityMap[day].map((val, idx) => {
                let opacity = 'opacity-20';
                if (val > 70) opacity = 'opacity-100';
                else if (val > 40) opacity = 'opacity-60';
                else if (val > 20) opacity = 'opacity-40';
                
                return (
                  <div 
                    key={idx} 
                    className={`w-full aspect-square bg-indigo-500 rounded border border-indigo-700 ${opacity} transition-opacity hover:opacity-100 cursor-pointer`}
                    title={`${day} ${times[idx]}: ${val}% historical focus`}
                  ></div>
                )
              })}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PrimeTimeHeatmap;
