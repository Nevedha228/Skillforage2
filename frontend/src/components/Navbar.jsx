import { useAuth } from "../context/AuthContext";
import { Link } from "react-router-dom";

export function Navbar({ onToggleMobile }) {
  const { user } = useAuth();

  return (
    <header className="top-navbar">
      <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
        <button
          onClick={onToggleMobile}
          className="btn btn-secondary btn-sm"
          style={{ display: "none" }}
          id="mobile-nav-toggle"
          aria-label="Toggle navigation"
        >
          ☰
        </button>
        <span style={{ fontSize: "14px", color: "var(--neutral-500)", fontWeight: "500" }}>
          Campus Preparation Portal
        </span>
      </div>

      <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
        {user?.target_role && (
          <span className="badge badge-primary" style={{ padding: "4px 10px", fontSize: "12px" }}>
            Target: {user.target_role.toUpperCase()}
          </span>
        )}
        <span className="badge badge-neutral" style={{ padding: "4px 10px", fontSize: "12px" }}>
          Year {user?.year || 1} • {user?.degree || "B.Tech"}
        </span>
        <Link
          to="/settings"
          style={{
            width: "36px",
            height: "36px",
            borderRadius: "50%",
            background: "var(--primary-100)",
            color: "var(--primary-700)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontWeight: "700",
            fontSize: "14px"
          }}
          title="Account Settings"
        >
          {user?.username ? user.username.charAt(0).toUpperCase() : "U"}
        </Link>
      </div>
      <style>{`
        @media (max-width: 900px) {
          #mobile-nav-toggle { display: inline-flex !important; }
        }
      `}</style>
    </header>
  );
}
