import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const ForecastGraph = ({ predictions }) => {
  // Map predictions to a rough hourly timeline for visual flair
  const data = [
    { time: '08:00', focus: 30 },
    { time: '10:00', focus: 90 },
    { time: '12:00', focus: 60 },
    { time: '14:00', focus: 20 },
    { time: '16:00', focus: 75 },
    { time: '18:00', focus: 40 },
    { time: '20:00', focus: 20 }
  ];

  return (
    <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 h-full flex flex-col">
      <h2 className="text-xl font-bold mb-6 text-white">Focus Trajectory</h2>
      <div className="flex-1 min-h-[250px]">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 5, right: 5, left: -20, bottom: 5 }}>
            <defs>
              <linearGradient id="colorFocus" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#818CF8" stopOpacity={0.8}/>
                <stop offset="95%" stopColor="#818CF8" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" vertical={false} />
            <XAxis dataKey="time" stroke="#9CA3AF" tick={{ fill: '#9CA3AF', fontSize: 12 }} />
            <YAxis stroke="#9CA3AF" tick={{ fill: '#9CA3AF', fontSize: 12 }} />
            <Tooltip 
              contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151', borderRadius: '0.5rem' }}
              itemStyle={{ color: '#818CF8' }}
            />
            <Area type="monotone" dataKey="focus" stroke="#818CF8" strokeWidth={3} fillOpacity={1} fill="url(#colorFocus)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default ForecastGraph;
