import { useState, useEffect } from 'react';

function DomainSelector({ selectedDomain, onSelectDomain }) {
  const [domains, setDomains] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchDomains() {
      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/api/domains`);
        if (res.ok) {
          const data = await res.json();
          setDomains(data);
        }
      } catch (e) {
        console.error('Failed to fetch domains', e);
      } finally {
        setLoading(false);
      }
    }
    fetchDomains();
  }, []);

  return (
    <div className="mb-6 bg-gray-800/80 backdrop-blur-md rounded-2xl p-6 border border-gray-700 shadow-xl">
      <div className="flex justify-between items-center mb-4">
        <div>
          <h2 className="text-base font-semibold text-gray-200">Select Focus Domain</h2>
          <p className="text-xs text-gray-400">Choose a curriculum module to focus interview questions on</p>
        </div>
        <span className="text-xs font-medium px-2.5 py-1 rounded-full bg-indigo-900/60 text-indigo-300 border border-indigo-700/50">
          Optional
        </span>
      </div>

      {loading ? (
        <div className="text-xs text-gray-400 py-4 text-center">Loading domains...</div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
          {/* Default Option: Full Curriculum */}
          <div
            onClick={() => onSelectDomain(null)}
            className={`cursor-pointer p-3.5 rounded-xl border text-left transition-all ${
              selectedDomain === null
                ? 'bg-indigo-600/20 border-indigo-500 text-white shadow-lg shadow-indigo-950/40 ring-1 ring-indigo-500'
                : 'bg-gray-900/60 border-gray-700 text-gray-300 hover:border-gray-600 hover:bg-gray-900'
            }`}
          >
            <div className="flex items-center justify-between mb-1">
              <span className="text-xs font-semibold uppercase tracking-wider text-indigo-400">All Modules</span>
              {selectedDomain === null && (
                <span className="w-2 h-2 rounded-full bg-indigo-400 animate-pulse"></span>
              )}
            </div>
            <p className="text-sm font-medium">Any Domain / Full Curriculum</p>
            <p className="text-xs text-gray-400 mt-1">Draw questions across all 31 curriculum days</p>
          </div>

          {/* Module Options */}
          {domains.map((d) => {
            const isSelected = selectedDomain === d.number;
            return (
              <div
                key={d.number}
                onClick={() => onSelectDomain(d.number)}
                className={`cursor-pointer p-3.5 rounded-xl border text-left transition-all ${
                  isSelected
                    ? 'bg-indigo-600/20 border-indigo-500 text-white shadow-lg shadow-indigo-950/40 ring-1 ring-indigo-500'
                    : 'bg-gray-900/60 border-gray-700 text-gray-300 hover:border-gray-600 hover:bg-gray-900'
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs font-semibold uppercase tracking-wider text-gray-400">Module {d.number}</span>
                  <span className="text-[10px] text-gray-400 bg-gray-800 px-1.5 py-0.5 rounded">
                    Days {d.startDay}–{d.endDay} ({d.dayCount}d)
                  </span>
                </div>
                <p className="text-sm font-medium line-clamp-1">{d.title}</p>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default DomainSelector;
