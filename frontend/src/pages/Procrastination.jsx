import React, { useState } from 'react';
import axios from 'axios';
import { useIntelligence } from '../context/IntelligenceContext';
import { AlertCircle } from 'lucide-react';
import DistractionList from '../components/widgets/DistractionList';
import TimeLossMetrics from '../components/widgets/TimeLossMetrics';
import RecoverySuggestions from '../components/widgets/RecoverySuggestions';

const Procrastination = () => {
  const { globalState, loading: contextLoading } = useIntelligence();
  const [loading, setLoading] = useState(false);

  const patterns = globalState?.procrastination_patterns || [];
  const metrics = globalState?.procrastination_metrics || null;

  const generatePatterns = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      await axios.post('/api/procrastination/generate', {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert('Behavior scanned successfully. Refreshing global state...');
      window.location.reload();
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  if (contextLoading || loading) return <div className="text-white p-6">Detecting behavioral patterns...</div>;

  return (
    <div className="p-6 text-white space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-red-500 to-rose-600">
            Procrastination Detection
          </h1>
          <p className="text-gray-400 mt-2">Identify your distraction loops, productivity killers, and focus breakdowns.</p>
        </div>
        <button 
          onClick={generatePatterns}
          className="flex items-center gap-2 px-4 py-2 bg-rose-600 hover:bg-rose-700 rounded-lg transition-colors"
        >
          <AlertCircle size={18} />
          Scan Behavior
        </button>
      </div>
      
      {patterns.length === 0 ? (
        <div className="bg-gray-800 p-8 rounded-xl text-center border border-gray-700">
          <p className="text-gray-400">No patterns detected yet. Click "Scan Behavior" to process your data.</p>
        </div>
      ) : (
        <>
          <TimeLossMetrics metrics={metrics} />
          
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-6">
              <DistractionList patterns={patterns} />
            </div>
            <div>
              <RecoverySuggestions patterns={patterns} />
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default Procrastination;
