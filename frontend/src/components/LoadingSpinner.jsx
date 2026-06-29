import React from 'react';

const LoadingSpinner = ({ message = "Analyzing behavioral ecosystems..." }) => {
  return (
    <div className="flex flex-col items-center justify-center p-12 w-full h-full min-h-[300px]">
      <div className="relative w-16 h-16 mb-6">
        <div className="absolute inset-0 border-4 border-gray-700 rounded-full"></div>
        <div className="absolute inset-0 border-4 border-emerald-500 rounded-full border-t-transparent animate-spin"></div>
      </div>
      <p className="text-gray-400 font-medium animate-pulse">{message}</p>
    </div>
  );
};

export default LoadingSpinner;
