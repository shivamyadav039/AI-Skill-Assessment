import React, { useState, useEffect } from 'react';
import './App.css';
import UploadPage from './UploadPage';
import AssessmentPage from './AssessmentPage';
import ScoresPage from './ScoresPage';
import PlanPage from './PlanPage';

/* ── Home / Landing Page ── */
function HomePage({ onStart }) {
  const features = [
    { icon: '📄', title: 'Smart Skill Extraction', desc: 'NLP parses your JD & Resume to find exact skill gaps automatically.' },
    { icon: '🤖', title: 'AI Interviewer', desc: 'NVIDIA NIM asks adaptive questions across 3 difficulty levels per skill.' },
    { icon: '📊', title: 'Evidence Scoring', desc: '4-dimension scoring: Relevance, Depth, Clarity & Confidence.' },
    { icon: '🗺️', title: 'Learning Roadmap', desc: 'Personalized week-by-week plan with curated resources to close gaps.' },
  ];
  const stats = [
    { val: '4', label: 'AI Agents', color: 'from-purple-400 to-violet-500' },
    { val: '4D', label: 'Scoring Dims', color: 'from-pink-400 to-rose-500' },
    { val: '5', label: 'Turns / Skill', color: 'from-blue-400 to-cyan-500' },
    { val: '∞', label: 'Skills', color: 'from-emerald-400 to-teal-500' },
  ];
  const steps = [
    { icon: '📋', label: 'Upload JD + Resume' },
    { icon: '🔍', label: 'AI Extracts Gaps' },
    { icon: '💬', label: 'Live Interview' },
    { icon: '🗺️', label: 'Get Roadmap' },
  ];

  return (
    <div className="animate-fade-in max-w-5xl mx-auto px-4 py-12">
      {/* Hero */}
      <div className="text-center mb-16">
        <div className="inline-flex items-center gap-2 bg-purple-500/10 border border-purple-500/30 rounded-full px-4 py-1.5 text-sm text-purple-300 font-medium mb-6">
          ✨ Powered by NVIDIA NIM AI
        </div>
        <h2 className="text-5xl sm:text-6xl font-black mb-5 leading-tight">
          Prove Your Skills,<br />
          <span className="bg-gradient-to-r from-purple-400 via-pink-400 to-rose-400 bg-clip-text text-transparent">
            Not Just Claims
          </span>
        </h2>
        <p className="text-slate-300 text-lg max-w-2xl mx-auto mb-10 leading-relaxed">
          AI-powered conversational assessment that tests real proficiency from any JD + Resume,
          then generates a personalized learning roadmap to close the gaps.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={onStart}
            className="px-10 py-4 rounded-2xl font-bold text-white text-lg bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 transition-all transform hover:scale-105 shadow-xl shadow-purple-900/40"
          >
            🚀 Start Free Assessment
          </button>
          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noopener noreferrer"
            className="px-10 py-4 rounded-2xl font-bold text-slate-300 text-lg border border-slate-600 hover:border-purple-500/60 hover:text-white transition-all hover:bg-slate-800/50"
          >
            📖 View API Docs
          </a>
        </div>
        <p className="text-slate-500 text-sm mt-5">No signup required · Free to use · Open Source</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-14">
        {stats.map((s, i) => (
          <div key={i} className="bg-slate-800/50 border border-slate-700/50 rounded-2xl p-5 text-center hover:border-purple-500/40 transition-all hover:-translate-y-0.5">
            <div className={`text-3xl font-black mb-1 bg-gradient-to-r ${s.color} bg-clip-text text-transparent`}>{s.val}</div>
            <div className="text-xs text-slate-400 font-semibold uppercase tracking-wider">{s.label}</div>
          </div>
        ))}
      </div>

      {/* How it works */}
      <div className="mb-14">
        <h3 className="text-xl font-bold text-center mb-2 text-white">How It Works</h3>
        <p className="text-center text-slate-400 text-sm mb-8">Four simple steps to your personalised learning plan</p>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {steps.map((s, i) => (
            <div key={i} className="relative bg-slate-800/40 border border-slate-700/40 rounded-xl p-5 text-center hover:border-purple-500/40 transition-all group">
              {i < steps.length - 1 && (
                <div className="hidden sm:block absolute top-1/2 -right-2 text-slate-600 text-lg z-10">→</div>
              )}
              <div className="text-3xl mb-3 group-hover:scale-110 transition-transform">{s.icon}</div>
              <div className="text-xs font-bold text-purple-400 mb-1">Step {i + 1}</div>
              <div className="text-sm font-semibold text-white">{s.label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Features */}
      <div className="mb-14">
        <h3 className="text-xl font-bold text-center mb-2 text-white">Key Features</h3>
        <p className="text-center text-slate-400 text-sm mb-8">Everything you need for a comprehensive skill assessment</p>
        <div className="grid sm:grid-cols-2 gap-4">
          {features.map((f, i) => (
            <div key={i} className="bg-slate-800/40 border border-slate-700/40 rounded-xl p-5 flex gap-4 hover:border-purple-500/30 transition-all group">
              <div className="text-3xl flex-shrink-0 group-hover:scale-110 transition-transform">{f.icon}</div>
              <div>
                <h4 className="font-bold mb-1 text-white">{f.title}</h4>
                <p className="text-sm text-slate-400 leading-relaxed">{f.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* CTA Banner */}
      <div className="bg-gradient-to-r from-purple-900/40 to-pink-900/40 border border-purple-500/30 rounded-2xl p-10 text-center">
        <h3 className="text-2xl font-bold mb-2 text-white">Ready to get assessed?</h3>
        <p className="text-slate-400 text-sm mb-7">Paste your JD + Resume and let AI do the rest. Takes less than 10 minutes.</p>
        <button
          onClick={onStart}
          className="px-10 py-4 rounded-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white transition-all transform hover:scale-105 shadow-lg shadow-purple-900/40"
        >
          🚀 Start Assessment Now
        </button>
      </div>
    </div>
  );
}

export default function App() {
  const [step, setStep] = useState(0);   // 0=home 1=upload 2=assess 3=scores 4=plan
  const [session, setSession] = useState(null);
  const [scores, setScores] = useState({});
  const [health, setHealth] = useState(null);

  useEffect(() => {
    fetch('/health')
      .then(r => r.json())
      .then(() => setHealth(true))
      .catch(() => setHealth(false));
  }, []);

  const handleRestart = () => {
    setStep(0);
    setSession(null);
    setScores({});
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white">
      {/* Background Elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 right-20 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl"></div>
        <div className="absolute bottom-20 left-20 w-96 h-96 bg-pink-500/10 rounded-full blur-3xl"></div>
      </div>

      <div className="relative z-10">
        {/* Header */}
        <header className="backdrop-blur-md bg-slate-900/80 border-b border-purple-500/20 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <button onClick={handleRestart} className="flex items-center gap-3 hover:opacity-80 transition">
                <div className="w-12 h-12 bg-gradient-to-br from-purple-400 to-pink-500 rounded-lg flex items-center justify-center font-bold text-lg">
                  ⚡
                </div>
                <div>
                  <h1 className="text-2xl font-bold">AI Skill Assessment</h1>
                  <p className="text-sm text-purple-300">Powered by NVIDIA NIM</p>
                </div>
              </button>
              <div className="flex items-center gap-3">
                {step > 0 && (
                  <button
                    onClick={handleRestart}
                    className="text-xs text-slate-400 hover:text-white transition px-3 py-1.5 rounded-lg hover:bg-slate-800 border border-transparent hover:border-slate-600"
                  >
                    ← Home
                  </button>
                )}
                <div className={`inline-flex items-center gap-2 border rounded-lg px-4 py-2 text-sm font-semibold
                  ${health === null ? 'border-slate-600 text-slate-400'
                    : health ? 'bg-green-500/20 border-green-500/50 text-green-300'
                      : 'bg-red-500/20 border-red-500/50 text-red-300'}`}>
                  <span className={`w-2 h-2 rounded-full ${health === null ? 'bg-slate-500' : health ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`} />
                  {health === null ? 'Checking…' : health ? '✓ API Online' : '✗ API Offline'}
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Pages */}
        <main className="max-w-6xl mx-auto px-4 py-8">
          {step === 0 && (
            <HomePage onStart={() => setStep(1)} />
          )}
          {step === 1 && (
            <UploadPage onNext={(data) => { setSession(data); setStep(2); }} />
          )}
          {step === 2 && session && (
            <AssessmentPage
              session={session}
              onNext={(s) => { setScores(s || {}); setStep(3); }}
            />
          )}
          {step === 3 && session && (
            <ScoresPage
              session={session}
              scores={scores}
              onNext={() => setStep(4)}
            />
          )}
          {step === 4 && session && (
            <PlanPage session={session} onRestart={handleRestart} />
          )}
        </main>

        {/* Footer */}
        <footer className="border-t border-purple-500/20 bg-slate-900/50 py-12 mt-20">
          <div className="max-w-7xl mx-auto px-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
              <div>
                <h3 className="font-semibold mb-3">Features</h3>
                <ul className="text-sm text-gray-400 space-y-2">
                  <li>✓ Multi-turn Assessment</li>
                  <li>✓ NLP Evaluation</li>
                  <li>✓ Learning Plans</li>
                </ul>
              </div>
              <div>
                <h3 className="font-semibold mb-3">Services</h3>
                <ul className="text-sm text-gray-400 space-y-2">
                  <li>• Skill Extraction</li>
                  <li>• Response Scoring</li>
                  <li>• Gap Analysis</li>
                </ul>
              </div>
              <div>
                <h3 className="font-semibold mb-3">Agents</h3>
                <ul className="text-sm text-gray-400 space-y-2">
                  <li>• Assessment Agent</li>
                  <li>• Scoring Agent</li>
                  <li>• Planning Agent</li>
                </ul>
              </div>
              <div>
                <h3 className="font-semibold mb-3">Info</h3>
                <ul className="text-sm text-gray-400 space-y-2">
                  <li>📖 <a href="#" className="hover:text-purple-400">Docs</a></li>
                  <li>🚀 <a href="#" className="hover:text-purple-400">API</a></li>
                  <li>💾 <a href="#" className="hover:text-purple-400">Status</a></li>
                </ul>
              </div>
            </div>

            <div className="border-t border-purple-500/10 pt-8 text-center text-sm text-gray-500">
              <p>Built with ❤️ for Hackathon Deccan • Powered by NVIDIA NIM • FastAPI Backend</p>
              <p className="mt-2">© 2026 AI Skill Assessment • All Rights Reserved</p>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
}
