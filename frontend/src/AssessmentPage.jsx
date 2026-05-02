import React, { useState, useEffect, useRef } from 'react';
import { api } from './api.js';
import { StepBar, TypingIndicator, Toast } from './components.jsx';

export default function AssessmentPage({ session, onNext }) {
  const { session_id, jd_skills = [], resume_skills = [] } = session;

  const [messages, setMessages]       = useState([]);
  const [input, setInput]             = useState('');
  const [sending, setSending]         = useState(false);
  const [aiTyping, setAiTyping]       = useState(false);
  const [currentSkill, setCurrentSkill] = useState(jd_skills[0] || '');
  const [skillIndex, setSkillIndex]   = useState(0);
  const [turnCount, setTurnCount]     = useState(1);
  const [scores, setScores]           = useState({});
  const [toast, setToast]             = useState(null);
  const [scoringSkill, setScoringSkill] = useState(null);
  const [done, setDone]               = useState(false);
  const bottomRef = useRef(null);

  const allSkills = jd_skills;
  const gap_skills = jd_skills.filter(s => !resume_skills.includes(s));

  // First AI greeting
  useEffect(() => {
    const greeting = {
      role: 'assistant',
      content: `👋 Hello! I'm your AI interviewer. I'll assess your proficiency in: **${allSkills.join(', ')}**.\n\nLet's start with **${currentSkill}**. Please introduce your experience with it briefly, then I'll ask targeted questions.`,
      ts: new Date(),
    };
    setMessages([greeting]);
  }, []); // eslint-disable-line

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, aiTyping]);

  const scoreAndAdvance = async (skill) => {
    setScoringSkill(skill);
    try {
      const result = await api.score({ session_id, skill });
      const s = result.skill_score;
      setScores(prev => ({ ...prev, [skill]: s }));
      const nextIdx = skillIndex + 1;
      if (nextIdx < allSkills.length) {
        setSkillIndex(nextIdx);
        setCurrentSkill(allSkills[nextIdx]);
        setTurnCount(1);
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: `✅ Scored **${skill}**: Level ${s.assessed_level}/5 (${(s.confidence * 100).toFixed(0)}% confidence)\n\nNow let's assess **${allSkills[nextIdx]}**. Tell me about your experience!`,
          ts: new Date(),
          isTransition: true,
        }]);
      } else {
        setDone(true);
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: `🎉 Assessment complete! I've scored all ${allSkills.length} skills.\n\nClick **"View Results"** below to see your detailed scores and get your personalized learning plan.`,
          ts: new Date(),
          isTransition: true,
        }]);
      }
    } catch (err) {
      setToast({ message: `Scoring failed: ${err.message}`, type: 'error' });
    } finally { setScoringSkill(null); }
  };

  const handleSend = async () => {
    const text = input.trim();
    if (!text || sending || done) return;
    const userMsg = { role: 'user', content: text, ts: new Date() };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setSending(true);
    setAiTyping(true);

    try {
      const res = await api.chat({
        session_id, skill: currentSkill,
        user_message: text, turn_count: turnCount,
      });
      setAiTyping(false);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: res.assistant_message,
        ts: new Date(),
      }]);
      const newTurn = turnCount + 1;
      setTurnCount(newTurn);
      if (res.assessment_complete || newTurn > 5) {
        await scoreAndAdvance(currentSkill);
      }
    } catch (err) {
      setAiTyping(false);
      setToast({ message: err.message, type: 'error' });
    } finally { setSending(false); }
  };

  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(); }
  };

  const formatMsg = (text) =>
    text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br/>');

  return (
    <div className="animate-fade-in-up max-w-5xl mx-auto">
      {toast && <Toast {...toast} onDismiss={() => setToast(null)} />}
      <StepBar step={2} />

      <div className="grid lg:grid-cols-4 gap-4">
        {/* Sidebar — skill progress */}
        <div className="lg:col-span-1 space-y-3">
          <div className="glass rounded-xl p-4">
            <h3 className="text-xs font-bold text-slate-200 uppercase mb-3">Skills</h3>
            <div className="space-y-2">
              {allSkills.map((skill, i) => {
                const scored = scores[skill];
                const active = skill === currentSkill && !done;
                const isGap = gap_skills.includes(skill);
                return (
                  <div key={i} className={`rounded-lg p-2.5 text-sm transition-all duration-300
                    ${active ? 'bg-purple-500/20 border border-purple-500/40' : 'glass-light'}
                    ${scored ? 'opacity-70' : ''}`}>
                    <div className="flex items-center justify-between gap-1">
                      <span className={`font-semibold truncate text-sm ${active ? 'text-purple-200' : 'text-white'}`}>{skill}</span>
                      {scored
                        ? <span className="text-xs font-bold text-green-400 flex-shrink-0">L{scored.assessed_level}</span>
                        : active
                          ? <span className="w-2 h-2 bg-purple-400 rounded-full animate-pulse flex-shrink-0" />
                          : <span className="text-slate-600 text-xs flex-shrink-0">—</span>}
                    </div>
                    {isGap && <span className="text-xs text-orange-300 font-semibold">⚠ Gap</span>}
                  </div>
                );
              })}
            </div>
          </div>

          {/* Turn counter */}
          {!done && (
            <div className="glass rounded-xl p-4 text-center">
              <div className="text-xs text-slate-200 mb-1 font-semibold">Turn</div>
              <div className="text-2xl font-bold gradient-text">{turnCount}<span className="text-slate-500 text-base">/5</span></div>
              <div className="w-full bg-slate-700 rounded-full h-1.5 mt-2">
                <div className="h-1.5 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 transition-all duration-500"
                  style={{ width: `${Math.min((turnCount / 5) * 100, 100)}%` }} />
              </div>
            </div>
          )}
        </div>

        {/* Chat */}
        <div className="lg:col-span-3 glass rounded-2xl flex flex-col" style={{ height: '70vh' }}>
          {/* Chat header */}
          <div className="flex items-center gap-3 px-5 py-4 border-b border-slate-700/50">
            <div className="w-9 h-9 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-lg">🤖</div>
            <div>
              <p className="font-bold text-sm text-white">{done ? 'Assessment Complete' : `Assessing: ${currentSkill}`}</p>
              <p className="text-xs text-slate-200 font-medium">{done ? '🎉 All skills scored' : `Skill ${skillIndex + 1} of ${allSkills.length}`}</p>
            </div>
            {scoringSkill && (
              <div className="ml-auto flex items-center gap-2 text-xs text-yellow-400 animate-pulse">
                <div className="w-3 h-3 border border-yellow-400 border-t-transparent rounded-full animate-spin" />
                Scoring {scoringSkill}...
              </div>
            )}
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-5 space-y-4">
            {messages.map((msg, i) => (
              <div key={i} className={`flex gap-2 animate-fade-in-up ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm flex-shrink-0
                  ${msg.role === 'user'
                    ? 'bg-gradient-to-br from-blue-500 to-purple-600'
                    : msg.isTransition ? 'bg-gradient-to-br from-green-500 to-emerald-600'
                    : 'bg-gradient-to-br from-purple-500 to-pink-500'}`}>
                  {msg.role === 'user' ? '👤' : msg.isTransition ? '✅' : '🤖'}
                </div>
                <div className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed relative
                  ${msg.role === 'user'
                    ? 'bg-gradient-to-br from-purple-600 to-purple-700 text-white rounded-tr-sm'
                    : 'glass-light text-slate-200 rounded-tl-sm'}`}
                  dangerouslySetInnerHTML={{ __html: formatMsg(msg.content) }} />
              </div>
            ))}
            {aiTyping && <TypingIndicator />}
            <div ref={bottomRef} />
          </div>

          {/* Input */}
          <div className="p-4 border-t border-slate-700/50">
            {done ? (
              <button onClick={() => onNext(scores)}
                className="w-full py-3 rounded-xl font-bold bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-400 hover:to-emerald-500 text-white transition transform hover:scale-[1.01]">
                📊 View My Results →
              </button>
            ) : (
              <div className="flex gap-3">
                <textarea value={input} onChange={e => setInput(e.target.value)} onKeyDown={handleKey}
                  rows={2} placeholder="Type your answer… (Enter to send, Shift+Enter for newline)"
                  disabled={sending || !!scoringSkill}
                  className="flex-1 bg-slate-800 border border-slate-500 rounded-xl px-4 py-2.5 text-white text-sm placeholder-slate-400 resize-none disabled:opacity-50 font-medium" />
                <button onClick={handleSend} disabled={sending || !input.trim() || !!scoringSkill}
                  className="w-12 bg-gradient-to-br from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 disabled:opacity-40 rounded-xl flex items-center justify-center transition">
                  {sending
                    ? <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    : <span className="text-xl">➤</span>}
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
