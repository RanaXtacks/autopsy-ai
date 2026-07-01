import { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const IntelligenceContext = createContext(null);

export const IntelligenceProvider = ({ children }) => {
  const [globalState, setGlobalState] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchGlobalState = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const token = localStorage.getItem('token');
        const headers = token ? { Authorization: `Bearer ${token}` } : {};

        const res = await axios.get('/api/v1/intelligence/state', { headers });
        setGlobalState(res.data);
      } catch (err) {
        console.error('Error fetching global intelligence state:', err);
        setError('Failed to load global intelligence state. Please refresh or try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchGlobalState();
  }, []);

  return (
    <IntelligenceContext.Provider value={{ globalState, loading, error }}>
      {children}
    </IntelligenceContext.Provider>
  );
};

export const useIntelligence = () => {
  const context = useContext(IntelligenceContext);
  if (!context) {
    throw new Error('useIntelligence must be used within an IntelligenceProvider');
  }
  return context;
};
