import React, { useState, useEffect } from 'react';
import './App.css';
import UploadPage     from './UploadPage.jsx';
import AssessmentPage from './AssessmentPage.jsx';
import ScoresPage     from './ScoresPage.jsx';
import PlanPage       from './PlanPage.jsx';

/* ── Background blobs ── */
function Blobs() {
  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
      <div className="absolute top-10 right-10 w-[500px] h-[500px] bg-purple-600/8 rounded-full blur-3xl animate-float" />
      <div className="absolute bottom-10 left-10 w-[400px] h-[400px] bg-pink-600/8 rounded-full blur-3xl animate-float" style={{ animationDelay: '1.5s' }} />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[300px] bg-blue-600/5 rounded-full blur-3xl" />
    </div>
  );
}

/* ── Header ── */
function Header({ step, onHome }) {
  const [health, setHealth] = useState(null);
  useEffect(() => {
    fetch('/health').then(r => r.json()).then(() => setHealth(true)).catch(() => setHealth(false));
  }, []);

  return (
    <header className="sticky top-0 z-50 backdrop-blur-xl bg-slate-900/80 border-b border-purple-500/15">
      <div className="max-w-6xl mx-auto px-6 py-3 flex items-center justify-between">
        <button onClick={onHome} className="flex items-center gap-3 hover:opacity-80 transition group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-lg font-bold group-hover:scale-105 transition">
            🧠
          </div>
          <div>
            <h1 className="text-lg font-bold leading-tight">AI Skill Assessment</h1>
            <p className="text-xs text-purple-300 leading-tight">Powered by Gemini</p>
          </div>
        </button>

        <div className="flex items-center gap-3">
          {step > 1 && (
            <button onClick={onHome}
              className="text-xs text-slate-400 hover:text-white transition px-3 py-1.5 rounded-lg hover:bg-slate-800 border border-transparent hover:border-slate-600">
              ← New Assessment
            </button>
          )}
          <div className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border text-xs font-medium
            ${health === null ? 'border-slate-700 text-slate-500'
            : health ? 'border-green-500/40 bg-green-500/10 text-green-400'
            : 'border-red-500/40 bg-red-500/10 text-red-400'}`}>
            <span className={`w-2 h-2 rounded-full ${health === null ? 'bg-slate-600' : health ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`} />
            {health === null ? 'Checking…' : health ? 'API Online' : 'API Offline'}
          </div>
        </div>
      </div>
    </header>
  );
}

/* ── Landing / Home page ── */
function HomePage({ onStart }) {
  const features = [
    { icon: '📄', title: 'Smart Skill Extraction', desc: 'NLP analyses JD + Resume to find exact skill gaps' },
    { icon: '🤖', title: 'AI Interviewer', desc: 'Gemini asks adaptive questions across 3 difficulty turns' },
    { icon: '📊', title: 'Evidence Scoring', desc: '4-dimension scoring: Relevance, Depth, Clarity, Confidence' },
    { icon: '🗺️', title: 'Learning Roadmap', desc: 'Personalized week-by-week plan with curated resources' },
  ];
  const stats = [
    { val: '4', label: 'AI Agents', color: 'text-purple-400' },
    { val: '4D', label: 'Scoring Dims', color: 'text-pink-400' },
    { val: '5', label: 'Turns/Skill', color: 'text-blue-400' },
    { val: '∞', label: 'Skills', color: 'text-green-400' },
  ];

  return (
    <div className="animate-fade-in-up max-w-5xl mx-auto">
      {/* Hero */}
      <div className="text-center py-16">
        <div className="inline-block text-7xl mb-6 animate-float">🧠</div>
        <h2 className="text-5xl sm:text-6xl font-black mb-4 leading-tight">
          Prove Skills,<br />
          <span className="gradient-text">Not Just Claims</span>
        </h2>
        <p className="text-slate-400 text-lg max-w-2xl mx-auto mb-8">
          AI-powered conversational assessment that tests real proficiency from any JD + Resume,
          then generates a personalized learning roadmap to close the gaps.
        </p>
        <button onClick={onStart}
          className="px-10 py-4 rounded-2xl font-bold text-white text-lg bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 transition transform hover:scale-105 shadow-xl shadow-purple-900/40 animate-pulse-glow">
          Start Free Assessment →
        </button>
        <p className="text-slate-500 text-xs mt-4">No signup required · Powered by Google Gemini</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4 mb-12 stagger">
        {stats.map((s, i) => (
          <div key={i} className="glass rounded-2xl p-5 text-center animate-fade-in-up">
            <div className={`text-3xl font-black mb-1 ${s.color}`}>{s.val}</div>
            <div className="text-xs text-slate-400">{s.label}</div>
          </div>
        ))}
      </div>

      {/* How it works */}
      <div className="mb-12">
        <h3 className="text-xl font-bold text-center mb-6 text-slate-300">How It Works</h3>
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 stagger">
          {['Upload JD + Resume', 'AI Extracts Gaps', 'Live Interview', 'Get Roadmap'].map((t, i) => (
            <div key={i} className="glass rounded-xl p-5 text-center animate-fade-in-up relative overflow-hidden group hover:border-purple-500/40 transition border border-purple-500/10">
              <div className="text-3xl mb-3">{['📋','🔍','💬','🗺️'][i]}</div>
              <div className="text-xs font-bold text-purple-400 mb-1">Step {i+1}</div>
              <div className="text-sm font-semibold text-slate-200">{t}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Features */}
      <div className="grid sm:grid-cols-2 gap-4 mb-12 stagger">
        {features.map((f, i) => (
          <div key={i} className="glass-light rounded-xl p-5 flex gap-4 animate-fade-in-up hover:border-purple-500/30 border border-transparent transition group">
            <div className="text-3xl flex-shrink-0 group-hover:scale-110 transition">{f.icon}</div>
            <div>
              <h4 className="font-semibold mb-1 text-slate-200">{f.title}</h4>
              <p className="text-xs text-slate-400 leading-relaxed">{f.desc}</p>
            </div>
          </div>
        ))}
      </div>

      {/* CTA banner */}
      <div className="glass rounded-2xl p-8 text-center border border-purple-500/20">
        <h3 className="text-2xl font-bold mb-2">Ready to get started?</h3>
        <p className="text-slate-400 text-sm mb-6">Load sample documents or paste your own JD + Resume in seconds</p>
        <button onClick={onStart}
          className="px-8 py-3 rounded-xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white transition transform hover:scale-105">
          🚀 Launch Assessment
        </button>
      </div>
    </div>
  );
}

/* ── Root App ── */
export default function App() {
  const [step, setStep]       = useState(0);   // 0=home 1=upload 2=assess 3=scores 4=plan
  const [session, setSession] = useState(null);
  const [scores, setScores]   = useState({});

  const restart = () => { setStep(0); setSession(null); setScores({}); };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950/30 to-slate-950 text-white">
      <Blobs />
      <div className="relative z-10">
        <Header step={step} onHome={restart} />
        <main className="max-w-6xl mx-auto px-4 py-8">
          {step === 0 && <HomePage onStart={() => setStep(1)} />}
          {step === 1 && (
            <UploadPage onNext={(data) => { setSession(data); setStep(2); }} />
          )}
          {step === 2 && session && (
            <AssessmentPage
              session={session}
              onNext={(s) => { if (s) setScores(s); setStep(3); }}
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
            <PlanPage session={session} onRestart={restart} />
          )}
        </main>

        {/* Footer */}
        <footer className="border-t border-slate-800 mt-16 py-6 text-center text-xs text-slate-600">
          <p>Built by <a href="https://github.com/shivamyadav039" className="text-purple-500 hover:text-purple-400 transition">Shivam Yadav</a> · Powered by Google Gemini · FastAPI Backend</p>
          <div className="flex justify-center gap-6 mt-3">
            <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer" className="hover:text-purple-400 transition">API Docs</a>
            <a href="http://localhost:8000/health" target="_blank" rel="noopener noreferrer" className="hover:text-purple-400 transition">Health</a>
            <a href="https://github.com/shivamyadav039/AI-Skill-Assessment" target="_blank" rel="noopener noreferrer" className="hover:text-purple-400 transition">GitHub</a>
          </div>
        </footer>
      </div>
    </div>
  );
}
