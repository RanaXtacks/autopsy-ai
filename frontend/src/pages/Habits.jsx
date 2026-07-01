import React, { useState } from 'react';
import axios from 'axios';
import { useIntelligence } from '../context/IntelligenceContext';
import { RefreshCw } from 'lucide-react';
import TopHabits from '../components/widgets/TopHabits';
import TriggerMap from '../components/widgets/TriggerMap';
import RoutineMap from '../components/widgets/RoutineMap';

const Habits = () => {
  const { globalState, loading: contextLoading } = useIntelligence();
  const [loading, setLoading] = useState(false);

  const summary = globalState?.habits_summary || null;

  const generateHabits = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      await axios.post('/api/habits/generate', {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert('Habits scanned successfully. Refreshing global state...');
      window.location.reload();
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  if (contextLoading || loading) return <div className="text-white p-6">Loading habit intelligence...</div>;

  return (
    <div className="p-6 text-white space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-teal-400 to-indigo-500">
            Habit Intelligence
          </h1>
          <p className="text-gray-400 mt-2">Discover your hidden behavioral patterns and triggers.</p>
        </div>
        <button 
          onClick={generateHabits}
          className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 rounded-lg transition-colors"
        >
          <RefreshCw size={18} />
          Scan Patterns
        </button>
      </div>
      
      {summary && summary.total_habits === 0 ? (
        <div className="bg-gray-800 p-8 rounded-xl text-center border border-gray-700">
          <p className="text-gray-400">No habits detected yet. Click "Scan Patterns" to analyze your sessions.</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <TopHabits habits={summary?.top_habits || []} />
            <RoutineMap />
          </div>
          
          <div className="mt-6">
            <TriggerMap />
          </div>
        </>
      )}
    </div>
  );
};

export default Habits;
