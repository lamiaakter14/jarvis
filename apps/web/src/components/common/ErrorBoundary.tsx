import React from 'react';

interface Props { children: React.ReactNode; }
interface State { hasError: boolean; error?: Error; }

export class ErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) { super(props); this.state = { hasError: false }; }
  static getDerivedStateFromError(error: Error) { return { hasError: true, error }; }
  
  render() {
    if (this.state.hasError) {
      return (
        <div className="flex items-center justify-center h-screen bg-[#0A0E14] text-white">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-red-400 mb-4">⚠️ Something went wrong</h1>
            <p className="text-gray-400 mb-4">{this.state.error?.message}</p>
            <button onClick={() => window.location.reload()} className="px-6 py-2 bg-purple-600 text-white rounded-lg font-bold">
              Reload JARVIS
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}
