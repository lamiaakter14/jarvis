import React, { useState, useEffect, useRef } from 'react';
import { Send, MapPin, Brain, Loader2, Zap, Target, DollarSign } from 'lucide-react';

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  contexts?: any[];
  intent?: string;
  project?: any;
  timestamp: Date;
}

export const MasterChat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: 'আমি JARVIS. সখীপুরের লোকাল কনটেক্স অনুযায়ী প্ল্যান করতে পারি।\n\nআপনি কি করতে চান?\n- 🏗️ বাড়ি বানাতে\n- �� দোকান খুলতে\n- 💰 টাকা আয় করতে\n- 📝 কিছু plan করতে',
      isUser: false,
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [showQuestions, setShowQuestions] = useState(false);
  const [answerIndex, setAnswerIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (messageText: string) => {
    if (!messageText.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: messageText,
      isUser: true,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('/api/chat/context-aware', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: messageText })
      });
      const data = await response.json();

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: data.response,
        isUser: false,
        contexts: data.contexts_loaded,
        intent: data.intent,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, aiMessage]);
    } catch (err) {
      console.error('Chat error:', err);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'দুঃখিত, কিছু সমস্যা হয়েছে। আবার চেষ্টা করুন।',
        isUser: false,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleSend = async () => {
    if (showQuestions && answerIndex < currentQuestions.length) {
      // Save answer
      const newAnswers = { ...answers, [currentQuestions[answerIndex]]: input };
      setAnswers(newAnswers);
      
      // Add answer to chat
      const answerMsg: Message = {
        id: Date.now().toString(),
        text: input,
        isUser: true,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, answerMsg]);
      
      // Move to next question or finish
      const nextIndex = answerIndex + 1;
      if (nextIndex < currentQuestions.length) {
        setAnswerIndex(nextIndex);
        const nextQuestion: Message = {
          id: (Date.now() + 1).toString(),
          text: `❓ ${currentQuestions[nextIndex]}`,
          isUser: false,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, nextQuestion]);
        setInput('');
      } else {
        setShowQuestions(false);
        setLoading(true);
        
        try {
          const planResponse = await fetch('/api/planner/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ answers: newAnswers, questions: currentQuestions })
          });
          const planData = await planResponse.json();
          
          const planMessage: Message = {
            id: (Date.now() + 2).toString(),
            text: `📋 **Project Plan Created!**\n\n**Project ID:** ${planData.project_id || 'PROJ-001'}\n**Project Name:** ${planData.project_name || 'New Project'}\n\n**Tasks:**\n${planData.tasks?.map((t: any) => `- ${t.name} (${t.estimated_hours} hrs)`).join('\n') || '- Setup task'}\n\n✅ Type "approve" to start.`,
            isUser: false,
            timestamp: new Date()
          };
          setMessages(prev => [...prev, planMessage]);
        } catch (err) {
          console.error('Plan creation error:', err);
        } finally {
          setLoading(false);
          setInput('');
        }
      }
    } else {
      await sendMessage(input);
    }
  };

  return (
    <div className="flex flex-col h-full bg-gray-900 min-h-screen">
      <div className="border-b border-gray-800 p-4 bg-gray-900 sticky top-0 z-10">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold flex items-center gap-2">
              <Brain className="w-5 h-5 text-purple-400" />
              <span className="text-white">Master Chat</span>
              <span className="text-xs bg-green-600/30 text-green-400 px-2 py-1 rounded-full ml-2 flex items-center gap-1">
                <MapPin className="w-3 h-3" /> Sakhipur Context Ready
              </span>
            </h2>
            <p className="text-xs text-gray-500 mt-1">
              💡 Try: "দোকান খুলতে চাই" | "বাড়ি বানাতে কত লাগবে?" | "৭ দিনে ১০,০০০ টাকা"
            </p>
          </div>
          <div className="flex gap-1">
            <Target className="w-4 h-4 text-blue-400" />
            <DollarSign className="w-4 h-4 text-green-400" />
            <Zap className="w-4 h-4 text-yellow-500" />
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex ${msg.isUser ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] rounded-lg p-3 ${
              msg.isUser 
                ? 'bg-blue-600 text-white' 
                : 'bg-gray-800 text-gray-200'
            }`}>
              <p className="whitespace-pre-wrap">{msg.text}</p>
              
              {!msg.isUser && msg.contexts && msg.contexts.length > 0 && (
                <div className="mt-3 pt-2 border-t border-gray-700">
                  <p className="text-xs flex items-center gap-1 text-green-400 mb-2">
                    <MapPin className="w-3 h-3" /> 📍 Local Context Loaded:
                  </p>
                  <div className="space-y-1">
                    {msg.contexts.slice(0, 4).map((ctx: any) => (
                      <div key={ctx.id} className="text-xs bg-gray-700/50 rounded p-1.5">
                        <span className="font-semibold">{ctx.key}</span>
                        <span className="text-green-400 ml-2">{ctx.value}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              <span className="text-[10px] opacity-50 mt-1 block">
                {msg.timestamp.toLocaleTimeString()}
              </span>
            </div>
          </div>
        ))}
        
        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-800 rounded-lg p-3 flex items-center gap-2">
              <Loader2 className="w-4 h-4 animate-spin" />
              <span className="text-sm text-gray-300">JARVIS thinking... 🤔</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="border-t border-gray-800 p-4 bg-gray-900">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder={showQuestions ? "এখানে উত্তর দিন..." : "Bangla or English e likhun..."}
            className="flex-1 bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:border-purple-500"
          />
          <button
            onClick={handleSend}
            disabled={loading || !input.trim()}
            className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg disabled:opacity-50 transition-colors"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
        <div className="flex gap-4 mt-2 text-xs text-gray-500 flex-wrap">
          <span>📍 "কাঠের দাম কত?"</span>
          <span>🏗️ "বাড়ি বানাতে কত লাগবে?"</span>
          <span>👷 "শ্রমিক লাগবে"</span>
          <span>💰 "৭ দিনে ১০,০০০ টাকা"</span>
        </div>
      </div>
    </div>
  );
};
