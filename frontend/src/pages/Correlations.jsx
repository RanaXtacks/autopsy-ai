import React, { useState } from 'react';
import axios from 'axios';
import { useIntelligence } from '../context/IntelligenceContext';
import { Network } from 'lucide-react';
import CorrelationList from '../components/widgets/CorrelationList';
import TrendRadar from '../components/widgets/TrendRadar';

const Correlations = () => {
  const { globalState, loading: contextLoading } = useIntelligence();
  const [loading, setLoading] = useState(false);

  const correlations = globalState?.correlations || [];

  const generateCorrelations = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      await axios.post('/api/correlations/generate', {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert('Connections analyzed successfully. Refreshing global state...');
      window.location.reload();
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  if (contextLoading || loading) return <div className="text-white p-6">Computing behavior correlations...</div>;

  const positiveCorrelations = correlations.filter(c => c.relationship_type.includes('Positive'));
  const negativeCorrelations = correlations.filter(c => c.relationship_type.includes('Negative'));
  const topCorrelations = correlations.filter(c => c.confidence_score > 50).slice(0, 5);

  return (
    <div className="p-6 text-white space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-orange-400 to-rose-500">
            Behavior Intelligence
          </h1>
          <p className="text-gray-400 mt-2">Causal reasoning and statistical relationships in your routine.</p>
        </div>
        <button 
          onClick={generateCorrelations}
          className="flex items-center gap-2 px-4 py-2 bg-orange-600 hover:bg-orange-700 rounded-lg transition-colors"
        >
          <Network size={18} />
          Analyze Connections
        </button>
      </div>
      
      {correlations.length === 0 ? (
        <div className="bg-gray-800 p-8 rounded-xl text-center border border-gray-700">
          <p className="text-gray-400">No correlations detected yet. Click "Analyze Connections" to process your data.</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <CorrelationList title="Positive Influences" correlations={positiveCorrelations} type="positive" />
            <CorrelationList title="Negative Influences" correlations={negativeCorrelations} type="negative" />
          </div>
          
          <div className="mt-6">
            <TrendRadar correlations={topCorrelations} />
          </div>
        </>
      )}
    </div>
  );
};

export default Correlations;
