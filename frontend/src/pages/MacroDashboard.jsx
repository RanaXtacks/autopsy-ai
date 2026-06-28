import React, { useState, useEffect } from 'react';
import { Line, Bar } from 'react-chartjs-2';

const MacroDashboard = () => {
  const [trajectoryData, setTrajectoryData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setTimeout(() => {
      setTrajectoryData({
        goal: { goal_type: "Weekly Deep Work", target_value: 15.0, status: "active" },
        forecast: { projected_final_value: 12.0, status: "At Risk", deficit: 3.0 },
        consistency: { survival_probability: 0.85, high_risk_day: "Saturday", forecast_message: "85% probability of maintaining current streak based on historical drop-offs." },
        trend_detected: "Chronotype Shift: Morning focus dropping, shifting to low-quality evening work.",
        course_correction: "Re-establish 9 AM coding block to recover 3.0 hours."
      });
      setLoading(false);
    }, 1000);
  }, []);

  if (loading) return <div className="p-8 text-center text-gray-400">Loading Macro Intelligence...</div>;

  return (
    <div className="p-6 bg-gray-900 min-h-screen text-gray-100">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">Macro Intelligence</h1>
        <p className="text-gray-400">Elite sprint trajectory and behavioral analysis.</p>
      </header>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg border border-gray-700">
          <h2 className="text-xl font-semibold mb-4 text-blue-400">Goal Trajectory</h2>
          <div className="space-y-4">
            <div><p className="text-sm text-gray-400">Target ({trajectoryData.goal.goal_type})</p><p className="text-2xl font-bold">{trajectoryData.goal.target_value} hrs</p></div>
            <div><p className="text-sm text-gray-400">Projected Run-rate</p><p className="text-2xl font-bold text-yellow-400">{trajectoryData.forecast.projected_final_value} hrs</p></div>
            <div><span className={`px-3 py-1 rounded-full text-xs font-bold ${trajectoryData.forecast.status === 'On Track' ? 'bg-green-900 text-green-300' : 'bg-yellow-900 text-yellow-300'}`}>{trajectoryData.forecast.status.toUpperCase()}</span></div>
          </div>
        </div>
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg border border-gray-700">
          <h2 className="text-xl font-semibold mb-4 text-purple-400">Macro Trend Detected</h2>
          <div className="bg-purple-900/30 p-4 rounded border border-purple-500/30"><p className="text-purple-200">{trajectoryData.trend_detected}</p></div>
          <div className="mt-6"><h3 className="text-sm font-semibold text-gray-400 mb-2">AI Course Correction</h3><div className="bg-blue-900/30 p-4 rounded border border-blue-500/30"><p className="text-blue-200">{trajectoryData.course_correction}</p></div></div>
        </div>
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg border border-gray-700">
          <h2 className="text-xl font-semibold mb-4 text-emerald-400">Consistency Survival</h2>
          <div className="flex items-center justify-center py-6">
            <div className="relative w-32 h-32 flex items-center justify-center rounded-full border-8 border-emerald-500"><span className="text-3xl font-bold">{trajectoryData.consistency.survival_probability * 100}%</span></div>
          </div>
          <p className="text-center text-sm text-gray-400">{trajectoryData.consistency.forecast_message}</p>
          {trajectoryData.consistency.high_risk_day && <p className="text-center text-xs text-red-400 mt-4">⚠️ High risk drop-off: {trajectoryData.consistency.high_risk_day}</p>}
        </div>
      </div>
    </div>
  );
};

export default MacroDashboard;
