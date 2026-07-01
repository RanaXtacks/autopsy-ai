import { useState, useEffect } from 'react';
import { useIntelligence } from '../context/IntelligenceContext';
import { Brain, Database, FileText, Clock, AlertCircle } from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import { Link } from 'react-router-dom';

import ActivityTimeline from '../components/widgets/ActivityTimeline';
import ActivityDistribution from '../components/widgets/ActivityDistribution';
import ActivityHeatmap from '../components/widgets/ActivityHeatmap';
import InsightsPanel from '../components/widgets/InsightsPanel';

const Dashboard = () => {
  const { globalState, loading, error } = useIntelligence();
  const [summary, setSummary] = useState(null);
  const [timeline, setTimeline] = useState(null);
  const [heatmap, setHeatmap] = useState(null);
  const [insights, setInsights] = useState(null);
  const [period, setPeriod] = useState('daily');

  useEffect(() => {
    if (globalState) {
      const data = globalState;
      setSummary({
        average_daily_activity: data.focus_average || 0,
        most_active_hour: '--',
        most_active_day: '--',
        least_active_hour: '--',
        categories_percentage: {}
      });
      
      setTimeline(data.timeline || []);
      setHeatmap(data.heatmap || { x: [], y: [], z: [] });

      const newInsights = [];
      if (data.archetype) {
        newInsights.push({ type: 'behavior', text: `Primary Archetype: ${data.archetype.primary}` });
        newInsights.push({ type: 'routine', text: `Risk Profile: ${data.archetype.risk_profile}` });
      }
      if (data.segmentation) {
        newInsights.push({ type: 'summary', text: data.segmentation });
      }
      if (data.prescriptions && data.prescriptions.length > 0) {
        data.prescriptions.forEach(p => {
          newInsights.push({ type: 'productivity', text: `Prescription: ${p}` });
        });
      }
      
      setInsights(newInsights);
    }
  }, [globalState]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full min-h-[400px]">
        <div className="w-8 h-8 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
        <AlertCircle className="text-red-600 mt-0.5" size={24} />
        <div>
          <h3 className="font-semibold text-red-800">Error Loading Dashboard</h3>
          <p className="text-red-700 mt-1">{error}</p>
          <Button onClick={() => window.location.reload()} variant="outline" className="mt-4">
            Retry
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Behavioral Insights</h1>
          <p className="text-slate-500 mt-1">First-generation analysis of your activity</p>
        </div>
        <Link to="/upload">
          <Button>New Upload</Button>
        </Link>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-slate-500 font-medium">Avg Daily Activity</p>
              <p className="text-2xl font-bold text-slate-900 mt-1">
                {summary?.average_daily_activity || 0}
              </p>
            </div>
            <div className="w-12 h-12 bg-emerald-100 rounded-xl flex items-center justify-center text-emerald-600">
              <Brain size={24} />
            </div>
          </div>
        </Card>
        
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-slate-500 font-medium">Most Active Hour</p>
              <p className="text-2xl font-bold text-slate-900 mt-1">
                {summary?.most_active_hour || '--'}
              </p>
            </div>
            <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center text-blue-600">
              <Clock size={24} />
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-slate-500 font-medium">Most Active Day</p>
              <p className="text-2xl font-bold text-slate-900 mt-1">
                {summary?.most_active_day || '--'}
              </p>
            </div>
            <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center text-purple-600">
              <Database size={24} />
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-slate-500 font-medium">Least Active Hour</p>
              <p className="text-2xl font-bold text-slate-900 mt-1">
                {summary?.least_active_hour || '--'}
              </p>
            </div>
            <div className="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center text-orange-600">
              <FileText size={24} />
            </div>
          </div>
        </Card>
      </div>

      {/* Main Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Timeline Chart */}
        <Card className="lg:col-span-2 p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-slate-900">Activity Timeline</h3>
            <select 
              value={period} 
              onChange={(e) => setPeriod(e.target.value)}
              className="px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
            >
              <option value="daily">Daily</option>
              <option value="weekly">Weekly</option>
              <option value="monthly">Monthly</option>
            </select>
          </div>
          <ActivityTimeline data={timeline} />
        </Card>

        {/* Insights Panel */}
        <Card className="p-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">V1 Insights</h3>
          <InsightsPanel insights={insights} />
        </Card>

      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Heatmap */}
        <Card className="p-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">Activity Heatmap</h3>
          <ActivityHeatmap data={heatmap} />
        </Card>

        {/* Distribution */}
        <Card className="p-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">Category Distribution</h3>
          <ActivityDistribution data={summary?.categories_percentage || {}} />
        </Card>
      </div>
      
    </div>
  );
};

export default Dashboard;
