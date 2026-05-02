import React, { useState, useEffect } from 'react';
import { api } from './api.js';
import { StepBar, Skeleton, Toast } from './components.jsx';

export default function PlanPage({ session, onRestart }) {
  const { session_id } = session;
  const [plan, setPlan]     = useState(null);
  const [loading, setLoading] = useState(true);
  const [toast, setToast]   = useState(null);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    api.plan({ session_id })
      .then(d => setPlan(d))
      .catch(err => setToast({ message: err.message, type: 'error' }))
      .finally(() => setLoading(false));
  }, [session_id]);

  const copyPlan = () => {
    const text = plan?.summary || '';
    navigator.clipboard.writeText(text).then(() => { setCopied(true); setTimeout(() => setCopied(false), 2000); });
  };

  if (loading) return (
    <div className="animate-fade-in-up max-w-4xl mx-auto">
      <StepBar step={4} />
      <div className="glass rounded-2xl p-8 space-y-4">
        <div className="text-center mb-6">
          <div className="w-16 h-16 mx-auto rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-3xl animate-spin-slow mb-4">🧭</div>
          <p className="text-loading text-slate-200 font-medium">Generating your personalized learning plan…</p>
        </div>
        {[1,2,3,4].map(i => <Skeleton key={i} className="h-16 rounded-xl" />)}
      </div>
    </div>
  );

  const lp = plan?.learning_plan;
  const milestones = lp?.milestones || [];
  const prioritySkills = lp?.priority_skills || [];
  const adjacentSkills = lp?.adjacent_skills || [];

  return (
    <div className="animate-fade-in-up max-w-4xl mx-auto">
      {toast && <Toast {...toast} onDismiss={() => setToast(null)} />}
      <StepBar step={4} />

      {/* Header */}
      <div className="glass rounded-2xl p-6 mb-6 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold gradient-text mb-1">Your Learning Roadmap</h2>
          <p className="text-slate-200 text-sm font-medium">
            {lp?.total_duration_weeks
              ? `${lp.total_duration_weeks}-week plan · ${milestones.length} milestones`
              : 'Personalized plan ready'}
          </p>
        </div>
        <div className="flex gap-2">
          <button onClick={copyPlan}
            className="text-xs px-4 py-2 rounded-lg bg-slate-700 hover:bg-slate-600 text-slate-300 transition border border-slate-600 flex items-center gap-1">
            {copied ? '✓ Copied!' : '📋 Copy'}
          </button>
          <button onClick={onRestart}
            className="text-xs px-4 py-2 rounded-lg bg-purple-600/30 hover:bg-purple-600/50 text-purple-300 transition border border-purple-500/40">
            🔄 New Assessment
          </button>
        </div>
      </div>

      {/* Summary box */}
      {plan?.summary && (
        <div className="glass-light rounded-xl p-5 mb-6 border-l-4 border-purple-500">
          <h3 className="text-sm font-bold text-white mb-2">📋 Summary</h3>
          <pre className="text-sm text-slate-100 whitespace-pre-wrap leading-relaxed font-sans font-medium">{plan.summary}</pre>
        </div>
      )}

      <div className="grid md:grid-cols-2 gap-6 mb-6">
        {/* Priority skills */}
        {prioritySkills.length > 0 && (
          <div className="glass rounded-xl p-5">
            <h3 className="text-sm font-bold text-white uppercase mb-3">🎯 Priority Skills</h3>
            <div className="space-y-2">
              {prioritySkills.map((s, i) => (
                <div key={i} className="flex items-center gap-3 animate-fade-in-up" style={{ animationDelay: `${i*0.1}s` }}>
                  <div className="w-6 h-6 rounded-full bg-red-500/20 border border-red-500/40 text-red-400 text-xs flex items-center justify-center font-bold">{i+1}</div>
                  <span className="text-sm text-white font-semibold">{s}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Adjacent skills */}
        {adjacentSkills.length > 0 && (
          <div className="glass rounded-xl p-5">
            <h3 className="text-sm font-bold text-white uppercase mb-3">🌱 Adjacent Skills to Explore</h3>
            <div className="flex flex-wrap gap-2">
              {adjacentSkills.map((s, i) => (
                <span key={i} className="text-sm px-3 py-1.5 rounded-full bg-blue-500/20 text-blue-200 border border-blue-400/40 font-semibold animate-fade-in"
                  style={{ animationDelay: `${i*0.1}s` }}>{s}</span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Timeline milestones */}
      {milestones.length > 0 && (
        <div className="glass rounded-2xl p-6 mb-6">
          <h3 className="text-sm font-bold text-white uppercase mb-5">📅 Week-by-Week Milestones</h3>
          <div className="relative">
            {/* Timeline line */}
            <div className="absolute left-4 top-0 bottom-0 w-0.5 bg-gradient-to-b from-purple-500 via-pink-500 to-transparent" />
            <div className="space-y-6">
              {milestones.map((m, i) => (
                <div key={i} className="pl-10 relative animate-fade-in-up" style={{ animationDelay: `${i*0.12}s` }}>
                  {/* Circle */}
                  <div className="absolute left-0 top-0 w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-xs font-bold z-10">
                    W{m.week || i+1}
                  </div>
                  <div className="glass-light rounded-xl p-4">
                    <div className="flex items-start justify-between gap-2 mb-2">
                      <h4 className="font-bold text-sm text-purple-200">{m.skill || `Skill ${i+1}`}</h4>
                      {m.estimated_hours && (
                        <span className="text-xs text-slate-400 flex-shrink-0">⏱ {m.estimated_hours}h</span>
                      )}
                    </div>
                    {m.objective && <p className="text-sm text-slate-100 mb-3 font-medium">{m.objective}</p>}

                    {/* Resources */}
                    {(m.resources || []).length > 0 && (
                      <div className="mb-2">
                        <p className="text-xs text-slate-200 font-semibold mb-1">📚 Resources</p>
                        <div className="space-y-1.5">
                          {m.resources.slice(0, 3).map((r, j) => {
                            const rObj = typeof r === 'string' ? { title: r } : r;
                            const typeIcon = { course: '🎓', book: '📖', project: '🛠️', practice: '💻', tutorial: '📝' }[rObj.resource_type] || '📌';
                            return (
                              <div key={j} className="flex items-start gap-2 text-xs">
                                <span className="flex-shrink-0 mt-0.5">{typeIcon}</span>
                                <div className="min-w-0">
                                  <span className="text-sm text-slate-100 font-medium">{rObj.title}</span>
                                  {rObj.estimated_duration_hours && (
                                    <span className="ml-2 text-slate-500 text-xs">⏱ {rObj.estimated_duration_hours}h</span>
                                  )}
                                </div>
                              </div>
                            );
                          })}
                        </div>
                      </div>
                    )}

                    {/* Assessment criteria */}
                    {(m.assessment_criteria || []).length > 0 && (
                      <div>
                        <p className="text-xs text-slate-200 font-semibold mb-1">✅ Success Criteria</p>
                        {m.assessment_criteria.slice(0, 2).map((c, j) => (
                          <p key={j} className="text-sm text-green-300 font-medium">• {typeof c === 'string' ? c : JSON.stringify(c)}</p>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* CTA */}
      <div className="glass rounded-2xl p-6 text-center">
        <p className="text-slate-200 text-sm mb-4 font-medium">Ready to start your learning journey? 🚀</p>
        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <button onClick={onRestart}
            className="px-8 py-3 rounded-xl font-semibold bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white transition transform hover:scale-105">
            🔄 Assess Another Candidate
          </button>
          <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer"
            className="px-8 py-3 rounded-xl font-semibold bg-slate-700 hover:bg-slate-600 text-slate-300 transition border border-slate-600">
            📖 View API Docs
          </a>
        </div>
      </div>
    </div>
  );
}
