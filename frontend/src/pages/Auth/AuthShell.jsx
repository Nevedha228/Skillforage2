import { Link } from "react-router-dom";

export default function AuthShell({ title, subtitle, children }) {
  return (
    <div style={{ minHeight: "100vh", background: "var(--neutral-50)", display: "grid", placeItems: "center", padding: 24 }}>
      <div className="card" style={{ width: "100%", maxWidth: 480, padding: 32 }}>
        <Link to="/" style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 24, color: "var(--neutral-900)" }}>
          <span style={{ width: 32, height: 32, borderRadius: 8, background: "var(--primary-600)", color: "#fff", display: "grid", placeItems: "center", fontWeight: 700 }}>SF</span>
          <strong>SkillForage AI</strong>
        </Link>
        <h1 style={{ fontSize: 24, marginBottom: 8 }}>{title}</h1>
        <p style={{ color: "var(--neutral-500)", fontSize: 14, marginBottom: 24 }}>{subtitle}</p>
        {children}
      </div>
    </div>
  );
}
