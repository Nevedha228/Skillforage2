import { NavLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const GROUPS = [
  {
    label: "Prepare",
    items: [
      { label: "Dashboard", path: "/dashboard" },
      { label: "Career Discovery", path: "/careers" },
      { label: "Assessments", path: "/assessments" },
      { label: "History", path: "/assessment-history" },
      { label: "Skill Evidence", path: "/skills" },
    ],
  },
  {
    label: "Learn",
    items: [
      { label: "Market Intelligence", path: "/market" },
      { label: "Roadmap", path: "/roadmap" },
      { label: "Learning Hub", path: "/learning" },
      { label: "Projects", path: "/projects" },
    ],
  },
  {
    label: "Practice",
    items: [
      { label: "Challenges", path: "/challenges" },
      { label: "Streaks & Rewards", path: "/rewards" },
      { label: "Interview Hub", path: "/interviews" },
      { label: "Resume", path: "/resume" },
    ],
  },
  {
    label: "Tools",
    items: [
      { label: "What-If Simulator", path: "/what-if" },
      { label: "Emergency Sprint", path: "/sprint" },
      { label: "Hackathons", path: "/hackathons" },
      { label: "Profile", path: "/settings" },
    ],
  },
];

export function Sidebar({ mobileOpen, onClose }) {
  const { user, logout } = useAuth();

  return (
    <aside className={`sidebar-container${mobileOpen ? " mobile-open" : ""}`}>
      <div className="sidebar-header">
        <div
          style={{
            width: 36,
            height: 36,
            borderRadius: 8,
            background: "var(--primary-600)",
            color: "#fff",
            display: "grid",
            placeItems: "center",
            fontWeight: 700,
          }}
        >
          SF
        </div>
        <div>
          <div style={{ fontWeight: 700, fontSize: 15 }}>SkillForage AI</div>
          <div style={{ fontSize: 11, color: "var(--neutral-500)" }}>Student workspace</div>
        </div>
      </div>

      <nav className="sidebar-nav">
        {GROUPS.map((group) => (
          <div key={group.label}>
            <div className="nav-section-title">{group.label}</div>
            {group.items.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) => `nav-item${isActive ? " active" : ""}`}
                onClick={onClose}
              >
                {item.label}
              </NavLink>
            ))}
          </div>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 4 }}>{user?.username}</div>
        <div style={{ fontSize: 12, color: "var(--neutral-500)", marginBottom: 12 }}>
          Year {user?.year} · {user?.degree}
        </div>
        <button type="button" className="btn btn-secondary btn-sm" style={{ width: "100%" }} onClick={logout}>
          Sign out
        </button>
      </div>
    </aside>
  );
}

export default Sidebar;
