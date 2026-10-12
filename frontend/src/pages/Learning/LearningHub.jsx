import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../../api/client";
import { EmptyState, ErrorMessage, LoadingState, PageHeader } from "../../components/CommonComponents";

export default function LearningHub() {
  const [lessons, setLessons] = useState([]);
  const [category, setCategory] = useState("");
  const [difficulty, setDifficulty] = useState("");
  const [bookmarked, setBookmarked] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  function load() {
    setLoading(true);
    api.learning
      .list(category, difficulty, bookmarked)
      .then(setLessons)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    load();
  }, [category, difficulty, bookmarked]);

  if (loading) return <LoadingState />;
  if (error) return <ErrorMessage message={error} onRetry={load} />;

  return (
    <div>
      <PageHeader title="Learning hub" subtitle="A lesson counts as complete only after the quiz is passed, not after opening it." breadcrumbs="Learn / Lessons" />
      <div className="grid-3" style={{ marginBottom: 16 }}>
        <select className="form-select" value={category} onChange={(e) => setCategory(e.target.value)}>
          <option value="">All skills</option>
          {["Python", "SQL", "DSA", "DBMS", "OOP", "Web", "Statistics/Data Analysis", "Problem Solving"].map((c) => <option key={c}>{c}</option>)}
        </select>
        <select className="form-select" value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
          <option value="">All difficulties</option>
          <option>Beginner</option>
          <option>Intermediate</option>
          <option>Advanced</option>
        </select>
        <label style={{ fontSize: 14, display: "flex", alignItems: "center", gap: 8 }}>
          <input type="checkbox" checked={bookmarked} onChange={(e) => setBookmarked(e.target.checked)} /> Bookmarks only
        </label>
      </div>
      {lessons.length === 0 ? (
        <EmptyState title="No lessons match" description="Try clearing filters." />
      ) : (
        <div className="grid-2">
          {lessons.map((l) => (
            <Link key={l.id} to={`/learning/${l.id}`} className="card" style={{ padding: 16, color: "inherit" }}>
              <div className="badge badge-neutral">{l.skill_category}</div>
              <h3 style={{ marginTop: 8 }}>{l.title}</h3>
              <p style={{ fontSize: 13 }}>{l.difficulty} · {l.estimated_minutes} min · {l.is_completed ? "Complete" : "Not complete"}</p>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
