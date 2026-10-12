import { useMemo, useState } from "react";
import { api } from "../../api/client";
import { useAuth } from "../../context/AuthContext";
import { ErrorMessage, LoadingState, PageHeader } from "../../components/CommonComponents";

const INTERESTS = ["Data & Analytics", "Business Strategy", "Visualization", "Statistics", "AI / ML", "Mathematics", "Research", "Software Engineering", "Problem Solving", "Web Development", "Design", "Cloud & Infrastructure", "Security", "Product"];
const ACTIVITIES = ["Building dashboards", "Querying databases", "Writing APIs", "Designing UIs", "Training models", "Automating deployments", "Writing tests", "Solving puzzles"];
const SKILLS = ["Python", "SQL", "Excel", "Java", "JavaScript", "React", "DSA", "OOP", "Git", "Linux", "Statistics", "HTML", "CSS"];

function Chip({ label, selected, onClick }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`badge ${selected ? "badge-primary" : "badge-neutral"}`}
      style={{ border: "none", cursor: "pointer", margin: 4, padding: "6px 10px" }}
    >
      {label}
    </button>
  );
}

export default function CareerDiscovery() {
  const { refreshUser } = useAuth();
  const [form, setForm] = useState({
    interests: [],
    activities: [],
    known_skills: [],
    favorite_subjects: ["Mathematics"],
    problem_solving_style: "analytical",
    career_goals: "high_growth",
    work_style: "flexible",
    confidence_level: 3,
    learning_style: "practical",
  });
  const [result, setResult] = useState(null);
  const [compare, setCompare] = useState([]);
  const [compareData, setCompareData] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState("");

  function toggle(field, value) {
    setForm((prev) => {
      const set = new Set(prev[field]);
      if (set.has(value)) set.delete(value);
      else set.add(value);
      return { ...prev, [field]: [...set] };
    });
  }

  async function runMatch(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const data = await api.careers.match(form);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function saveTarget(roleId) {
    setSaving(roleId);
    try {
      await api.careers.setTarget({ role_id: roleId });
      await refreshUser();
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving("");
    }
  }

  async function runCompare() {
    if (compare.length < 2) return;
    const data = await api.careers.compare({ role_ids: compare });
    setCompareData(data);
  }

  const top = useMemo(() => result?.recommended_roles?.slice(0, 6) || [], [result]);

  return (
    <div>
      <PageHeader
        title="Career Discovery"
        subtitle="Transparent weighted matching. Scores are heuristic planning guides, not a validated psychological assessment."
        breadcrumbs="Prepare / Careers"
      />
      <form onSubmit={runMatch} className="card" style={{ padding: 24, marginBottom: 24 }}>
        <p className="form-label">Interests</p>
        {INTERESTS.map((i) => <Chip key={i} label={i} selected={form.interests.includes(i)} onClick={() => toggle("interests", i)} />)}
        <p className="form-label" style={{ marginTop: 16 }}>Activities you enjoy</p>
        {ACTIVITIES.map((i) => <Chip key={i} label={i} selected={form.activities.includes(i)} onClick={() => toggle("activities", i)} />)}
        <p className="form-label" style={{ marginTop: 16 }}>Skills you already have</p>
        {SKILLS.map((i) => <Chip key={i} label={i} selected={form.known_skills.includes(i)} onClick={() => toggle("known_skills", i)} />)}
        <div className="grid-2" style={{ marginTop: 16 }}>
          <div className="form-group">
            <label className="form-label">Problem-solving style</label>
            <select className="form-select" value={form.problem_solving_style} onChange={(e) => setForm({ ...form, problem_solving_style: e.target.value })}>
              <option value="analytical">Analytical</option>
              <option value="creative">Creative</option>
              <option value="systematic">Systematic</option>
              <option value="collaborative">Collaborative</option>
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">Goal</label>
            <select className="form-select" value={form.career_goals} onChange={(e) => setForm({ ...form, career_goals: e.target.value })}>
              <option value="high_growth">High growth</option>
              <option value="research">Research</option>
              <option value="entrepreneurship">Entrepreneurship</option>
              <option value="stable">Stable</option>
            </select>
          </div>
        </div>
        {error && <ErrorMessage message={error} />}
        <button className="btn btn-primary" type="submit" disabled={loading}>{loading ? "Matching..." : "Calculate matches"}</button>
      </form>

      {loading && <LoadingState message="Scoring 13 roles..." />}

      {result && (
        <>
          <div className="alert alert-info">{result.disclaimer}</div>
          <div className="grid-2">
            {top.map((role) => (
              <div key={role.id} className="card" style={{ padding: 20 }}>
                <div style={{ display: "flex", justifyContent: "space-between" }}>
                  <h3>{role.title}</h3>
                  <span className="badge badge-primary">{role.match_score}%</span>
                </div>
                <p style={{ fontSize: 13, color: "var(--neutral-600)" }}>{role.explanation.summary}</p>
                <p style={{ fontSize: 12 }}><strong>Matching interests:</strong> {role.explanation.matching_interests.join(", ") || "None"}</p>
                <p style={{ fontSize: 12 }}><strong>Strengths:</strong> {role.explanation.strengths.join(", ") || "None yet"}</p>
                <p style={{ fontSize: 12 }}><strong>Missing skills:</strong> {role.explanation.missing_skills.slice(0, 6).join(", ")}</p>
                <p style={{ fontSize: 12 }}><strong>Learn next:</strong> {role.learning_priorities.slice(0, 2).join(" · ")}</p>
                <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
                  <button className="btn btn-primary btn-sm" onClick={() => saveTarget(role.id)} disabled={saving === role.id}>
                    {saving === role.id ? "Saving..." : "Set as target"}
                  </button>
                  <button className="btn btn-secondary btn-sm" onClick={() => setCompare((c) => c.includes(role.id) ? c.filter((x) => x !== role.id) : [...c, role.id])}>
                    {compare.includes(role.id) ? "Selected" : "Compare"}
                  </button>
                </div>
              </div>
            ))}
          </div>
          {compare.length >= 2 && (
            <div style={{ marginTop: 16 }}>
              <button className="btn btn-outline" onClick={runCompare}>Compare selected roles</button>
            </div>
          )}
          {compareData && (
            <div className="grid-2" style={{ marginTop: 16 }}>
              {compareData.compared_roles.map((r) => (
                <div key={r.id} className="card" style={{ padding: 16 }}>
                  <h4>{r.title}</h4>
                  <p style={{ fontSize: 13 }}>{r.description}</p>
                  <p style={{ fontSize: 12 }}><strong>Skills:</strong> {Object.keys(r.required_skills || {}).join(", ")}</p>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}
