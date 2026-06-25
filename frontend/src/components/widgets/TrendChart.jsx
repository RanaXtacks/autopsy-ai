import React from 'react';
import Plot from 'react-plotly.js';

const TrendChart = ({ historyData }) => {
  if (!historyData || historyData.length === 0) {
    return <div className="text-slate-500 text-sm text-center py-8">No historical data available</div>;
  }

  const dates = historyData.map(d => d.date);
  const productivity = historyData.map(d => d.productivity_score);
  const focus = historyData.map(d => d.focus_score);

  return (
    <div className="w-full h-80">
      <Plot
        data={[
          {
            x: dates,
            y: productivity,
            type: 'scatter',
            mode: 'lines+markers',
            name: 'Productivity',
            line: { color: '#0f172a', width: 3 },
            marker: { size: 6 }
          },
          {
            x: dates,
            y: focus,
            type: 'scatter',
            mode: 'lines+markers',
            name: 'Focus',
            line: { color: '#3b82f6', width: 2, dash: 'dot' },
            marker: { size: 5 }
          }
        ]}
        layout={{
          autosize: true,
          margin: { t: 20, r: 20, l: 40, b: 40 },
          legend: { orientation: 'h', y: -0.2 },
          paper_bgcolor: 'transparent',
          plot_bgcolor: 'transparent',
          xaxis: { showgrid: false },
          yaxis: { showgrid: true, gridcolor: '#f1f5f9', range: [0, 105] }
        }}
        useResizeHandler={true}
        style={{ width: '100%', height: '100%' }}
        config={{ displayModeBar: false }}
      />
    </div>
  );
};

export default TrendChart;
