import { useEffect, useState } from "react";
import { api } from "../../api/client";
import { EmptyState, ErrorMessage, LoadingState, PageHeader } from "../../components/CommonComponents";

export default function Challenges() {
  const [items, setItems] = useState([]);
  const [type, setType] = useState("");
  const [drafts, setDrafts] = useState({});
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  function load() {
    setLoading(true);
    api.challenges
      .list(type)
      .then(setItems)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    load();
  }, [type]);

  async function submit(id) {
    const data = await api.challenges.submit(id, { submission_text: drafts[id] || "" });
    setMessage(data.message + ` XP awarded: ${data.xp_awarded}`);
    load();
  }

  if (loading) return <LoadingState />;

  return (
    <div>
      <PageHeader title="Challenges" subtitle="Backend evaluation. XP is awarded once per challenge (idempotent)." breadcrumbs="Practice / Challenges" />
      {error && <ErrorMessage message={error} />}
      {message && <div className="alert alert-success">{message}</div>}
      <select className="form-select" style={{ maxWidth: 240, marginBottom: 16 }} value={type} onChange={(e) => setType(e.target.value)}>
        <option value="">All types</option>
        <option value="daily">Daily</option>
        <option value="weekly">Weekly</option>
      </select>
      {items.length === 0 ? <EmptyState title="No challenges" description="Seed data may still be loading." /> : items.map((c) => (
        <div key={c.id} className="card" style={{ padding: 16, marginBottom: 12 }}>
          <div style={{ display: "flex", justifyContent: "space-between" }}>
            <h3>{c.title}</h3>
            <span className="badge badge-primary">{c.xp_reward} XP</span>
          </div>
          <p style={{ fontSize: 13 }}>{c.description}</p>
          <p style={{ fontSize: 12 }}>Hints: {(c.hints || []).join(" · ")}</p>
          {c.is_completed ? <div className="badge badge-success">Completed</div> : (
            <>
              <textarea className="form-textarea" rows={3} value={drafts[c.id] || ""} onChange={(e) => setDrafts({ ...drafts, [c.id]: e.target.value })} />
              <button className="btn btn-primary btn-sm" style={{ marginTop: 8 }} onClick={() => submit(c.id)}>Submit</button>
            </>
          )}
        </div>
      ))}
    </div>
  );
}
