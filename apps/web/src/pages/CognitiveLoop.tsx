import React, { useState } from 'react';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { Brain, CheckCircle, Loader, AlertCircle, ChevronDown, ChevronUp } from 'lucide-react';
import { cognitiveLoopApi, CognitiveLoopResult } from '../api/cognitive-loop';
import toast from 'react-hot-toast';

type AgentStatus = 'pending' | 'running' | 'completed' | 'error';

interface BadgeVariantMap {
  pending: 'default';
  running: 'info';
  completed: 'success';
  error: 'error';
}

const BADGE_VARIANTS: BadgeVariantMap = {
  pending: 'default',
  running: 'info',
  completed: 'success',
  error: 'error',
};

type AgentKey = 'strategist' | 'mentor' | 'executor' | 'innovator' | 'amplifier';

interface AgentCard {
  key: AgentKey;
  name: string;
  description: string;
  status: AgentStatus;
}

const INITIAL_AGENTS: AgentCard[] = [
  { key: 'strategist', name: 'Strategist', description: 'Daily plan & priorities', status: 'pending' },
  { key: 'mentor', name: 'Mentor', description: 'Knowledge gaps & task guidance', status: 'pending' },
  { key: 'executor', name: 'Executor', description: 'Task execution & tracking', status: 'pending' },
  { key: 'innovator', name: 'Innovator', description: 'New ideas & automation', status: 'pending' },
  { key: 'amplifier', name: 'Amplifier', description: 'Performance metrics', status: 'pending' },
];

function getAgentSummary(key: AgentKey, result: CognitiveLoopResult): string {
  switch (key) {
    case 'strategist': {
      const tasks = result.strategist?.plan?.tasks;
      if (Array.isArray(tasks) && tasks.length > 0) {
        return `${tasks.length} task(s) planned`;
      }
      return 'Plan generated';
    }
    case 'mentor': {
      const feedback = result.mentor?.task_feedback;
      const gapKeys = result.mentor?.gaps ? Object.keys(result.mentor.gaps) : [];
      const parts: string[] = [];
      if (gapKeys.length > 0) parts.push(`${gapKeys.length} gap(s) identified`);
      if (Array.isArray(feedback) && feedback.length > 0) parts.push(`${feedback.length} task(s) reviewed`);
      return parts.length > 0 ? parts.join(', ') : 'Analysis complete';
    }
    case 'executor':
      return result.executor?.status ?? 'Tasks executed';
    case 'innovator': {
      const innovations = result.innovator?.innovations;
      if (innovations && typeof innovations === 'object') {
        const count = Object.keys(innovations).length;
        return count > 0 ? `${count} innovation(s) generated` : 'Innovations generated';
      }
      return 'Innovations generated';
    }
    case 'amplifier': {
      const perf = result.amplifier?.performance;
      if (perf && typeof perf === 'object') {
        const count = Object.keys(perf).length;
        return count > 0 ? `${count} metric(s) collected` : 'Metrics collected';
      }
      return 'Metrics collected';
    }
  }
}

const AgentResultCard: React.FC<{
  agent: AgentCard;
  result: CognitiveLoopResult | null;
}> = ({ agent, result }) => {
  const [expanded, setExpanded] = useState(false);

  const getStatusIcon = (status: AgentStatus) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-600" />;
      case 'running':
        return <Loader className="w-5 h-5 text-blue-600 animate-spin" />;
      case 'error':
        return <AlertCircle className="w-5 h-5 text-red-500" />;
      default:
        return <div className="w-5 h-5 rounded-full border-2 border-gray-300" />;
    }
  };

  return (
    <Card className="flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          {getStatusIcon(agent.status)}
          <div>
            <h3 className="font-semibold text-sm">{agent.name}</h3>
            <p className="text-xs text-gray-500 dark:text-gray-400">{agent.description}</p>
          </div>
        </div>
        <Badge variant={BADGE_VARIANTS[agent.status]}>{agent.status}</Badge>
      </div>

      {result && agent.status === 'completed' && (
        <>
          <p className="text-sm text-gray-700 dark:text-gray-300">
            {getAgentSummary(agent.key, result)}
          </p>
          <button
            className="flex items-center gap-1 text-xs text-blue-600 dark:text-blue-400 hover:underline self-start"
            onClick={() => setExpanded(prev => !prev)}
            aria-expanded={expanded}
          >
            {expanded ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
            {expanded ? 'Hide details' : 'Show details'}
          </button>
          {expanded && (
            <div className="bg-gray-50 dark:bg-gray-900 p-3 rounded-lg overflow-x-auto">
              <pre className="text-xs">
                {JSON.stringify(result[agent.key], null, 2)}
              </pre>
            </div>
          )}
        </>
      )}
    </Card>
  );
};

export const CognitiveLoop: React.FC = () => {
  const [isRunning, setIsRunning] = useState(false);
  const [result, setResult] = useState<CognitiveLoopResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [agents, setAgents] = useState<AgentCard[]>(INITIAL_AGENTS);

  const runCognitiveLoop = async () => {
    setIsRunning(true);
    setResult(null);
    setError(null);
    setAgents(INITIAL_AGENTS.map(a => ({ ...a, status: 'running' })));

    try {
      const data = await cognitiveLoopApi.runLoop();
      setResult(data);
      setAgents(INITIAL_AGENTS.map(a => ({ ...a, status: 'completed' })));
      toast.success('Cognitive loop completed successfully!');
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Failed to run cognitive loop';
      setError(message);
      setAgents(INITIAL_AGENTS.map(a => ({ ...a, status: 'error' })));
      toast.error('Failed to run cognitive loop');
    } finally {
      setIsRunning(false);
    }
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

      {error && (
        <div className="flex items-center gap-2 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-red-700 dark:text-red-400">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span className="text-sm">{error}</span>
        </div>
      )}

      {/* Agent Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        {agents.map((agent) => (
          <AgentResultCard key={agent.key} agent={agent} result={result} />
        ))}
      </div>
    </div>
  );
};
