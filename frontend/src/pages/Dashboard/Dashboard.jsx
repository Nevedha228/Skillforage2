import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../../api/client";
import { EmptyState, ErrorMessage, LoadingState, PageHeader, ProgressBar, StatCard } from "../../components/CommonComponents";

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  function load() {
    setLoading(true);
    api.dashboard
      .getStats()
      .then(setStats)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    load();
  }, []);

  if (loading) return <LoadingState message="Loading persisted dashboard metrics..." />;
  if (error) return <ErrorMessage message={error} onRetry={load} />;
  if (!stats) return null;

  return (
    <div>
      <PageHeader
        title={`Welcome, ${stats.username}`}
        subtitle={`Year ${stats.year} · ${stats.degree} · ${stats.branch}${stats.target_role_title ? ` · Target: ${stats.target_role_title}` : ""}`}
        breadcrumbs="Workspace / Dashboard"
      />

      {stats.is_empty_state && (
        <EmptyState
          icon="◎"
          title="No evidence yet"
          description="Numbers here come only from saved assessments, roadmaps, projects, and interviews. Start with a career match or a baseline assessment."
          actionText="Discover careers"
          onAction={() => { window.location.href = "/careers"; }}
        />
      )}

      <div className="grid-4" style={{ marginBottom: 24 }}>
        <StatCard title="Assessments" value={stats.total_assessments_taken} subtext={`Avg ${stats.average_assessment_score}%`} />
        <StatCard title="Evidenced skills" value={stats.total_verified_skills} subtext="Demonstrated or strong evidence" />
        <StatCard title="Roadmap" value={`${stats.roadmap_progress_percentage}%`} subtext="Completed tasks" />
        <StatCard title="Streak / XP" value={`${stats.current_streak_days}d`} subtext={`${stats.total_xp} XP`} />
      </div>

      <div className="grid-2">
        <div className="card">
          <div className="card-header"><h3 className="card-title">Suggested next step</h3></div>
          <div className="card-body">
            <h4 style={{ marginBottom: 8 }}>{stats.suggested_next_action?.title}</h4>
            <p style={{ color: "var(--neutral-600)", fontSize: 14, marginBottom: 16 }}>{stats.suggested_next_action?.description}</p>
            <Link className="btn btn-primary" to={stats.suggested_next_action?.url || "/careers"}>
              {stats.suggested_next_action?.button_text || "Continue"}
            </Link>
          </div>
        </div>
        <div className="card">
          <div className="card-header"><h3 className="card-title">Onboarding checklist</h3></div>
          <div className="card-body">
            {(stats.onboarding_checklist || []).map((item) => (
              <div key={item.id} style={{ display: "flex", justifyContent: "space-between", marginBottom: 10, fontSize: 14 }}>
                <span>{item.is_complete ? "Done" : "Open"} · {item.title}</span>
                <Link to={item.action_url}>Go</Link>
              </div>
            ))}
            <ProgressBar percentage={(stats.onboarding_checklist || []).filter((i) => i.is_complete).length * 20} />
          </div>
        </div>
      </div>

      <div className="card" style={{ marginTop: 24 }}>
        <div className="card-header"><h3 className="card-title">Recent activity from saved records</h3></div>
        <div className="card-body">
          {(stats.recent_activities || []).length === 0 ? (
            <p style={{ color: "var(--neutral-500)", fontSize: 14 }}>No activity logged yet.</p>
          ) : (
            stats.recent_activities.map((a, idx) => (
              <div key={idx} style={{ padding: "10px 0", borderBottom: "1px solid var(--neutral-100)", fontSize: 14 }}>
                <strong>{a.title}</strong>
                <div style={{ color: "var(--neutral-500)" }}>{a.detail} · {a.date}</div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
