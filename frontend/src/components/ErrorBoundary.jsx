import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("Autopsy AI Caught Error:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-gray-100 p-6">
          <div className="bg-gray-800 border border-red-900/50 p-8 rounded-lg shadow-lg max-w-lg w-full text-center">
            <h1 className="text-2xl font-bold text-red-400 mb-4">Something went wrong.</h1>
            <p className="text-gray-400 mb-6">
              Our autonomous agents hit an unrecoverable error in this component. 
              Please refresh or try resetting your local cache.
            </p>
            <button 
              onClick={() => window.location.reload()}
              className="bg-red-600 hover:bg-red-500 text-white px-6 py-2 rounded font-medium transition"
            >
              Reload Application
            </button>
          </div>
        </div>
      );
    }

    return this.props.children; 
  }
}

export default ErrorBoundary;
