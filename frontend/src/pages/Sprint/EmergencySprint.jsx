
import { useState } from "react";
import { api } from "../../api/client";

export default function EmergencySprint() {
  const [targetRole, setTargetRole] = useState("Data Analyst");
  const [days, setDays] = useState(7);
  const [hours, setHours] = useState(2);
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function generatePlan(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setPlan(null);

    try {
      const result = await api.sprint.plan({
        target_role: targetRole.trim(),
        days_left: Number(days),
        hours_per_day: Number(hours),
      });
      setPlan(result);
    } catch (err) {
      setError(err.message || "Could not generate your sprint plan.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={styles.page}>
      <div style={styles.hero}>
        <span style={styles.eyebrow}>⚡ PLACEMENT MODE</span>
        <h1 style={styles.title}>Emergency Placement Sprint</h1>
        <p style={styles.subtitle}>
          Short on time? Build a focused interview-preparation schedule
          around the time you have available.
        </p>
      </div>

      <form onSubmit={generatePlan} style={styles.card}>
        <h2 style={styles.heading}>Configure your sprint</h2>

        <label style={styles.label}>Target role</label>
        <input
          style={styles.input}
          value={targetRole}
          onChange={(e) => setTargetRole(e.target.value)}
          placeholder="e.g. Data Analyst, Software Engineer"
          required
        />

        <div style={styles.grid}>
          <div>
            <label style={styles.label}>Days remaining</label>
            <input
              style={styles.input}
              type="number"
              min="1"
              max="90"
              value={days}
              onChange={(e) => setDays(e.target.value)}
              required
            />
          </div>

          <div>
            <label style={styles.label}>Study hours per day</label>
            <input
              style={styles.input}
              type="number"
              min="0.5"
              max="16"
              step="0.5"
              value={hours}
              onChange={(e) => setHours(e.target.value)}
              required
            />
          </div>
        </div>

        <p style={styles.helper}>
          Available preparation time:{" "}
          <strong>{(Number(days) * Number(hours)).toFixed(1)} hours</strong>
        </p>

        <button style={styles.button} type="submit" disabled={loading}>
          {loading ? "Building your plan..." : "Generate my sprint →"}
        </button>

        {error && <p style={styles.error}>{error}</p>}
      </form>

      {plan && (
        <section style={styles.results}>
          <div style={styles.summary}>
            <div>
              <span style={styles.metricLabel}>Target role</span>
              <h2 style={styles.heading}>{plan.target_role}</h2>
            </div>
            <div>
              <span style={styles.metricLabel}>Total study time</span>
              <h2 style={styles.heading}>
                {plan.total_dedicated_hours} hrs
              </h2>
            </div>
            <div>
              <span style={styles.metricLabel}>Readiness target</span>
              <h2 style={styles.heading}>{plan.readiness_target_score}%</h2>
            </div>
          </div>

          <p style={styles.notice}>{plan.guidance_message}</p>

          <h2 style={styles.sectionTitle}>Your daily action plan</h2>

          {(plan.daily_schedule || []).map((day) => (
            <article key={day.day_number} style={styles.dayCard}>
              <div style={styles.dayHeader}>
                <span style={styles.dayBadge}>DAY {day.day_number}</span>
                <span style={styles.metricLabel}>
                  {day.time_allocation_hours} hours
                </span>
              </div>

              <h3 style={styles.dayTitle}>{day.focus_topic}</h3>

              <h4 style={styles.subheading}>Today's checklist</h4>
              <ul style={styles.list}>
                {(day.checklist || []).map((task, index) => (
                  <li key={index} style={styles.listItem}>{task}</li>
                ))}
              </ul>

              {day.practice_tasks?.length > 0 && (
                <>
                  <h4 style={styles.subheading}>Practice</h4>
                  <ul style={styles.list}>
                    {day.practice_tasks.map((task, index) => (
                      <li key={index} style={styles.listItem}>{task}</li>
                    ))}
                  </ul>
                </>
              )}

              {day.milestone_check && (
                <div style={styles.milestone}>
                  🎯 {day.milestone_check}
                </div>
              )}
            </article>
          ))}

          {plan.critical_checkpoints?.length > 0 && (
            <>
              <h2 style={styles.sectionTitle}>Important checkpoints</h2>
              {plan.critical_checkpoints.map((item, index) => (
                <div key={index} style={styles.checkpoint}>
                  <strong>Day {item.day}</strong>
                  <span>{item.action}</span>
                </div>
              ))}
            </>
          )}
        </section>
      )}
    </div>
  );
}

const styles = {
  page: {
    maxWidth: 1000,
    margin: "0 auto",
    padding: "28px 20px 60px",
    color: "var(--neutral-900, #172033)",
  },
  hero: {
    padding: "28px",
    borderRadius: 20,
    background: "linear-gradient(125deg, #172554, #4338ca, #6d28d9)",
    color: "#fff",
    marginBottom: 24,
  },
  eyebrow: { fontSize: 12, fontWeight: 800, letterSpacing: 1.5 },
  title: { fontSize: "clamp(26px, 4vw, 38px)", margin: "12px 0" },
  subtitle: { maxWidth: 650, lineHeight: 1.7, color: "#e0e7ff" },
  card: {
    padding: 24,
    border: "1px solid #e2e8f0",
    borderRadius: 18,
    background: "#fff",
    marginBottom: 28,
  },
  heading: { margin: "8px 0 18px", fontSize: 21 },
  label: { display: "block", fontWeight: 700, fontSize: 13, marginBottom: 8 },
  input: {
    boxSizing: "border-box",
    width: "100%",
    padding: "12px 14px",
    border: "1px solid #cbd5e1",
    borderRadius: 10,
    marginBottom: 18,
    fontSize: 15,
    background: "#fff",
    color: "#172033",
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
    gap: 16,
  },
  helper: { color: "#64748b", fontSize: 14, margin: "0 0 20px" },
  button: {
    width: "100%",
    padding: 14,
    border: 0,
    borderRadius: 10,
    background: "#4f46e5",
    color: "#fff",
    fontWeight: 800,
    fontSize: 15,
    cursor: "pointer",
  },
  error: { color: "#b91c1c", marginBottom: 0 },
  results: { display: "grid", gap: 16 },
  summary: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(170px, 1fr))",
    gap: 16,
    padding: 22,
    borderRadius: 16,
    border: "1px solid #e2e8f0",
    background: "#fff",
  },
  metricLabel: { fontSize: 12, color: "#64748b" },
  notice: {
    padding: 16,
    borderRadius: 12,
    background: "#eef2ff",
    color: "#3730a3",
    lineHeight: 1.7,
  },
  sectionTitle: { fontSize: 22, margin: "18px 0 4px" },
  dayCard: {
    padding: 22,
    borderRadius: 16,
    background: "#fff",
    border: "1px solid #e2e8f0",
  },
  dayHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: 12,
  },
  dayBadge: {
    color: "#4338ca",
    background: "#eef2ff",
    borderRadius: 7,
    padding: "6px 10px",
    fontWeight: 800,
    fontSize: 12,
  },
  dayTitle: { fontSize: 18, lineHeight: 1.5 },
  subheading: { fontSize: 14, marginBottom: 8 },
  list: { paddingLeft: 22, lineHeight: 1.8 },
  listItem: { marginBottom: 5 },
  milestone: {
    marginTop: 14,
    padding: 12,
    borderRadius: 9,
    background: "#fef3c7",
    color: "#92400e",
    lineHeight: 1.6,
  },
  checkpoint: {
    display: "flex",
    flexWrap: "wrap",
    gap: 12,
    padding: 16,
    background: "#fff",
    border: "1px solid #e2e8f0",
    borderRadius: 12,
  },
};