import { useEffect, useState } from "react";
import { api } from "../../api/client";
import { EmptyState, ErrorMessage, LoadingState, PageHeader, ProgressBar } from "../../components/CommonComponents";

export default function Roadmap() {
  const [roadmap, setRoadmap] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [weekly, setWeekly] = useState(10);

  function load() {
    setLoading(true);
    api.roadmaps
      .getCurrent()
      .then(setRoadmap)
      .catch((e) => {
        if (e.status === 404) setRoadmap(null);
        else setError(e.message);
      })
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    load();
  }, []);

  async function generate() {
    setLoading(true);
    try {
      const data = await api.roadmaps.generate({ weekly_hours: weekly });
      setRoadmap(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function complete(taskId) {
    const data = await api.roadmaps.completeTask({ task_id: taskId });
    setRoadmap(data);
  }

  async function reschedule() {
    const data = await api.roadmaps.reschedule({ reason: "Missed tasks — adjust pacing" });
    setRoadmap(data);
  }

  if (loading) return <LoadingState />;

  return (
    <div>
      <PageHeader title="Adaptive roadmap" subtitle="Year-aware phases from your profile, assessments, and market gaps. Versions are persisted." breadcrumbs="Learn / Roadmap" />
      {error && <ErrorMessage message={error} />}
      <div className="card" style={{ padding: 16, marginBottom: 16, display: "flex", gap: 12, alignItems: "end" }}>
        <div className="form-group" style={{ margin: 0 }}>
          <label className="form-label">Weekly hours</label>
          <input className="form-control" type="number" min={2} max={40} value={weekly} onChange={(e) => setWeekly(Number(e.target.value))} />
        </div>
        <button className="btn btn-primary" onClick={generate}>Generate / refresh roadmap</button>
      </div>
      {!roadmap ? (
        <EmptyState title="No roadmap saved" description="Generate a plan after choosing a target role." />
      ) : (
        <>
          <p>{roadmap.year_emphasis} · v{roadmap.version} · {roadmap.progress_percentage}%</p>
          <ProgressBar percentage={roadmap.progress_percentage} />
          {roadmap.rescheduling_suggestion && (
            <div className="alert alert-info">
              {roadmap.rescheduling_suggestion.message}
              <button className="btn btn-secondary btn-sm" style={{ marginLeft: 8 }} onClick={reschedule}>Reschedule without penalty</button>
            </div>
          )}
          {(roadmap.phases || []).map((phase) => (
            <div key={phase.phase_number} className="card" style={{ padding: 16, marginTop: 16 }}>
              <h3>Phase {phase.phase_number}: {phase.title}</h3>
              <p style={{ fontSize: 13, color: "var(--neutral-600)" }}>{phase.focus} · {phase.estimated_weeks} weeks · checkpoint: {phase.milestone}</p>
              {phase.tasks.map((t) => (
                <div key={t.id} style={{ display: "flex", justifyContent: "space-between", padding: "8px 0", borderBottom: "1px solid var(--neutral-100)", fontSize: 14 }}>
                  <span>{t.is_completed ? "Done" : "Open"} · {t.title} ({t.skill}, {t.estimated_hours}h)</span>
                  {!t.is_completed && <button className="btn btn-sm btn-secondary" onClick={() => complete(t.id)}>Mark complete</button>}
                </div>
              ))}
            </div>
          ))}
        </>
      )}
    </div>
  );
}
