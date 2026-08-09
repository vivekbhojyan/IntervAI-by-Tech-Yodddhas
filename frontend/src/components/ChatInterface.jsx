import { useState, useRef, useEffect } from 'react';

function ChatInterface({ messages, isLoading, onSendMessage, error }) {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSendMessage(input);
      setInput('');
    }
  };

  return (
    <div className="flex flex-col h-full bg-transparent glass-panel rounded-2xl overflow-hidden">
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.length === 0 && (
          <div className="flex items-center justify-center h-full text-gray-500">
            <p>Click "Start Interview" to begin.</p>
          </div>
        )}
        {messages.map((msg, idx) => (
          <div 
            key={idx} 
            className={`flex ${msg.role === 'candidate' ? 'justify-end' : 'justify-start'} items-end gap-3 animate-fade-in-up`}
          >
            {msg.role !== 'candidate' && (
              <div className="avatar" style={{background:'#111827'}} aria-hidden>
                AI
              </div>
            )}
            <div className={`max-w-[75%] rounded-2xl px-5 py-4 shadow-md ${msg.role === 'candidate' ? 'bg-indigo-600 text-white rounded-br-none' : 'bg-gray-800 text-gray-100 rounded-bl-none border border-gray-700'}`}>
              <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>
              <div className="text-[11px] text-gray-400 mt-2 text-right">{new Date(msg.ts || Date.now()).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'})}</div>
            </div>
            {msg.role === 'candidate' && (
              <div className="avatar" style={{background:'#4338ca'}} aria-hidden>
                {Array.isArray(msg.senderInitials) ? msg.senderInitials.join('') : (msg.senderInitials || 'Y')}
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start animate-fade-in-up">
            <div className="bg-gray-700 text-gray-400 rounded-2xl rounded-bl-none px-5 py-4 border border-gray-600 flex space-x-2 items-center shadow-md">
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
            </div>
          </div>
        )}
        {error && (
          <div className="p-4 bg-red-900/30 border border-red-700 rounded-xl text-red-400 text-sm">
            Error: {error}
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 bg-gradient-to-t from-black/20 to-transparent border-t border-gray-800">
        <form onSubmit={handleSubmit} className="relative flex items-center">
          <input
            type="text"
            className="w-full bg-transparent border border-gray-700 rounded-full pl-5 pr-12 py-4 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-sm placeholder-gray-400 shadow-inner"
            placeholder={messages.length === 0 ? "Waiting for interview to start..." : "Type your answer..."}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isLoading || messages.length === 0}
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="absolute right-2 p-2 bg-indigo-600 hover:bg-indigo-500 rounded-full text-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
            </svg>
          </button>
        </form>
      </div>
    </div>
  );
}

export default ChatInterface;
