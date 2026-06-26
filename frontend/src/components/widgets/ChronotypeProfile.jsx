import React from 'react';
import { Sun } from 'lucide-react';

const ChronotypeProfile = ({ chronotype }) => {
  const profileName = chronotype || "Analyzing...";
  
  return (
    <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 h-full flex flex-col items-center text-center justify-center">
      <h2 className="text-xl font-bold mb-4 text-white self-start w-full text-left">Chronotype</h2>
      
      <div className="w-24 h-24 rounded-full bg-gradient-to-br from-yellow-400 to-orange-500 flex items-center justify-center mb-4 shadow-[0_0_20px_rgba(251,191,36,0.3)]">
        <Sun size={40} className="text-white" />
      </div>
      
      <h3 className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-yellow-300 to-orange-400">
        {profileName}
      </h3>
      <p className="text-gray-400 text-sm mt-3">
        Based on historical deep work distribution and behavioral patterns.
      </p>
    </div>
  );
};

export default ChronotypeProfile;
