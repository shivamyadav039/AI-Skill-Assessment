import React, { useState, useEffect } from 'react';
import { api } from './api.js';
import { StepBar, ScoreRing, SeverityBadge, Skeleton, Toast, levelLabel } from './components.jsx';

export default function ScoresPage({ session, scores: initialScores, onNext }) {
  const { session_id, jd_skills = [] } = session;
  const [gaps, setGaps]   = useState(null);
  const [loading, setLoading] = useState(true);
  const [toast, setToast] = useState(null);

  useEffect(() => {
    api.gaps(session_id)
      .then(d => setGaps(d))
      .catch(err => setToast({ message: err.message, type: 'error' }))
      .finally(() => setLoading(false));
  }, [session_id]);

  const scoresList = Object.entries(initialScores || {});
  const avgLevel = scoresList.length
    ? (scoresList.reduce((a, [, v]) => a + (v.assessed_level || 0), 0) / scoresList.length).toFixed(1)
    : 0;
  const readiness = gaps?.overall_readiness ?? (avgLevel / 5);

  return (
    <div className="animate-fade-in-up max-w-5xl mx-auto">
      {toast && <Toast {...toast} onDismiss={() => setToast(null)} />}
      <StepBar step={3} />

      {/* Overall readiness banner */}
      <div className="glass rounded-2xl p-6 mb-6 flex flex-col sm:flex-row items-center gap-6">
        <div className="relative flex-shrink-0">
          <svg width="120" height="120" viewBox="0 0 120 120">
            <circle cx="60" cy="60" r="52" fill="none" stroke="#1e293b" strokeWidth="10" />
            <circle cx="60" cy="60" r="52" fill="none"
              stroke="url(#grad)" strokeWidth="10"
              strokeDasharray={`${2 * Math.PI * 52}`}
              strokeDashoffset={`${2 * Math.PI * 52 * (1 - readiness)}`}
              strokeLinecap="round"
              style={{ transform: 'rotate(-90deg)', transformOrigin: '50% 50%', transition: 'stroke-dashoffset 1.4s ease' }} />
            <defs>
              <linearGradient id="grad" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" stopColor="#a855f7" />
                <stop offset="100%" stopColor="#ec4899" />
              </linearGradient>
            </defs>
            <text x="60" y="55" textAnchor="middle" fill="white" fontSize="22" fontWeight="800">
              {Math.round(readiness * 100)}%
            </text>
            <text x="60" y="72" textAnchor="middle" fill="#94a3b8" fontSize="10">Readiness</text>
          </svg>
        </div>
        <div className="text-center sm:text-left">
          <h2 className="text-2xl font-bold gradient-text mb-1">Assessment Complete!</h2>
          <p className="text-slate-200 text-sm mb-3 font-medium">
            You scored across <strong className="text-white">{scoresList.length}</strong> skills with an average proficiency of
            <strong className="text-purple-300"> Level {avgLevel}</strong> ({levelLabel(Math.round(Number(avgLevel)))})
          </p>
          <div className="flex flex-wrap gap-2">
            {scoresList.length > 0 && (
              <>
                <span className="text-xs px-3 py-1 rounded-full bg-green-500/15 text-green-400 border border-green-500/30">
                  ✓ {scoresList.filter(([,v]) => v.assessed_level >= 4).length} Strong Skills
                </span>
                <span className="text-xs px-3 py-1 rounded-full bg-red-500/15 text-red-400 border border-red-500/30">
                  ⚠ {scoresList.filter(([,v]) => v.assessed_level < 3).length} Needs Work
                </span>
              </>
            )}
          </div>
        </div>
      </div>

      <div className="grid lg:grid-cols-2 gap-6 mb-6">
        {/* Skill score cards */}
        <div className="space-y-3">
          <h3 className="font-bold text-white text-sm uppercase tracking-wide">Skill Scores</h3>
          {loading
            ? [1,2,3].map(i => <Skeleton key={i} className="h-24 rounded-xl" />)
            : scoresList.length === 0
              ? <div className="glass rounded-xl p-6 text-center text-slate-500 text-sm">No scores yet</div>
              : scoresList.map(([skill, s], i) => (
                <div key={i} className="glass-light rounded-xl p-4 flex items-center gap-4 animate-fade-in-up"
                  style={{ animationDelay: `${i * 0.08}s` }}>
                  <ScoreRing score={s.assessed_level} size={72} />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-1">
                      <p className="font-bold text-sm text-white truncate">{skill}</p>
                      <span className="text-xs text-slate-200 font-medium flex-shrink-0">{(s.confidence * 100).toFixed(0)}% conf.</span>
                    </div>
                    <p className="text-xs text-purple-300 font-bold mb-2">{levelLabel(s.assessed_level)}</p>
                    {/* Evidence tags */}
                    <div className="flex flex-wrap gap-1">
                      {(s.evidence_tags || []).slice(0, 3).map((t, j) => (
                        <span key={j} className="text-xs bg-slate-700 text-slate-200 px-2 py-0.5 rounded-full font-medium border border-slate-500">{t}</span>
                      ))}
                    </div>
                    {/* Confidence bar */}
                    <div className="w-full bg-slate-700 rounded-full h-1 mt-2">
                      <div className="h-1 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 animate-progress"
                        style={{ width: `${s.confidence * 100}%` }} />
                    </div>
                  </div>
                </div>
              ))}
        </div>

        {/* Gap analysis */}
        <div className="space-y-3">
          <h3 className="font-bold text-white text-sm uppercase tracking-wide">Gap Analysis</h3>
          {loading
            ? [1,2,3].map(i => <Skeleton key={i} className="h-20 rounded-xl" />)
            : !gaps || (gaps.gaps || []).length === 0
              ? <div className="glass rounded-xl p-6 text-center text-green-400 text-sm">🎉 No critical gaps found!</div>
              : (gaps.gaps || []).map((g, i) => (
                <div key={i} className="glass-light rounded-xl p-4 animate-fade-in-up"
                  style={{ animationDelay: `${i * 0.08}s` }}>
                  <div className="flex items-center justify-between mb-2">
                    <p className="font-bold text-sm text-white">{g.skill}</p>
                    <SeverityBadge severity={g.gap_severity || 'medium'} />
                  </div>
                  <div className="flex items-center gap-4 text-xs text-slate-400">
                    <span>Required: <strong className="text-white">L{g.jd_required_level}</strong></span>
                    <span>Assessed: <strong className="text-purple-200">L{g.assessed_level}</strong></span>
                    <span>Gap: <strong className="text-red-300">{g.jd_required_level - g.assessed_level} levels</strong></span>
                  </div>
                  {/* Gap bar */}
                  <div className="flex gap-1 mt-2">
                    {[1,2,3,4,5].map(lvl => (
                      <div key={lvl} className={`h-1.5 flex-1 rounded-full ${lvl <= g.assessed_level ? 'bg-purple-500' : lvl <= g.jd_required_level ? 'bg-red-500/40' : 'bg-slate-700'}`} />
                    ))}
                  </div>
                </div>
              ))}
        </div>
      </div>

      <button onClick={onNext}
        className="w-full py-4 rounded-xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white transition transform hover:scale-[1.01] flex items-center justify-center gap-2">
        🗺️ Generate My Learning Plan →
      </button>
    </div>
  );
}
