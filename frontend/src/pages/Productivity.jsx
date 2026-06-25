import { useState, useEffect } from 'react';
import axios from 'axios';
import { RefreshCw, Target, Zap, Clock, TrendingUp } from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import ScoreCard from '../components/widgets/ScoreCard';
import TrendChart from '../components/widgets/TrendChart';
import InsightsList from '../components/widgets/InsightsList';

const Productivity = () => {
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [todayData, setTodayData] = useState(null);
  const [historyData, setHistoryData] = useState([]);

  const fetchScores = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const headers = token ? { Authorization: `Bearer ${token}` } : {};

      const [todayRes, historyRes] = await Promise.all([
        axios.get('/api/scores/today', { headers }),
        axios.get('/api/scores/history?days=30', { headers })
      ]);

      setTodayData(todayRes.data);
      setHistoryData(historyRes.data);
    } catch (err) {
      console.error('Error fetching scores:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchScores();
  }, []);

  const handleGenerate = async () => {
    try {
      setGenerating(true);
      const token = localStorage.getItem('token');
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      
      await axios.post('/api/scores/generate', {}, { headers });
      await fetchScores();
    } catch (err) {
      console.error('Error generating scores:', err);
      alert('Failed to generate scores');
    } finally {
      setGenerating(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full min-h-[400px]">
        <div className="w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  const scores = todayData?.scores || {};
  const insights = todayData?.insights || [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Productivity Intelligence</h1>
          <p className="text-slate-500 mt-1">AI-scored behavioral analysis and insights</p>
        </div>
        <Button onClick={handleGenerate} disabled={generating}>
          {generating ? (
            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
          ) : (
            <RefreshCw size={20} className="mr-2" />
          )}
          {generating ? 'Processing Engine...' : 'Run Scoring Engine'}
        </Button>
      </div>

      {/* Top Scores */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <ScoreCard 
          title="Productivity Score" 
          score={scores.productivity_score || 0} 
          icon={TrendingUp} 
          colorClass="bg-indigo-100 text-indigo-600" 
        />
        <ScoreCard 
          title="Focus Score" 
          score={scores.focus_score || 0} 
          icon={Target} 
          colorClass="bg-blue-100 text-blue-600" 
        />
        <ScoreCard 
          title="Consistency Score" 
          score={scores.consistency_score || 0} 
          icon={Clock} 
          colorClass="bg-emerald-100 text-emerald-600" 
        />
        <ScoreCard 
          title="Discipline Score" 
          score={scores.discipline_score || 0} 
          icon={Zap} 
          colorClass="bg-amber-100 text-amber-600" 
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Chart */}
        <Card className="lg:col-span-2 p-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">Performance Trends (30 Days)</h3>
          <TrendChart historyData={historyData} />
        </Card>

        {/* AI Insights */}
        <Card className="p-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">Intelligence Insights</h3>
          <InsightsList insights={insights} />
        </Card>
      </div>
    </div>
  );
};

export default Productivity;
