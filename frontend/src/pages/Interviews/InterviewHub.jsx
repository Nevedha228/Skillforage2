import { useEffect, useState } from "react";
import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { api } from "../../api/client";
import { EmptyState, ErrorMessage, LoadingState, PageHeader } from "../../components/CommonComponents";

export default function InterviewHub() {
  const [form, setForm] = useState({ target_role: "sde", interview_type: "technical", difficulty: "Intermediate" });
  const [session, setSession] = useState(null);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState("");
  const [startedAt, setStartedAt] = useState(null);

  useEffect(() => {
    api.interviews.history().then(setHistory).catch(() => setHistory([]));
  }, [result]);

  async function start() {
    setError("");
    try {
      const data = await api.interviews.start(form);
      setSession(data);
      setResult(null);
      setAnswers({});
      setStartedAt(Date.now());
    } catch (e) {
      setError(e.message);
    }
  }

  async function submit() {
    const payload = {
      target_role: session.target_role,
      interview_type: session.interview_type,
      difficulty: session.difficulty,
      time_taken_seconds: Math.floor((Date.now() - startedAt) / 1000),
      answers: session.questions.map((q) => ({
        question_id: q.id,
        question: q.question,
        answer_text: answers[q.id] || "",
      })),
    };
    const data = await api.interviews.submit(payload);
    setResult(data);
    setSession(null);
  }

  const chart = (history || []).map((h) => ({
    name: new Date(h.created_at).toLocaleDateString(),
    score: h.total_percentage,
  }));

  return (
    <div>
      <PageHeader
        title="Interview hub"
        subtitle="Rubric scoring uses transparent keyword/coverage heuristics. Results do not predict real interview outcomes. No camera or microphone is required."
        breadcrumbs="Practice / Interviews"
      />
      {error && <ErrorMessage message={error} />}
      {!session && (
        <div className="card" style={{ padding: 16, marginBottom: 16 }}>
          <div className="grid-3">
            <input className="form-control" value={form.target_role} onChange={(e) => setForm({ ...form, target_role: e.target.value })} placeholder="Role id e.g. sde" />
            <select className="form-select" value={form.interview_type} onChange={(e) => setForm({ ...form, interview_type: e.target.value })}>
              {["technical", "behavioral", "sql", "programming", "project", "hr"].map((t) => <option key={t}>{t}</option>)}
            </select>
            <select className="form-select" value={form.difficulty} onChange={(e) => setForm({ ...form, difficulty: e.target.value })}>
              <option>Beginner</option>
              <option>Intermediate</option>
              <option>Advanced</option>
            </select>
          </div>
          <button className="btn btn-primary" style={{ marginTop: 12 }} onClick={start}>Start timed session</button>
        </div>
      )}
      {session && (
        <div className="card" style={{ padding: 16 }}>
          <p>{session.disclaimer}</p>
          {session.questions.map((q) => (
            <div key={q.id} style={{ marginTop: 16 }}>
              <strong>{q.question}</strong>
              <textarea className="form-textarea" rows={4} value={answers[q.id] || ""} onChange={(e) => setAnswers({ ...answers, [q.id]: e.target.value })} />
            </div>
          ))}
          <button className="btn btn-primary" style={{ marginTop: 12 }} onClick={submit}>Submit for rubric scoring</button>
        </div>
      )}
      {result && (
        <div className="card" style={{ padding: 16, marginTop: 16 }}>
          <h3>{result.rubric_scores.total_percentage}%</h3>
          <p>LLM status: {result.feedback.llm_status === "ai_evaluated" ? "LLM evaluated" : "LLM not configured — heuristic fallback"}</p>
          <p>{result.disclaimer}</p>
          {Object.entries(result.rubric_scores).map(([k, v]) => k !== "total_percentage" && <div key={k}>{k}: {v}</div>)}
        </div>
      )}
      <div className="card" style={{ padding: 16, height: 240, marginTop: 16 }}>
        <h3 className="card-title">Readiness trend</h3>
        {chart.length === 0 ? <EmptyState title="No sessions yet" description="Complete a mock interview to plot trend." /> : (
          <ResponsiveContainer>
            <LineChart data={chart}>
              <XAxis dataKey="name" />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Line dataKey="score" stroke="#4f46e5" />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
}
