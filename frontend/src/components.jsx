import React from 'react';

/* ── Step progress bar at top of page ── */
export function StepBar({ step }) {
  const steps = ['Upload', 'Assessment', 'Scores', 'Learning Plan'];
  return (
    <div className="flex items-center justify-center gap-0 mb-10">
      {steps.map((label, i) => {
        const idx = i + 1;
        const done = step > idx;
        const active = step === idx;
        return (
          <React.Fragment key={i}>
            <div className="flex flex-col items-center">
              <div className={`w-9 h-9 rounded-full flex items-center justify-center text-sm font-bold border-2 transition-all duration-500
                ${done   ? 'bg-purple-500 border-purple-500 text-white'
                : active ? 'bg-slate-900 border-purple-400 text-purple-300 animate-pulse-glow'
                :          'bg-slate-800 border-slate-600 text-slate-500'}`}>
                {done ? '✓' : idx}
              </div>
              <span className={`text-xs mt-1 font-bold transition-colors duration-300
                ${active ? 'text-purple-200' : done ? 'text-purple-400' : 'text-slate-400'}`}>
                {label}
              </span>
            </div>
            {i < steps.length - 1 && (
              <div className={`h-0.5 w-16 sm:w-24 mx-1 mb-5 transition-all duration-700
                ${step > idx ? 'bg-purple-500' : 'bg-slate-700'}`} />
            )}
          </React.Fragment>
        );
      })}
    </div>
  );
}

/* ── Typing indicator (AI thinking) ── */
export function TypingIndicator() {
  return (
    <div className="flex items-end gap-2 animate-fade-in">
      <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-sm flex-shrink-0">🤖</div>
      <div className="glass-light rounded-2xl rounded-bl-sm px-4 py-3 flex gap-1.5 items-center">
        <span className="typing-dot w-2 h-2 bg-purple-400 rounded-full block" />
        <span className="typing-dot w-2 h-2 bg-purple-400 rounded-full block" />
        <span className="typing-dot w-2 h-2 bg-purple-400 rounded-full block" />
      </div>
    </div>
  );
}

/* ── Score ring SVG ── */
export function ScoreRing({ score, max = 5, size = 80 }) {
  const pct = score / max;
  const r = 36; const circ = 2 * Math.PI * r;
  const offset = circ * (1 - pct);
  const color = score >= 4 ? '#4ade80' : score >= 3 ? '#facc15' : score >= 2 ? '#fb923c' : '#f87171';
  return (
    <svg width={size} height={size} viewBox="0 0 80 80">
      <circle cx="40" cy="40" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
      <circle cx="40" cy="40" r={r} fill="none" stroke={color} strokeWidth="8"
        strokeDasharray={circ} strokeDashoffset={offset}
        strokeLinecap="round"
        style={{ transform: 'rotate(-90deg)', transformOrigin: '50% 50%', transition: 'stroke-dashoffset 1.2s ease' }} />
      <text x="40" y="44" textAnchor="middle" fill={color} fontSize="18" fontWeight="700">{score}</text>
    </svg>
  );
}

/* ── Severity badge ── */
export function SeverityBadge({ severity }) {
  const map = {
    critical: 'badge-critical', high: 'badge-high',
    medium: 'badge-medium',    low: 'badge-low',
  };
  return (
    <span className={`text-xs px-2 py-0.5 rounded-full font-semibold uppercase ${map[severity] || 'badge-low'}`}>
      {severity}
    </span>
  );
}

/* ── Toast notification ── */
export function Toast({ message, type = 'error', onDismiss }) {
  const colors = {
    error:   'border-red-500/40 bg-red-500/10 text-red-300',
    success: 'border-green-500/40 bg-green-500/10 text-green-300',
    info:    'border-purple-500/40 bg-purple-500/10 text-purple-300',
  };
  React.useEffect(() => {
    const t = setTimeout(onDismiss, 4000);
    return () => clearTimeout(t);
  }, [onDismiss]);
  return (
    <div className={`toast glass rounded-xl p-4 border ${colors[type]} flex items-start gap-3`}>
      <span className="text-lg">{type === 'error' ? '⚠️' : type === 'success' ? '✅' : 'ℹ️'}</span>
      <p className="text-sm flex-1">{message}</p>
      <button onClick={onDismiss} className="text-slate-500 hover:text-white ml-2">✕</button>
    </div>
  );
}

/* ── Skeleton loader ── */
export function Skeleton({ className = '' }) {
  return <div className={`skeleton ${className}`} />;
}

/* ── Level label helper ── */
export function levelLabel(n) {
  return ['', 'Beginner', 'Basic', 'Intermediate', 'Advanced', 'Expert'][n] || '—';
}
