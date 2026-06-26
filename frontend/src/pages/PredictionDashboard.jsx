import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Calendar } from 'lucide-react';
import TomorrowSchedule from '../components/widgets/TomorrowSchedule';
import PrimeTimeHeatmap from '../components/widgets/PrimeTimeHeatmap';
import ChronotypeProfile from '../components/widgets/ChronotypeProfile';
import ForecastGraph from '../components/widgets/ForecastGraph';

const PredictionDashboard = () => {
  const [predictions, setPredictions] = useState([]);
  const [chronotype, setChronotype] = useState('');
  const [loading, setLoading] = useState(true);

  const fetchDashboardData = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };
      
      const [predRes, chronoRes] = await Promise.all([
        axios.get('/api/predictions/tomorrow', { headers }),
        axios.get('/api/predictions/chronotype', { headers })
      ]);
      
      setPredictions(predRes.data.predictions);
      setChronotype(chronoRes.data.chronotype);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const generatePredictions = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      await axios.post('/api/predictions/generate', {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      await fetchDashboardData();
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  if (loading) return <div className="text-white p-6">Generating focus forecasts...</div>;

  return (
    <div className="p-6 text-white space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-indigo-600">
            Predictive Scheduling
          </h1>
          <p className="text-gray-400 mt-2">AI-driven forecasts for optimal productivity blocks.</p>
        </div>
        <button 
          onClick={generatePredictions}
          className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 rounded-lg transition-colors"
        >
          <Calendar size={18} />
          Generate Forecast
        </button>
      </div>
      
      {predictions.length === 0 ? (
        <div className="bg-gray-800 p-8 rounded-xl text-center border border-gray-700">
          <p className="text-gray-400">No predictions for tomorrow. Click "Generate Forecast" to build your schedule.</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="md:col-span-1">
              <ChronotypeProfile chronotype={chronotype} />
            </div>
            <div className="md:col-span-2">
              <TomorrowSchedule predictions={predictions} />
            </div>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <ForecastGraph predictions={predictions} />
            <PrimeTimeHeatmap />
          </div>
        </>
      )}
    </div>
  );
};

export default PredictionDashboard;
