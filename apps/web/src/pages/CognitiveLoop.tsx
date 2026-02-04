import React, { useState } from 'react';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { Brain, CheckCircle, Loader } from 'lucide-react';
import { cognitiveLoopApi } from '../api/cognitive-loop';
import toast from 'react-hot-toast';

interface AgentResult {
  name: string;
  status: 'pending' | 'running' | 'completed' | 'error';
  result?: any;
  error?: string;
}

export const CognitiveLoop: React.FC = () => {
  const [isRunning, setIsRunning] = useState(false);
  const [results, setResults] = useState<any>(null);
  const [agents, setAgents] = useState<AgentResult[]>([
    { name: 'Strategist', status: 'pending' },
    { name: 'Mentor', status: 'pending' },
    { name: 'Executor', status: 'pending' },
    { name: 'Innovator', status: 'pending' },
    { name: 'Amplifier', status: 'pending' },
  ]);

  const runCognitiveLoop = async () => {
    setIsRunning(true);
    setResults(null);

    try {
      // Simulate agent progression
      for (let i = 0; i < agents.length; i++) {
        setAgents(prev => prev.map((agent, idx) => 
          idx === i ? { ...agent, status: 'running' } : agent
        ));
        await new Promise(resolve => setTimeout(resolve, 500));
      }

      const result = await cognitiveLoopApi.runLoop();
      
      setAgents(agents.map(agent => ({ ...agent, status: 'completed' })));
      setResults(result);
      toast.success('Cognitive loop completed successfully!');
    } catch (err: any) {
      toast.error('Failed to run cognitive loop');
      setAgents(agents.map(agent => ({ 
        ...agent, 
        status: agent.status === 'running' ? 'error' : agent.status 
      })));
    } finally {
      setIsRunning(false);
    }
  };

  const getStatusIcon = (status: AgentResult['status']) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-600" />;
      case 'running':
        return <Loader className="w-5 h-5 text-blue-600 animate-spin" />;
      default:
        return <div className="w-5 h-5 rounded-full border-2 border-gray-300" />;
    }
  };

  const getStatusBadge = (status: AgentResult['status']) => {
    const variants: Record<AgentResult['status'], any> = {
      pending: 'default',
      running: 'info',
      completed: 'success',
      error: 'error',
    };
    return <Badge variant={variants[status]}>{status}</Badge>;
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">Cognitive Loop</h1>
          <p className="text-gray-600 dark:text-gray-400">
            Execute all 5 cognitive agents in sequence
          </p>
        </div>
        <Button
          onClick={runCognitiveLoop}
          disabled={isRunning}
          isLoading={isRunning}
          size="lg"
        >
          <Brain className="w-5 h-5 mr-2" />
          {isRunning ? 'Running...' : 'Run Cognitive Loop'}
        </Button>
      </div>

      {/* Agent Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        {agents.map((agent) => (
          <Card key={agent.name} className="text-center">
            <div className="flex flex-col items-center gap-3">
              {getStatusIcon(agent.status)}
              <div>
                <h3 className="font-semibold">{agent.name}</h3>
                <div className="mt-2">{getStatusBadge(agent.status)}</div>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Results */}
      {results && (
        <Card>
          <h2 className="text-xl font-semibold mb-4">Results</h2>
          <div className="space-y-4">
            {/* Strategist Results */}
            <div>
              <h3 className="font-medium mb-2">Strategist - Plan Generated</h3>
              <div className="bg-gray-50 dark:bg-gray-900 p-4 rounded-lg">
                <pre className="text-sm overflow-x-auto">
                  {JSON.stringify(results.strategist, null, 2)}
                </pre>
              </div>
            </div>

            {/* Mentor Results */}
            <div>
              <h3 className="font-medium mb-2">Mentor - Knowledge Gaps</h3>
              <div className="bg-gray-50 dark:bg-gray-900 p-4 rounded-lg">
                <pre className="text-sm overflow-x-auto">
                  {JSON.stringify(results.mentor, null, 2)}
                </pre>
              </div>
            </div>

            {/* Other results */}
            <div>
              <h3 className="font-medium mb-2">Full Results</h3>
              <div className="bg-gray-50 dark:bg-gray-900 p-4 rounded-lg">
                <pre className="text-sm overflow-x-auto">
                  {JSON.stringify(results, null, 2)}
                </pre>
              </div>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
};
