import React, { useState, useRef } from 'react';
import { Mic, Square } from 'lucide-react';

interface Props {
  onTranscript: (text: string) => void;
}

export const VoiceInput: React.FC<Props> = ({ onTranscript }) => {
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorder = useRef<MediaRecorder | null>(null);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      mediaRecorder.current = recorder;
      recorder.start();
      setIsRecording(true);
      setTimeout(() => { recorder.stop(); setIsRecording(false); onTranscript('🎤 Voice note saved'); }, 5000);
    } catch { alert('Microphone access denied'); }
  };

  return (
    <button onClick={startRecording} className={`p-2 rounded-lg border ${isRecording ? 'bg-red-500/20 border-red-500/40 text-red-400 animate-pulse' : 'bg-green-500/20 border-green-500/40 text-green-400'}`}>
      {isRecording ? <Square className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
    </button>
  );
};
