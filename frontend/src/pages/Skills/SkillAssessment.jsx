import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../../api/client";
import { ErrorMessage, LoadingState, PageHeader, ProgressBar } from "../../components/CommonComponents";

export default function SkillAssessment() {
  const [meta, setMeta] = useState({ categories: [], difficulties: [] });
  const [category, setCategory] = useState("Python");
  const [difficulty, setDifficulty] = useState("Beginner");
  const [session, setSession] = useState(null);
  const [answers, setAnswers] = useState({});
  const [startedAt, setStartedAt] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [remaining, setRemaining] = useState(null);

  useEffect(() => {
    api.assessments.getCategories().then(setMeta).catch((e) => setError(e.message));
  }, []);

  useEffect(() => {
    if (!session || !startedAt) return undefined;
    const timer = setInterval(() => {
      const elapsed = Math.floor((Date.now() - startedAt) / 1000);
      setRemaining(Math.max(0, session.time_limit_seconds - elapsed));
    }, 500);
    return () => clearInterval(timer);
  }, [session, startedAt]);

  async function start() {
    setError("");
    setResult(null);
    setLoading(true);
    try {
      const data = await api.assessments.start(category, difficulty);
      setSession(data);
      setAnswers({});
      setStartedAt(Date.now());
      setRemaining(data.time_limit_seconds);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function submit() {
    const timeTaken = Math.floor((Date.now() - startedAt) / 1000);
    const payload = {
      category: session.category,
      difficulty: session.difficulty,
      time_taken_seconds: timeTaken,
      answers: session.questions.map((q) => ({
        question_id: q.id,
        selected_answer: answers[q.id] || "",
      })),
    };
    setLoading(true);
    try {
      const data = await api.assessments.submit(payload);
      setResult(data);
      setSession(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <PageHeader
        title="Skill assessments"
        subtitle="Scoring happens only on the backend. Timed mode is optional and recorded."
        breadcrumbs="Prepare / Assessments"
        action={<Link className="btn btn-secondary" to="/assessment-history">History</Link>}
      />

      {!session && !result && (
        <div className="card" style={{ padding: 24 }}>
          <div className="grid-2">
            <div className="form-group">
              <label className="form-label">Category</label>
              <select className="form-select" value={category} onChange={(e) => setCategory(e.target.value)}>
                {(meta.categories || []).map((c) => <option key={c}>{c}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Difficulty</label>
              <select className="form-select" value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
                {(meta.difficulties || []).map((c) => <option key={c}>{c}</option>)}
              </select>
            </div>
          </div>
          {error && <ErrorMessage message={error} />}
          <button className="btn btn-primary" onClick={start} disabled={loading}>Start assessment</button>
        </div>
      )}

      {loading && <LoadingState />}

      {session && (
        <div className="card" style={{ padding: 24 }}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 16 }}>
            <strong>{session.category} · {session.difficulty}</strong>
            <span className="badge badge-warning">Time left: {remaining}s</span>
          </div>
          <ProgressBar percentage={(Object.keys(answers).length / session.total_questions) * 100} />
          {session.questions.map((q, idx) => (
            <div key={q.id} style={{ marginTop: 20 }}>
              <p style={{ fontWeight: 600 }}>{idx + 1}. {q.question_text}</p>
              <p style={{ fontSize: 12, color: "var(--neutral-500)" }}>{q.topic_tag} · {q.question_type}</p>
              {q.code_starter && <pre style={{ background: "var(--neutral-100)", padding: 12, borderRadius: 8 }}>{q.code_starter}</pre>}
              {(q.options || []).map((opt) => (
                <label key={opt} style={{ display: "block", fontSize: 14, marginTop: 6 }}>
                  <input type="radio" name={`q-${q.id}`} checked={answers[q.id] === opt} onChange={() => setAnswers({ ...answers, [q.id]: opt })} /> {opt}
                </label>
              ))}
              {(!q.options || q.options.length === 0) && (
                <textarea className="form-textarea" rows={4} value={answers[q.id] || ""} onChange={(e) => setAnswers({ ...answers, [q.id]: e.target.value })} />
              )}
            </div>
          ))}
          <button className="btn btn-primary" style={{ marginTop: 20 }} onClick={submit}>Submit for scoring</button>
        </div>
      )}

      {result && (
        <div className="card" style={{ padding: 24 }}>
          <h3>{result.percentage}% · {result.proficiency_level}</h3>
          <p>Score {result.score}/{result.max_score} in {result.time_taken_seconds}s. Evidence status: {result.verification_status}.</p>
          <p style={{ fontSize: 13 }}><strong>Weak topics:</strong> {(result.weak_topics || []).join(", ") || "None flagged"}</p>
          <ul>{(result.recommendations || []).map((r) => <li key={r} style={{ fontSize: 13 }}>{r}</li>)}</ul>
          {(result.review || []).map((item) => (
            <div key={item.question_id} className="alert" style={{ background: item.is_correct ? "var(--success-50)" : "var(--danger-50)", marginTop: 8 }}>
              <div>
                <strong>{item.question_text}</strong>
                <div>Your answer: {item.selected_answer || "(blank)"}</div>
                <div>Correct: {item.correct_answer}</div>
                <div style={{ fontSize: 13 }}>{item.explanation}</div>
              </div>
            </div>
          ))}
          <button className="btn btn-secondary" onClick={() => setResult(null)}>Take another</button>
        </div>
      )}
    </div>
  );
}
