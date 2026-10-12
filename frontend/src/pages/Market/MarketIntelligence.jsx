import { useEffect, useState } from "react";
import { Bar, BarChart, CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { api } from "../../api/client";
import { ErrorMessage, LoadingState, PageHeader } from "../../components/CommonComponents";

export default function MarketIntelligence() {
  const [origin, setOrigin] = useState("synthetic_demo");
  const [analytics, setAnalytics] = useState(null);
  const [gap, setGap] = useState(null);
  const [status, setStatus] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  function load() {
    setLoading(true);
    Promise.all([
      api.market.analytics(origin),
      api.market.skillGap(),
      api.market.status(),
    ])
      .then(([a, g, s]) => {
        setAnalytics(a);
        setGap(g);
        setStatus(s);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    load();
  }, [origin]);

  async function importFile(e) {
    const file = e.target.files?.[0];
    if (!file) return;
    const fd = new FormData();
    fd.append("file", file);
    try {
      await api.market.importFile(fd);
      setOrigin("imported");
    } catch (err) {
      setError(err.message);
    }
  }

  if (loading) return <LoadingState message="Loading labeled market analytics..." />;

  const topSkills = analytics?.top_skills || analytics?.skills || [];
  const skillRows = Array.isArray(topSkills)
    ? topSkills.slice(0, 12).map((s) => (typeof s === "string" ? { skill: s, count: 1 } : { skill: s.skill || s.name, count: s.count || s.frequency || 0 }))
    : Object.entries(topSkills).map(([skill, count]) => ({ skill, count }));

  return (
    <div>
      <PageHeader
        title="Market intelligence"
        subtitle="Charts are labeled by data origin. Synthetic demo postings are never mixed into collected statistics."
        breadcrumbs="Learn / Market"
      />
      {error && <ErrorMessage message={error} onRetry={load} />}
      <div className="alert alert-warning">
        Origin: <strong>{analytics?.data_origin || origin}</strong>
        {analytics?.low_sample_warning && <div>{analytics.low_sample_warning}</div>}
        {status && <div>Adapter status: Adzuna {status.adzuna_configured ? "configured" : "disabled (no keys)"}; LLM {status.llm_configured ? "configured" : "not configured"}.</div>}
      </div>
      <div style={{ display: "flex", gap: 8, marginBottom: 16, flexWrap: "wrap" }}>
        {["synthetic_demo", "imported", "collected"].map((o) => (
          <button key={o} className={`btn ${origin === o ? "btn-primary" : "btn-secondary"}`} onClick={() => setOrigin(o)}>{o}</button>
        ))}
        <label className="btn btn-outline">
          Import CSV/JSON
          <input type="file" accept=".json,.csv" hidden onChange={importFile} />
        </label>
      </div>
      <div className="grid-3" style={{ marginBottom: 16 }}>
        <div className="card" style={{ padding: 16 }}><div className="form-label">Postings</div><strong>{analytics?.posting_count || analytics?.total_postings || 0}</strong></div>
        <div className="card" style={{ padding: 16 }}><div className="form-label">Date range</div><strong>{analytics?.date_range || "n/a"}</strong></div>
        <div className="card" style={{ padding: 16 }}><div className="form-label">Freshness</div><strong>{analytics?.freshness || analytics?.last_updated || "seed"}</strong></div>
      </div>
      <div className="card" style={{ padding: 16, height: 300, marginBottom: 16 }}>
        <h3 className="card-title">Top skills ({origin})</h3>
        <ResponsiveContainer width="100%" height="90%">
          <BarChart data={skillRows}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="skill" hide />
            <YAxis />
            <Tooltip />
            <Bar dataKey="count" fill="#4f46e5" />
          </BarChart>
        </ResponsiveContainer>
      </div>
      {analytics?.trend_over_time && (
        <div className="card" style={{ padding: 16, height: 240, marginBottom: 16 }}>
          <h3 className="card-title">Posting trend ({origin})</h3>
          <ResponsiveContainer width="100%" height="90%">
            <LineChart data={analytics.trend_over_time}>
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line dataKey="count" stroke="#4338ca" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
      {gap && (
        <div className="card" style={{ padding: 16 }}>
          <h3 className="card-title">Personalized skill gap vs {gap.target_role || gap.role_title}</h3>
          <p style={{ fontSize: 13, color: "var(--neutral-600)" }}>{gap.disclaimer || "Comparison uses evidenced skills and role requirements."}</p>
          {(gap.prioritized_gaps || gap.gaps || []).slice(0, 12).map((g, i) => (
            <div key={i} style={{ fontSize: 14, marginTop: 6 }}>
              {g.skill || g.name} · {g.priority || g.severity || "gap"}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
