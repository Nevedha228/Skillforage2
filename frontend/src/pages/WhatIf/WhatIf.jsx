
import { useState } from "react";

export default function WhatIf() {
  const [targetRole, setTargetRole] = useState("Data Analyst");
  const [hours, setHours] = useState("1");
  const [weeks, setWeeks] = useState("8");
  const [skills, setSkills] = useState("SQL, Python, Excel");
  const [result, setResult] = useState(false);

  const totalHours = Number(hours) * Number(weeks) * 7;

  function simulate(event) {
    event.preventDefault();
    setResult(true);
  }

  return (
    <main className="whatif-page">
      <style>{`
        .whatif-page {
          max-width: 1050px;
          margin: auto;
          padding: 30px 22px;
          font-family: Inter, system-ui, sans-serif;
          color: var(--text-primary, #20213a);
        }
        .whatif-hero {
          padding: 30px;
          border-radius: 22px;
          color: white;
          background: linear-gradient(125deg, #4338ca, #7c3aed);
          margin-bottom: 24px;
        }
        .whatif-hero h1 { margin: 12px 0; font-size: 32px; }
        .whatif-hero p { line-height: 1.7; margin-bottom: 0; }
        .whatif-card {
          padding: 24px;
          border: 1px solid var(--border-color, #e5e7eb);
          border-radius: 18px;
          background: var(--card-bg, #fff);
          margin-bottom: 20px;
        }
        .whatif-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
          gap: 18px;
          margin: 22px 0;
        }
        .whatif-field label {
          display: block;
          font-size: 14px;
          font-weight: 600;
          margin-bottom: 8px;
        }
        .whatif-field input, .whatif-field select {
          width: 100%;
          box-sizing: border-box;
          padding: 12px;
          border-radius: 10px;
          border: 1px solid var(--border-color, #d1d5db);
          background: var(--input-bg, #fff);
          color: var(--text-primary, #20213a);
          font-size: 14px;
        }
        .whatif-button {
          border: 0;
          border-radius: 10px;
          padding: 13px 20px;
          color: white;
          background: #4f46e5;
          font-weight: 700;
          cursor: pointer;
        }
        .whatif-stat {
          padding: 20px;
          border-radius: 14px;
          background: var(--upload-bg, #f5f3ff);
        }
        .whatif-stat strong {
          display: block;
          font-size: 27px;
          color: #6366f1;
          margin-bottom: 8px;
        }
        .whatif-muted {
          color: var(--text-secondary, #6b7280);
          line-height: 1.7;
          font-size: 14px;
        }
      `}</style>

      <section className="whatif-hero">
        <div style={{ fontSize: 12, letterSpacing: 1.5, fontWeight: 700 }}>
          SKILLFORAGE AI · CAREER SIMULATOR
        </div>
        <h1>What If? 🚀</h1>
        <p>
          Explore how your learning time and target skills could shape
          your career preparation. Build a realistic plan before you begin.
        </p>
      </section>

      <form className="whatif-card" onSubmit={simulate}>
        <h2>Design your future scenario</h2>
        <p className="whatif-muted">
          Change the options below to estimate your learning commitment.
        </p>

        <div className="whatif-grid">
          <div className="whatif-field">
            <label htmlFor="targetRole">Target career</label>
            <select
              id="targetRole"
              value={targetRole}
              onChange={(e) => {
                setTargetRole(e.target.value);
                setResult(false);
              }}
            >
              <option>Data Analyst</option>
              <option>Software Engineer</option>
              <option>Data Scientist</option>
              <option>AI / ML Engineer</option>
              <option>Web Developer</option>
            </select>
          </div>

          <div className="whatif-field">
            <label htmlFor="hours">Learning hours per day</label>
            <select
              id="hours"
              value={hours}
              onChange={(e) => {
                setHours(e.target.value);
                setResult(false);
              }}
            >
              <option value="0.5">30 minutes</option>
              <option value="1">1 hour</option>
              <option value="2">2 hours</option>
              <option value="3">3 hours</option>
              <option value="4">4 hours</option>
            </select>
          </div>

          <div className="whatif-field">
            <label htmlFor="weeks">Plan duration</label>
            <select
              id="weeks"
              value={weeks}
              onChange={(e) => {
                setWeeks(e.target.value);
                setResult(false);
              }}
            >
              <option value="2">2 weeks</option>
              <option value="4">4 weeks</option>
              <option value="8">8 weeks</option>
              <option value="12">12 weeks</option>
              <option value="16">16 weeks</option>
            </select>
          </div>

          <div className="whatif-field">
            <label htmlFor="skills">Skills you want to learn</label>
            <input
              id="skills"
              value={skills}
              onChange={(e) => {
                setSkills(e.target.value);
                setResult(false);
              }}
              placeholder="e.g. SQL, Python, DSA"
            />
          </div>
        </div>

        <button className="whatif-button" type="submit">
          Simulate My Plan →
        </button>
      </form>

      {result && (
        <section className="whatif-card">
          <h2>Your learning scenario 📊</h2>
          <p className="whatif-muted">
            This is a time-budget estimate, not a prediction of employment
            or interview success.
          </p>

          <div className="whatif-grid">
            <div className="whatif-stat">
              <strong>{totalHours}</strong>
              Total planned learning hours
            </div>
            <div className="whatif-stat">
              <strong>{weeks} weeks</strong>
              Preparation timeline
            </div>
            <div className="whatif-stat">
              <strong>{hours} hr/day</strong>
              Daily commitment
            </div>
          </div>

          <h3>Target: {targetRole}</h3>
          <p className="whatif-muted">
            Skills to focus on: {skills.trim() || "Choose your priority skills"}.
          </p>

          <h3>Suggested approach</h3>
          <ol style={{ lineHeight: 1.9 }}>
            <li>Learn the fundamentals of your priority skills.</li>
            <li>Practise through small, hands-on exercises.</li>
            <li>Build a project related to {targetRole}.</li>
            <li>Review your progress and practise interview questions.</li>
          </ol>

          <p className="whatif-muted">
            Actual progress depends on your starting level, practice quality,
            consistency, and the requirements of your target roles.
          </p>
        </section>
      )}
    </main>
  );
}