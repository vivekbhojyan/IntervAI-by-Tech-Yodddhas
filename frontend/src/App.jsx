import { useState, useEffect } from 'react';
import ChatInterface from './components/ChatInterface';
import ProgressPanel from './components/ProgressPanel';
import FeedbackModal from './components/FeedbackModal';
import DomainSelector from './components/DomainSelector';
import candidatesData from '../../candidates.json';

function App() {
  const [sessionId, setSessionId] = useState('');
  const [candidate, setCandidate] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isDone, setIsDone] = useState(false);
  const [feedback, setFeedback] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Stats for the progress panel
  const [questionCount, setQuestionCount] = useState(0);
  const [progress, setProgress] = useState(null);
  const [selectedDomain, setSelectedDomain] = useState(null);

  useEffect(() => {
    // Generate a unique session ID
    setSessionId(Math.random().toString(36).substring(2, 15));
    // Load the first candidate for demo purposes
    setCandidate(candidatesData.candidates[0]);
  }, []);

  const startInterview = async () => {
    if (!sessionId || !candidate) return;
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/api/interview', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId, candidate, domain: selectedDomain })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Failed to start interview');
      
      setMessages([{ role: 'interviewer', content: data.reply }]);
      setQuestionCount(1);
      if (data.progress) {
        setProgress(data.progress);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const sendMessage = async (message) => {
    if (!message.trim() || isLoading) return;
    
    const newMessages = [...messages, { role: 'candidate', content: message }];
    setMessages(newMessages);
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/api/interview', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sessionId, message })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Failed to send message');
      
      setMessages([...newMessages, { role: 'interviewer', content: data.reply }]);
      if (!data.done) {
        setQuestionCount(prev => prev + 1);
      }
      setIsDone(data.done);
      if (data.feedback) {
        setFeedback(data.feedback);
      }
      if (data.progress) {
        setProgress(data.progress);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-900 overflow-hidden font-sans text-gray-100">
      
      {/* LEFT PANEL: Chat & Domain Selection */}
      <div className="flex-1 flex flex-col border-r border-gray-700 bg-gray-800">
        <header className="px-6 py-4 border-b border-gray-700 bg-gray-900 shadow-sm z-10 flex justify-between items-center">
          <div>
            <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">AI Interview Agent</h1>
            <p className="text-sm text-gray-400">Interviewing: {candidate?.member?.name} ({candidate?.member?.jobRole})</p>
          </div>
          {messages.length === 0 && (
            <button 
              onClick={startInterview}
              disabled={isLoading}
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 rounded-lg text-sm font-medium transition-colors shadow-lg shadow-indigo-900 flex items-center gap-2"
            >
              {isLoading && <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>}
              Start Interview
            </button>
          )}
        </header>

        <main className="flex-1 overflow-y-auto relative p-6">
          {messages.length === 0 ? (
            <div className="max-w-4xl mx-auto space-y-6">
              <div className="bg-gray-900/90 border border-gray-700 p-6 rounded-2xl shadow-xl">
                <h2 className="text-lg font-bold text-gray-200 mb-1">Welcome to your Technical Interview</h2>
                <p className="text-sm text-gray-400">
                  The AI Interview Agent will adaptively test your technical depth based on your candidate profile. You may select a target domain module below or proceed with the full curriculum.
                </p>
              </div>

              <DomainSelector
                selectedDomain={selectedDomain}
                onSelectDomain={setSelectedDomain}
              />
            </div>
          ) : (
            <ChatInterface 
              messages={messages} 
              isLoading={isLoading} 
              onSendMessage={sendMessage} 
              error={error}
            />
          )}
        </main>
      </div>


      {/* RIGHT PANEL: Progress / Stats */}
      <div className="w-80 flex flex-col bg-gray-900 p-6 overflow-y-auto">
        <ProgressPanel 
          candidate={candidate} 
          questionCount={questionCount} 
          isDone={isDone}
          progress={progress}
        />
      </div>


      {/* MODAL: Final Feedback */}
      {isDone && feedback && (
        <FeedbackModal feedback={feedback} candidate={candidate} />
      )}
    </div>
  );
}

export default App;
