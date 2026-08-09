function ProgressPanel({ candidate, questionCount, isDone, progress }) {
  if (!candidate) return <div className="text-gray-500 text-sm">Loading candidate...</div>;

  // Use server progress or derive fallback values
  let derivedPhase = "Warm-up";
  if (questionCount >= 2) derivedPhase = "Core Technical";
  if (questionCount >= 4) derivedPhase = "Deep Dive";
  if (questionCount >= 6) derivedPhase = "Production";
  if (questionCount >= 7) derivedPhase = "Final";

  const phase = isDone ? "Completed" : (progress?.phase || derivedPhase);
  const currentQ = progress?.question_count ?? questionCount;
  const maxQ = progress?.max_questions ?? 15;
  const topicsCovered = progress?.topics_covered || [];

  return (
    <div className="flex flex-col space-y-6">
      <div>
        <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-2">Candidate Context</h2>
        <div className="card p-4">
          <div className="flex items-center gap-3">
            <div className="avatar" style={{background:'#7c3aed'}}>{candidate.member.name.split(' ').map(n=>n[0]).slice(0,2).join('')}</div>
            <div>
              <p className="text-base font-medium text-gray-200">{candidate.member.name}</p>
              <p className="text-xs text-gray-400 mt-1">{candidate.member.jobRole} · {candidate.member.yearsExperience} yrs</p>
            </div>
          </div>
        </div>
      </div>

      <div>
        <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-2">Interview Status</h2>
        <div className="card p-4 space-y-3">
          
          <div>
            <div className="flex justify-between text-xs mb-1 text-gray-400">
              <span>Phase</span>
              <span className="text-indigo-400 font-medium">{phase}</span>
            </div>
            <div className="w-full bg-gray-800 rounded-full h-2">
              <div 
                className="bg-gradient-to-r from-indigo-500 to-purple-500 h-2 rounded-full transition-all duration-500" 
                style={{ width: `${Math.min((currentQ / maxQ) * 100, 100)}%` }}
              ></div>
            </div>
          </div>

          <div className="pt-2 flex justify-between items-center border-t border-gray-700">
            <span className="text-xs text-gray-400">Questions</span>
            <span className="text-sm font-medium text-gray-200">Question {currentQ} of ~{maxQ}</span>
          </div>

          <div className="pt-2 flex justify-between items-center border-t border-gray-700">
            <span className="text-xs text-gray-400">Days Covered</span>
            <span className="text-sm font-medium text-indigo-300">{topicsCovered.length} day{topicsCovered.length === 1 ? '' : 's'}</span>
          </div>

        </div>
      </div>

      <div>
        <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-2">Cohort Signals</h2>
          <div className="card p-4">
            <ul className="space-y-2 text-xs text-gray-400">
             <li className="flex justify-between">
                <span>Completed Missions</span>
                <span className="text-gray-200">{candidate.signals.missionsCompleted}/31</span>
             </li>
             <li className="flex justify-between">
                <span>First-try Passes</span>
                <span className="text-gray-200">{candidate.signals.missionsFirstTry}</span>
             </li>
           </ul>
        </div>
      </div>

    </div>
  );
}

export default ProgressPanel;

