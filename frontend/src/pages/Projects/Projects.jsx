import { useEffect, useState } from "react";
import { api } from "../../api/client";
import { EmptyState, ErrorMessage, LoadingState, PageHeader } from "../../components/CommonComponents";

export default function Projects() {
  const [templates, setTemplates] = useState([]);
  const [mine, setMine] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  function load() {
    setLoading(true);
    Promise.all([api.projects.templates(), api.projects.myProjects()])
      .then(([t, m]) => {
        setTemplates(t);
        setMine(m);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    load();
  }, []);

  async function add(template) {
    await api.projects.create({ template_id: template.id, title: template.title });
    load();
  }

  async function update(project, status) {
    await api.projects.update(project.id, { status });
    load();
  }

  if (loading) return <LoadingState />;

  return (
    <div>
      <PageHeader title="Projects planner" subtitle="GitHub URLs are format-checked only. Repositories are not analyzed." breadcrumbs="Learn / Projects" />
      {error && <ErrorMessage message={error} onRetry={load} />}
      <h3 style={{ marginBottom: 12 }}>Your projects</h3>
      {mine.length === 0 ? <EmptyState title="None planned" description="Add a template below." /> : mine.map((p) => (
        <div key={p.id} className="card" style={{ padding: 16, marginBottom: 8 }}>
          <strong>{p.title}</strong> · {p.status}
          <div style={{ display: "flex", gap: 8, marginTop: 8 }}>
            {["planned", "in progress", "completed", "submitted"].map((s) => (
              <button key={s} className="btn btn-sm btn-secondary" onClick={() => update(p, s)}>{s}</button>
            ))}
          </div>
        </div>
      ))}
      <h3 style={{ margin: "24px 0 12px" }}>Generator templates</h3>
      <div className="grid-2">
        {templates.map((t) => (
          <div key={t.id} className="card" style={{ padding: 16 }}>
            <h4>{t.title}</h4>
            <p style={{ fontSize: 13 }}>{t.problem_statement}</p>
            <p style={{ fontSize: 12 }}>Skills: {(t.skills || []).join(", ")} · {t.duration_hours}h · {t.difficulty}</p>
            <p style={{ fontSize: 12 }}><strong>Relevance:</strong> {t.relevance}</p>
            <button className="btn btn-primary btn-sm" onClick={() => add(t)}>Add as planned</button>
          </div>
        ))}
      </div>
    </div>
  );
}
