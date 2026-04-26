import React, { useState } from 'react';
import { api } from './api.js';
import { StepBar, Skeleton, Toast } from './components.jsx';

const SAMPLE_JD = `We are looking for a Senior Python Engineer with:
- 4+ years of Python development experience
- Strong knowledge of FastAPI and REST API design
- PostgreSQL and database optimization skills
- AWS cloud services experience
- System design and distributed systems knowledge
- Docker and containerization experience`;

const SAMPLE_RESUME = `John Doe - Software Engineer
Experience: 3 years Python development
- Built REST APIs using Flask and FastAPI
- Worked with PostgreSQL and MySQL databases
- Basic AWS S3 and EC2 usage
- Used Git, Docker for development
- Strong Python fundamentals`;

export default function UploadPage({ onNext }) {
  const [jd, setJd] = useState('');
  const [resume, setResume] = useState('');
  const [name, setName] = useState('');
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState(null);

  const useSample = () => { setJd(SAMPLE_JD); setResume(SAMPLE_RESUME); setName('John Doe'); };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!jd.trim() || !resume.trim() || !name.trim()) {
      setToast({ message: 'Please fill in all fields.', type: 'error' }); return;
    }
    setLoading(true);
    try {
      const data = await api.upload({ candidate_name: name, jd_content: jd, resume_content: resume });
      onNext(data);
    } catch (err) {
      setToast({ message: err.message, type: 'error' });
    } finally { setLoading(false); }
  };

  return (
    <div className="animate-fade-in-up max-w-4xl mx-auto">
      {toast && <Toast {...toast} onDismiss={() => setToast(null)} />}
      <StepBar step={1} />

      <div className="glass rounded-2xl p-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="text-2xl font-bold gradient-text mb-1">Upload Documents</h2>
            <p className="text-slate-400 text-sm">Paste your JD and resume to begin AI-powered skill assessment</p>
          </div>
          <button onClick={useSample}
            className="text-xs bg-purple-500/20 hover:bg-purple-500/30 border border-purple-500/40 text-purple-300 px-4 py-2 rounded-lg transition font-medium">
            📋 Load Sample
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Candidate Name */}
          <div>
            <label className="block text-sm font-semibold text-slate-300 mb-2">👤 Candidate Name</label>
            <input value={name} onChange={e => setName(e.target.value)}
              placeholder="e.g. Shivam Yadav"
              className="w-full bg-slate-800/60 border border-slate-600 rounded-xl px-4 py-3 text-white placeholder-slate-500 text-sm" />
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            {/* JD */}
            <div>
              <label className="block text-sm font-semibold text-slate-300 mb-2">
                📋 Job Description
                <span className="ml-2 text-xs text-slate-500 font-normal">{jd.length} chars</span>
              </label>
              <textarea value={jd} onChange={e => setJd(e.target.value)} rows={12}
                placeholder="Paste the job description here..."
                className="w-full bg-slate-800/60 border border-slate-600 rounded-xl px-4 py-3 text-white placeholder-slate-500 text-sm" />
            </div>
            {/* Resume */}
            <div>
              <label className="block text-sm font-semibold text-slate-300 mb-2">
                📄 Resume / CV
                <span className="ml-2 text-xs text-slate-500 font-normal">{resume.length} chars</span>
              </label>
              <textarea value={resume} onChange={e => setResume(e.target.value)} rows={12}
                placeholder="Paste your resume here..."
                className="w-full bg-slate-800/60 border border-slate-600 rounded-xl px-4 py-3 text-white placeholder-slate-500 text-sm" />
            </div>
          </div>

          <button type="submit" disabled={loading}
            className="w-full py-4 rounded-xl font-bold text-white bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 disabled:opacity-50 disabled:cursor-not-allowed transition transform hover:scale-[1.01] flex items-center justify-center gap-3">
            {loading ? (
              <><div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />Analysing...</>
            ) : (
              <> 🚀 Start AI Assessment</>
            )}
          </button>
        </form>
      </div>
    </div>
  );
}
