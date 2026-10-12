import { useEffect, useState } from "react";
import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { api } from "../../api/client";
import { EmptyState, ErrorMessage, LoadingState, PageHeader } from "../../components/CommonComponents";

export default function AssessmentHistory() {
  const [data, setData] = useState(null);
  const [detail, setDetail] = useState(null);
  const [category, setCategory] = useState("");
  const [sortBy, setSortBy] = useState("date_desc");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  function load() {
    setLoading(true);
    const params = new URLSearchParams();
    if (category) params.set("category", category);
    params.set("sort_by", sortBy);
    api.assessments
      .history(params.toString())
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    load();
  }, [category, sortBy]);

  if (loading) return <LoadingState />;
  if (error) return <ErrorMessage message={error} onRetry={load} />;

  const chart = (data?.assessments || []).slice().reverse().map((a) => ({
    name: new Date(a.created_at).toLocaleDateString(),
    score: a.percentage,
  }));

  return (
    <div>
      <PageHeader title="Assessment history" subtitle={`${data.total_taken} saved attempts · avg ${data.average_percentage}% · best ${data.best_percentage}%`} breadcrumbs="Prepare / History" />
      <div className="grid-2" style={{ marginBottom: 16 }}>
        <select className="form-select" value={category} onChange={(e) => setCategory(e.target.value)}>
          <option value="">All categories</option>
          {["Python", "SQL", "DSA", "DBMS", "OOP", "Web", "Statistics/Data Analysis", "Problem Solving"].map((c) => <option key={c}>{c}</option>)}
        </select>
        <select className="form-select" value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
          <option value="date_desc">Newest</option>
          <option value="date_asc">Oldest</option>
          <option value="score_desc">Highest score</option>
          <option value="score_asc">Lowest score</option>
        </select>
      </div>
      {(data.assessments || []).length === 0 ? (
        <EmptyState title="No attempts yet" description="Take an assessment to populate history, topic breakdowns, and trend charts." />
      ) : (
        <>
          <div className="card" style={{ padding: 16, height: 260, marginBottom: 16 }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chart}>
                <XAxis dataKey="name" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Line type="monotone" dataKey="score" stroke="#4f46e5" dot />
              </LineChart>
            </ResponsiveContainer>
          </div>
          {data.assessments.map((a) => (
            <button key={a.id} className="card" style={{ width: "100%", textAlign: "left", padding: 16, marginBottom: 8 }} onClick={() => api.assessments.getDetail(a.id).then(setDetail)}>
              <strong>{a.category}</strong> · {a.difficulty} · {a.percentage}% · {new Date(a.created_at).toLocaleString()}
            </button>
          ))}
        </>
      )}
      {detail && (
        <div className="card" style={{ padding: 16, marginTop: 16 }}>
          <h3>Attempt {detail.id}</h3>
          <p>{detail.percentage}% in {detail.time_taken_seconds}s</p>
          <p style={{ fontSize: 13 }}>Weak topics: {(detail.weak_topics || []).join(", ") || "None"}</p>
        </div>
      )}
    </div>
  );
}
