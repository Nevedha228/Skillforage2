import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { api } from "../../api/client";

export function Landing() {
  const [hackathonPopup, setHackathonPopup] = useState(null);
  const [showPopup, setShowPopup] = useState(false);

  useEffect(() => {
    // Check if user has already dismissed popup in this browser session
    const isDismissed = sessionStorage.getItem("sf_hackathon_popup_dismissed");
    if (!isDismissed) {
      api.hackathons.getPopup().then((res) => {
        if (res && res.show_popup && res.event) {
          setHackathonPopup(res);
          setShowPopup(true);
        }
      }).catch(() => {});
    }
  }, []);

  const handleDismissPopup = () => {
    sessionStorage.setItem("sf_hackathon_popup_dismissed", "true");
    setShowPopup(false);
  };

  return (
    <div style={{ backgroundColor: "var(--neutral-0)", minHeight: "100vh" }}>
      {/* Top Header */}
      <header style={{ borderBottom: "1px solid var(--neutral-200)", padding: "16px 32px", display: "flex", justifyContent: "space-between", alignItems: "center", maxWidth: "1280px", margin: "0 auto" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <div style={{ width: "36px", height: "36px", borderRadius: "8px", background: "var(--primary-600)", color: "#fff", display: "flex", alignItems: "center", justifyContent: "center", fontWeight: "700", fontSize: "18px" }}>
            SF
          </div>
          <div>
            <div style={{ fontWeight: "700", fontSize: "18px", color: "var(--neutral-900)" }}>SkillForage AI</div>
            <div style={{ fontSize: "11px", color: "var(--neutral-500)" }}>From Zero to Interview-Ready</div>
          </div>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
          <Link to="/login" className="btn btn-secondary">
            Sign In
          </Link>
          <Link to="/register" className="btn btn-primary">
            Create Student Account
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <section style={{ padding: "80px 24px 60px", textAlign: "center", maxWidth: "960px", margin: "0 auto" }}>
        <span className="badge badge-primary" style={{ padding: "6px 14px", fontSize: "13px", marginBottom: "20px" }}>
          🎯 Built for College Students (Years 1-4)
        </span>
        <h1 style={{ fontSize: "48px", fontWeight: "800", color: "var(--neutral-900)", lineHeight: "1.15", marginBottom: "20px" }}>
          Stop Guessing Your Career.<br />
          <span style={{ color: "var(--primary-600)" }}>From Zero to Interview-Ready.</span>
        </h1>
        <p style={{ fontSize: "18px", color: "var(--neutral-600)", maxWidth: "720px", margin: "0 auto 36px", lineHeight: "1.6" }}>
          An evidence-based preparation loop — not a resume scanner or chatbot. 
          Discover career fit, test technical skills, identify employer market demand gaps, and follow a year-aware adaptive roadmap.
        </p>

        <div style={{ display: "flex", justifyContent: "center", gap: "16px", flexWrap: "wrap", marginBottom: "48px" }}>
          <Link to="/register" className="btn btn-primary btn-lg">
            Start Your Journey Free →
          </Link>
          <Link to="/login" className="btn btn-secondary btn-lg">
            Student Login
          </Link>
        </div>

        <div style={{ padding: "16px", background: "var(--neutral-50)", borderRadius: "var(--radius-lg)", border: "1px solid var(--neutral-200)", display: "inline-flex", gap: "32px", flexWrap: "wrap", justifyContent: "center" }}>
          <div><strong>13</strong> In-Demand Tech Roles</div>
          <div><strong>8</strong> Technical Assessment Categories</div>
          <div><strong>160+</strong> Skills Taxonomy</div>
          <div><strong>Zero</strong> Fluff or Guaranteed Hype</div>
        </div>
      </section>

      {/* The Evidence-Based Loop */}
      <section style={{ backgroundColor: "var(--neutral-50)", padding: "72px 24px", borderTop: "1px solid var(--neutral-200)", borderBottom: "1px solid var(--neutral-200)" }}>
        <div style={{ maxWidth: "1140px", margin: "0 auto" }}>
          <div style={{ textAlign: "center", marginBottom: "48px" }}>
            <h2 style={{ fontSize: "30px", fontWeight: "700", color: "var(--neutral-900)", marginBottom: "12px" }}>
              The 7-Step Evidence-Based Loop
            </h2>
            <p style={{ color: "var(--neutral-600)", fontSize: "16px" }}>
              Continuous feedback replaces guesswork with verifiable milestones.
            </p>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))", gap: "16px", textAlign: "center" }}>
            {[
              { step: "1", title: "Student Profile", desc: "Year, degree, branch, hours", icon: "👤" },
              { step: "2", title: "Career Match", desc: "Transparent weighted matching", icon: "🧭" },
              { step: "3", title: "Skill Benchmark", desc: "Backend-scored assessments", icon: "🧠" },
              { step: "4", title: "Market Gap", desc: "Empirical demand comparison", icon: "📊" },
              { step: "5", title: "Adaptive Roadmap", desc: "Pacing with no penalty", icon: "🗺️" },
              { step: "6", title: "Practice & Projects", desc: "Verifiable milestones", icon: "🛠️" },
              { step: "7", title: "Interview Ready", desc: "Rubric-based evaluation", icon: "🎯" }
            ].map((s, idx) => (
              <div key={idx} className="card" style={{ padding: "20px 12px" }}>
                <div style={{ fontSize: "28px", marginBottom: "8px" }}>{s.icon}</div>
                <div style={{ fontSize: "11px", fontWeight: "700", color: "var(--primary-600)", textTransform: "uppercase" }}>Step {s.step}</div>
                <div style={{ fontSize: "14px", fontWeight: "600", color: "var(--neutral-900)", margin: "4px 0" }}>{s.title}</div>
                <div style={{ fontSize: "11px", color: "var(--neutral-500)" }}>{s.desc}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Year-Based Preparation */}
      <section style={{ padding: "72px 24px", maxWidth: "1140px", margin: "0 auto" }}>
        <div style={{ textAlign: "center", marginBottom: "48px" }}>
          <h2 style={{ fontSize: "30px", fontWeight: "700", color: "var(--neutral-900)", marginBottom: "12px" }}>
            Year-Aware Engineering Preparation
          </h2>
          <p style={{ color: "var(--neutral-600)", fontSize: "16px" }}>
            Tailored roadmaps that adapt whether you are starting early in 1st year or sprinting before final-year placement drives.
          </p>
        </div>

        <div className="grid-4">
          {[
            { year: "Year 1: Foundations", tag: "Exploration", desc: "Master introductory programming, algorithmic logic, and web basics. Discover which career domains excite you before specializing." },
            { year: "Year 2: Core CS", tag: "Data & Systems", desc: "Deep dive into Data Structures, Algorithms, Relational DBMS (SQL), and Object-Oriented Design. Build your first database-backed applications." },
            { year: "Year 3: Specialization", tag: "Portfolio & Internships", desc: "Develop full-stack capstone projects, cloud architectures, and machine learning pipelines. Prepare production repos for internship applications." },
            { year: "Year 4: Placement Sprint", tag: "Interview Readiness", desc: "Intensive drills on high-frequency interview patterns, rubric mock interviews, ATS resume alignment, and system design tradeoffs." }
          ].map((y, idx) => (
            <div key={idx} className="card" style={{ padding: "24px" }}>
              <span className="badge badge-primary" style={{ marginBottom: "12px" }}>{y.tag}</span>
              <h3 style={{ fontSize: "16px", fontWeight: "700", color: "var(--neutral-900)", marginBottom: "8px" }}>{y.year}</h3>
              <p style={{ fontSize: "13px", color: "var(--neutral-600)", lineHeight: "1.6" }}>{y.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Market Intelligence Preview */}
      <section style={{ backgroundColor: "var(--neutral-50)", padding: "72px 24px", borderTop: "1px solid var(--neutral-200)" }}>
        <div style={{ maxWidth: "1140px", margin: "0 auto" }}>
          <div style={{ textAlign: "center", marginBottom: "48px" }}>
            <span className="badge badge-neutral" style={{ marginBottom: "12px" }}>Data Transparency</span>
            <h2 style={{ fontSize: "30px", fontWeight: "700", color: "var(--neutral-900)", marginBottom: "12px" }}>
              Honest Labor Market Intelligence
            </h2>
            <p style={{ color: "var(--neutral-600)", fontSize: "16px", maxWidth: "680px", margin: "0 auto" }}>
              Every skill frequency and salary metric is strictly labeled with its data origin (Collected API, Imported Dataset, or Synthetic Demo). No exaggerated promises or hidden black boxes.
            </p>
          </div>

          <div className="grid-3">
            <div className="card" style={{ padding: "24px" }}>
              <div style={{ fontSize: "24px", marginBottom: "8px" }}>🔍</div>
              <h4 style={{ fontSize: "16px", fontWeight: "600", marginBottom: "8px" }}>Word-Boundary Skill Extraction</h4>
              <p style={{ fontSize: "13px", color: "var(--neutral-600)", lineHeight: "1.5" }}>
                Benchmarked on 52 hand-labeled job postings achieving 91.4% precision. Distinguishes standalone languages from substrings like Java and JavaScript.
              </p>
            </div>
            <div className="card" style={{ padding: "24px" }}>
              <div style={{ fontSize: "24px", marginBottom: "8px" }}>⚖️</div>
              <h4 style={{ fontSize: "16px", fontWeight: "600", marginBottom: "8px" }}>Prioritized Skill Gaps</h4>
              <p style={{ fontSize: "13px", color: "var(--neutral-600)", lineHeight: "1.5" }}>
                Identifies Critical, High, and Medium skill gaps comparing your demonstrated assessment scores against current employer posting demand.
              </p>
            </div>
            <div className="card" style={{ padding: "24px" }}>
              <div style={{ fontSize: "24px", marginBottom: "8px" }}>🏷️</div>
              <h4 style={{ fontSize: "16px", fontWeight: "600", marginBottom: "8px" }}>Explicit Data Origin Flags</h4>
              <p style={{ fontSize: "13px", color: "var(--neutral-600)", lineHeight: "1.5" }}>
                Synthetic demo data is never blended into real statistics without clear notice. Low-sample warnings alert you when datasets have fewer than 25 postings.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Frequently Asked Questions */}
      <section style={{ padding: "72px 24px", maxWidth: "800px", margin: "0 auto" }}>
        <h2 style={{ fontSize: "28px", fontWeight: "700", textAlign: "center", color: "var(--neutral-900)", marginBottom: "40px" }}>
          Frequently Asked Questions
        </h2>

        <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
          {[
            {
              q: "How does SkillForage AI calculate career matches?",
              a: "Career matches use a transparent weighted algorithm comparing your interests (35%), demonstrated skills (45%), and work style (20%) against 13 industry role profiles. Scores are educational heuristic guides, not psychometric or medical evaluations."
            },
            {
              q: "Do you guarantee placement offers or starting salaries?",
              a: "No. SkillForage AI provides structured, evidence-based preparation tools, but never guarantees job offers, interview invites, or salaries. Success depends on individual dedication, market conditions, and practice."
            },
            {
              q: "What happens if I miss tasks on my roadmap?",
              a: "You are never penalized. Our non-judgmental rescheduling algorithm calculates your remaining hours and smoothly rebalances incomplete tasks across your available weekly schedule."
            },
            {
              q: "How is resume ATS compatibility evaluated?",
              a: "We extract text directly from your uploaded PDF using standard parsing, check section presence, calculate technical keyword density against industry taxonomy, and compare against job descriptions. We never fabricate experience."
            }
          ].map((item, idx) => (
            <div key={idx} className="card" style={{ padding: "20px" }}>
              <h4 style={{ fontSize: "15px", fontWeight: "600", color: "var(--neutral-900)", marginBottom: "6px" }}>
                {item.q}
              </h4>
              <p style={{ fontSize: "13px", color: "var(--neutral-600)", lineHeight: "1.6" }}>
                {item.a}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer style={{ borderTop: "1px solid var(--neutral-200)", padding: "40px 24px", textAlign: "center", color: "var(--neutral-500)", fontSize: "13px", backgroundColor: "var(--neutral-50)" }}>
        <p style={{ marginBottom: "8px", fontWeight: "600", color: "var(--neutral-700)" }}>SkillForage AI — From Zero to Interview-Ready</p>
        <p style={{ maxWidth: "600px", margin: "0 auto 16px" }}>
          Designed for undergraduate and postgraduate engineering and computing students. Evidence-based preparation, transparent market algorithms, and verifiable milestones.
        </p>
        <p>© 2026 SkillForage AI. All rights reserved.</p>
      </footer>

      {/* Dismissible Hackathon Popup Modal (Shown once per session) */}
      {showPopup && hackathonPopup && hackathonPopup.event && (
        <div className="modal-backdrop">
          <div className="modal-dialog" style={{ padding: "28px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "16px" }}>
              <div>
                <span className="badge badge-warning" style={{ marginBottom: "6px" }}>
                  Demonstration Event Entry
                </span>
                <h3 style={{ fontSize: "18px", fontWeight: "700", color: "var(--neutral-900)" }}>
                  Featured Student Hackathon
                </h3>
              </div>
              <button onClick={handleDismissPopup} style={{ background: "none", border: "none", fontSize: "20px", cursor: "pointer", color: "var(--neutral-500)" }}>
                ✕
              </button>
            </div>

            <div style={{ marginBottom: "16px" }}>
              <div style={{ fontSize: "16px", fontWeight: "600", color: "var(--primary-700)", marginBottom: "4px" }}>
                {hackathonPopup.event.name}
              </div>
              <div style={{ fontSize: "13px", color: "var(--neutral-600)", marginBottom: "8px" }}>
                Organized by: <strong>{hackathonPopup.event.organizer}</strong> • {hackathonPopup.event.mode.toUpperCase()}
              </div>
              <p style={{ fontSize: "13px", color: "var(--neutral-600)", lineHeight: "1.5", marginBottom: "12px" }}>
                {hackathonPopup.event.description}
              </p>
              <div style={{ fontSize: "12px", color: "var(--neutral-500)", display: "flex", gap: "16px", flexWrap: "wrap" }}>
                <span>📅 Dates: {hackathonPopup.event.date}</span>
                <span>⏳ Deadline: {hackathonPopup.event.deadline}</span>
              </div>
            </div>

            <div style={{ fontSize: "11px", color: "var(--neutral-400)", marginBottom: "20px" }}>
              Verified: {hackathonPopup.data_last_updated} • {hackathonPopup.disclaimer}
            </div>

            <div style={{ display: "flex", justifyContent: "flex-end", gap: "12px" }}>
              <button onClick={handleDismissPopup} className="btn btn-secondary">
                Dismiss for Session
              </button>
              <a href={hackathonPopup.event.official_link} target="_blank" rel="noopener noreferrer" className="btn btn-primary">
                View Official Portal ↗
              </a>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Landing;