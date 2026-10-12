import { useEffect, useState } from "react";
import { api } from "../../api/client";
import { EmptyState, ErrorMessage, LoadingState, PageHeader, SkillBadge } from "../../components/CommonComponents";

export default function SkillVerification() {
  const [items, setItems] = useState([]);
  const [name, setName] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  function load() {
    setLoading(true);
    api.skills
      .verified()
      .then(setItems)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    load();
  }, []);

  async function selfReport(e) {
    e.preventDefault();
    try {
      await api.skills.selfReport({ skill_name: name });
      setName("");
      load();
    } catch (err) {
      setError(err.message);
    }
  }

  if (loading) return <LoadingState />;

  return (
    <div>
      <PageHeader
        title="Skill evidence"
        subtitle="Statuses are Not assessed, Self-reported, In progress, Demonstrated, or Strong evidence. This is not a certification."
        breadcrumbs="Prepare / Skills"
      />
      {error && <ErrorMessage message={error} onRetry={load} />}
      <form onSubmit={selfReport} className="card" style={{ padding: 16, marginBottom: 16, display: "flex", gap: 8 }}>
        <input className="form-control" placeholder="Self-report a skill" value={name} onChange={(e) => setName(e.target.value)} />
        <button className="btn btn-primary" type="submit">Add</button>
      </form>
      {items.length === 0 ? (
        <EmptyState title="No evidence recorded" description="Complete assessments, lessons, and projects, or self-report a skill to start." />
      ) : (
        items.map((s) => (
          <div key={s.id} className="card" style={{ padding: 16, marginBottom: 8 }}>
            <SkillBadge name={s.skill_name} status={s.status} />
            <ul style={{ marginTop: 8, fontSize: 13 }}>
              {(s.evidence_sources || []).map((e, i) => (
                <li key={i}>{e.type}: {e.description}</li>
              ))}
            </ul>
          </div>
        ))
      )}
    </div>
  );
}
