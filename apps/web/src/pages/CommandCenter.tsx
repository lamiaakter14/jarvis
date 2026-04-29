// apps/web/src/pages/CommandCenter.tsx
import { sendMessage } from '../api/chatApi';
import React, { useState } from 'react';
import { ChatMessage } from '../components/ChatMessage';
import { SystemPanel } from '../components/SystemPanel';
import { PlannerMode } from '../components/PlannerMode';
import { ApprovalFlow } from '../components/ApprovalFlow';
import { detectIntent, SystemMode } from '../components/IntentDetector';

interface Message {
  id: string;
  type: 'user' | 'jarvis' | 'system';
  content: string;
  timestamp: string;
}

export default function CommandCenter() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'system',
      content: 'JARVIS Command Center initialized. Type your command or idea.',
      timestamp: new Date().toLocaleTimeString()
    }
  ]);
  const [input, setInput] = useState('');
  const [mode, setMode] = useState<SystemMode>('chat');
  const [showPlan, setShowPlan] = useState(false);
  const [showApproval, setShowApproval] = useState(false);
  const [projectName, setProjectName] = useState<string>();
  const [taskCount, setTaskCount] = useState(0);
  const [projectData, setProjectData] = useState<any>(null);
  const [executing, setExecuting] = useState(false);

  const addMessage = (type: Message['type'], content: string) => {
    const newMsg: Message = {
      id: Date.now().toString(),
      type,
      content,
      timestamp: new Date().toLocaleTimeString()
    };
    setMessages(prev => [...prev, newMsg]);
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = input.trim();
    addMessage('user', userMessage);
    setInput('');

    try {
      const result = await sendMessage(userMessage);
      setMode(result.mode as SystemMode);
      addMessage('jarvis', result.response);
      
      // Phase 3: Planner Project Info
      if (result.meta?.project) {
        const project = result.meta.project;
        setProjectName(project.title);
        setTaskCount(project.tasks?.length || 0);
        setProjectData(project);
        
        addMessage('system', `📁 Project: ${project.id}`);
        addMessage('system', `📋 ${project.phases?.length || 0} phases, ${project.tasks?.length || 0} tasks`);
        
        if (project.phases) {
          project.phases.forEach((p: any) => {
            addMessage('system', `  ⬜ Phase ${p.order}: ${p.name}`);
          });
        }
      }

      // Phase 3: Show Planner Questions
      if (result.meta?.questions) {
        addMessage('jarvis', '📋 Please answer these questions:');
        result.meta.questions.forEach((q: string, i: number) => {
          addMessage('jarvis', `  ${i + 1}. ${q}`);
        });
      }

      // Phase 4: Execution result
      if (result.meta?.execution) {
        const exec = result.meta.execution;
        addMessage('system', `⚡ ${exec.tasks_executed} tasks executed successfully!`);
        if (exec.completed) {
          exec.completed.forEach((t: string) => {
            addMessage('system', `  ✅ ${t}`);
          });
        }
      }

      // Handle planner mode
      if (result.intent === 'planner') {
        addMessage('system', 'Planner ready. Click "Start Planning" to begin the question layer.');
        setShowPlan(true);
      } else if (result.intent === 'execution') {
        addMessage('system', 'Execution mode active. Waiting for approved tasks.');
      }
      
      addMessage('system', `Intent: ${result.intent} (confidence: ${(result.confidence * 100).toFixed(0)}%)`);
      
    } catch (error) {
      console.error('Chat API error:', error);
      
      const intent = detectIntent(userMessage);
      setMode(intent.mode);
      addMessage('jarvis', '⚠️ Backend not reachable. Using local mode.');
      addMessage('system', `Local mode: ${intent.mode} (offline)`);
      
      if (intent.mode === 'planner') {
        setShowPlan(true);
      }
    }
  };

  const handleGeneratePlan = (plan: any) => {
    setProjectName(plan.projectName);
    setTaskCount(plan.tasks.length);
    addMessage('system', `📁 Plan generated: ${plan.projectName} (${plan.projectId})`);
    addMessage('system', `📋 ${plan.phases.length} phases, ${plan.tasks.length} tasks created`);
    setShowApproval(true);
  };

  // ============================================================
  // Phase 4: Approve → Queue + Execute
  // ============================================================
  const handleApprove = async () => {
    setMode('execution');
    setShowApproval(false);
    setShowPlan(false);
    setExecuting(true);
    
    if (projectData) {
      addMessage('system', `✅ Project ${projectData.id} approved!`);
      addMessage('system', `📋 ${projectData.tasks?.length || 0} tasks queued for execution.`);
      
      // Phase 4: Queue tasks then execute
      try {
        // Step 1: Queue
        await fetch('/api/execute/queue', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ project: projectData })
        });
        
        addMessage('system', '⏳ Tasks queued. Starting execution...');
        
        // Step 2: Execute
        const execRes = await fetch('/api/execute/start', { method: 'POST' });
        const execData = await execRes.json();
        
        addMessage('system', `⚡ ${execData.tasks_executed} tasks executed successfully!`);
        
        if (execData.tasks) {
          execData.tasks.forEach((t: any) => {
            addMessage('system', `  ✅ ${t.title || t.id}`);
          });
        }
        
        addMessage('jarvis', '🎉 All tasks completed! Execution phase done.');
        
        // Step 3: Get status
        const statusRes = await fetch('/api/execute/status');
        const statusData = await statusRes.json();
        setTaskCount(statusData.completed || 0);
        
      } catch (err) {
        console.error('Execution error:', err);
        addMessage('system', '⚠️ Execution engine offline. Tasks queued locally.');
        addMessage('jarvis', '⚡ Ready for execution. Type "execute all tasks" when ready.');
      }
    } else {
      addMessage('system', '✅ Plan approved. Ready for execution.');
      addMessage('jarvis', '⚡ Execution Mode active. All tasks queued for approval-based execution.');
    }
    
    setExecuting(false);
  };

  const handleEdit = () => {
    addMessage('system', '✏️ Plan edit mode. Make changes and re-generate.');
  };

  const handleReject = () => {
    setShowApproval(false);
    setShowPlan(false);
    setMode('chat');
    setProjectData(null);
    setProjectName(undefined);
    setTaskCount(0);
    addMessage('system', '❌ Plan rejected. Start over when ready.');
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex h-full">
      {/* MAIN CHAT */}
      <main className="flex-1 flex flex-col">
        {/* Mode Badge */}
        <div className="px-4 py-2 border-b border-[#232A34] bg-[#0F1419] flex items-center gap-4">
          <div className="flex items-center gap-2">
            <span className={`w-2 h-2 rounded-full animate-pulse ${
              mode === 'planner' ? 'bg-purple-500' : mode === 'execution' ? 'bg-green-500' : 'bg-blue-500'
            }`} />
            <span className="text-xs text-gray-400 uppercase tracking-wider">
              Mode: <span className="text-white font-bold">{mode}</span>
            </span>
          </div>
          {projectName && <span className="text-[10px] text-gray-500">Project: <span className="text-purple-400">{projectName}</span></span>}
          {executing && <span className="text-[10px] text-yellow-400 animate-pulse">⏳ Executing...</span>}
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-2">
          {messages.map(msg => <ChatMessage key={msg.id} {...msg} />)}
          {showPlan && <PlannerMode onGeneratePlan={handleGeneratePlan} />}
          <ApprovalFlow visible={showApproval} onApprove={handleApprove} onEdit={handleEdit} onReject={handleReject} />
        </div>

        {/* Input */}
        <div className="p-4 border-t border-[#232A34] bg-[#0F1419]">
          <div className="flex gap-2">
            <input type="text" value={input} onChange={(e) => setInput(e.target.value)} onKeyPress={handleKeyPress}
              placeholder="Type a command or idea..." className="flex-1 bg-[#0A0E14] border border-[#232A34] rounded px-4 py-2 text-sm text-white font-mono placeholder-gray-600 focus:border-purple-500 outline-none" />
            <button onClick={handleSend} className="px-6 py-2 bg-purple-600 text-white rounded text-sm font-bold hover:bg-purple-500">▶</button>
          </div>
        </div>
      </main>

      {/* RIGHT PANEL */}
      <aside className="w-72 border-l border-[#232A34] hidden lg:block">
        <SystemPanel mode={mode} projectName={projectName} taskCount={taskCount} />
      </aside>
    </div>
  );
}