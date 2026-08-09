function FeedbackModal({ feedback, candidate }) {
  if (!feedback) return null;

  return (
    <div className="absolute inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 sm:p-8 animate-fade-in">
      <div className="bg-gray-900 border border-gray-700 rounded-2xl shadow-2xl w-full max-w-4xl max-h-full overflow-hidden flex flex-col animate-slide-up card">
        
        <div className="p-6 border-b border-gray-700 flex justify-between items-center bg-transparent">
          <div>
            <h2 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">Interview Complete</h2>
            <p className="text-sm text-gray-400 mt-1">Final Assessment for {candidate?.member?.name}</p>
          </div>
          <div className="flex items-center gap-3">
            <button 
              onClick={() => window.location.reload()}
              className="px-4 py-2 btn-primary text-sm font-medium"
            >
              Start New Interview
            </button>
            <button onClick={() => window.history.back()} className="px-3 py-2 bg-gray-800 rounded-lg text-sm">Close</button>
          </div>
        </div>

        <div className="p-6 overflow-y-auto space-y-8 bg-gray-900">
          
          <section>
            <h3 className="text-lg font-semibold text-gray-200 mb-3 flex items-center">
              <svg className="w-5 h-5 mr-2 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Summary
            </h3>
            <p className="text-gray-300 text-sm leading-relaxed p-4 bg-gray-800 rounded-xl border border-gray-700 shadow-inner">
              {feedback.summary}
            </p>
          </section>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <section>
              <h3 className="text-lg font-semibold text-gray-200 mb-3 flex items-center">
                <svg className="w-5 h-5 mr-2 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Strengths
              </h3>
              <ul className="space-y-2">
                {feedback.strengths?.map((item, idx) => (
                  <li key={idx} className="text-sm text-gray-300 bg-gray-800 p-3 rounded-lg border border-gray-700 border-l-4 border-l-green-500 shadow-sm">
                    {item}
                  </li>
                ))}
              </ul>
            </section>

            <section>
              <h3 className="text-lg font-semibold text-gray-200 mb-3 flex items-center">
                <svg className="w-5 h-5 mr-2 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                Identified Gaps
              </h3>
              <ul className="space-y-2">
                {feedback.gaps?.map((item, idx) => (
                  <li key={idx} className="text-sm text-gray-300 bg-gray-800 p-3 rounded-lg border border-gray-700 border-l-4 border-l-red-500 shadow-sm">
                    {item}
                  </li>
                ))}
              </ul>
            </section>
          </div>

          <section>
            <h3 className="text-lg font-semibold text-gray-200 mb-3 flex items-center">
              <svg className="w-5 h-5 mr-2 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              Recommended Next Steps
            </h3>
            <ul className="space-y-2">
              {feedback.next?.map((item, idx) => (
                <li key={idx} className="text-sm text-gray-300 bg-gray-800 p-3 rounded-lg border border-gray-700 border-l-4 border-l-blue-500 shadow-sm">
                  {item}
                </li>
              ))}
            </ul>
          </section>

        </div>
      </div>
    </div>
  );
}

export default FeedbackModal;
