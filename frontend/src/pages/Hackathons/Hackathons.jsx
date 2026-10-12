
import { useEffect, useState } from "react";
import { api } from "../../api/client";

export default function Hackathons() {
  const [events, setEvents] = useState([]);
  const [mode, setMode] = useState("");
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;

    async function loadEvents() {
      setLoading(true);
      setError("");

      try {
        const data = await api.hackathons.list(mode, search.trim());
        if (active) setEvents(Array.isArray(data) ? data : []);
      } catch (err) {
        if (active) setError(err.message || "Unable to load hackathons.");
      } finally {
        if (active) setLoading(false);
      }
    }

    loadEvents();

    return () => {
      active = false;
    };
  }, [mode, search]);

  return (
    <div style={styles.page}>
      <header style={styles.hero}>
        <span style={styles.eyebrow}>🚀 BUILD · COLLABORATE · COMPETE</span>
        <h1 style={styles.title}>Hackathons & Innovation Challenges</h1>
        <p style={styles.subtitle}>
          Discover events where you can build projects, collaborate with
          other students and gain practical experience.
        </p>
      </header>

      <section style={styles.filters}>
        <input
          style={styles.search}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search by event or topic..."
          aria-label="Search hackathons"
        />

        <select
          style={styles.select}
          value={mode}
          onChange={(e) => setMode(e.target.value)}
          aria-label="Filter by event mode"
        >
          <option value="">All formats</option>
          <option value="online">Online</option>
          <option value="offline">Offline</option>
          <option value="hybrid">Hybrid</option>
        </select>
      </section>

      {loading && <p style={styles.message}>Loading events...</p>}
      {error && <p style={styles.error}>{error}</p>}

      {!loading && !error && events.length === 0 && (
        <div style={styles.empty}>
          <div style={{ fontSize: 36 }}>🔎</div>
          <h2>No matching hackathons</h2>
          <p>Try another search term or select a different format.</p>
        </div>
      )}

      {!loading && events.length > 0 && (
        <>
          <p style={styles.count}>
            {events.length} event{events.length === 1 ? "" : "s"} found
          </p>

          <div style={styles.grid}>
            {events.map((event) => (
              <article key={event.id ?? `${event.name}-${event.date}`} style={styles.card}>
                <div style={styles.cardTop}>
                  <span style={styles.badge}>
                    {event.mode || "Event"}
                  </span>
                  {event.is_demo && (
                    <span style={styles.demo}>Demo listing</span>
                  )}
                </div>

                <h2 style={styles.eventTitle}>{event.name}</h2>
                <p style={styles.organizer}>
                  Organized by {event.organizer || "Organizer not specified"}
                </p>
                <p style={styles.description}>{event.description}</p>

                <div style={styles.details}>
                  <div>📅 <strong>Date:</strong> {event.date || "Check official page"}</div>
                  <div>⏳ <strong>Deadline:</strong> {event.deadline || "Check official page"}</div>
                  <div>📍 <strong>Location:</strong> {event.location || "Not specified"}</div>
                  <div>🎓 <strong>Eligibility:</strong> {event.eligibility || "Check event guidelines"}</div>
                </div>

                {event.last_verified && (
                  <p style={styles.verified}>
                    Last verified: {event.last_verified}
                  </p>
                )}

                {event.official_link && (
                  <a
                    style={styles.link}
                    href={event.official_link}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    View official details ↗
                  </a>
                )}
              </article>
            ))}
          </div>
        </>
      )}

      <p style={styles.disclaimer}>
        Important: verify event dates, deadlines, eligibility and submission
        rules on the organizer's official website before applying.
      </p>
    </div>
  );
}

const styles = {
  page: { maxWidth: 1100, margin: "0 auto", padding: "28px 20px 60px", color: "#172033" },
  hero: {
    padding: 28,
    borderRadius: 20,
    color: "#fff",
    background: "linear-gradient(125deg, #064e3b, #047857, #0e7490)",
  },
  eyebrow: { fontSize: 12, fontWeight: 800, letterSpacing: 1.3 },
  title: { fontSize: "clamp(26px, 4vw, 38px)", margin: "12px 0" },
  subtitle: { maxWidth: 680, lineHeight: 1.7, color: "#d1fae5" },
  filters: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(210px, 1fr))",
    gap: 12,
    margin: "24px 0 14px",
  },
  search: {
    boxSizing: "border-box",
    width: "100%",
    padding: 13,
    border: "1px solid #cbd5e1",
    borderRadius: 10,
    fontSize: 14,
  },
  select: {
    padding: 13,
    border: "1px solid #cbd5e1",
    borderRadius: 10,
    background: "#fff",
    fontSize: 14,
  },
  message: { padding: 20, color: "#64748b" },
  error: { padding: 16, color: "#b91c1c", background: "#fef2f2", borderRadius: 10 },
  empty: {
    padding: 40,
    textAlign: "center",
    border: "1px dashed #cbd5e1",
    borderRadius: 16,
    color: "#64748b",
  },
  count: { color: "#64748b", fontSize: 13, margin: "16px 0" },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
    gap: 18,
  },
  card: {
    display: "flex",
    flexDirection: "column",
    padding: 22,
    border: "1px solid #e2e8f0",
    borderRadius: 16,
    background: "#fff",
    minWidth: 0,
  },
  cardTop: { display: "flex", flexWrap: "wrap", gap: 8, alignItems: "center" },
  badge: {
    background: "#d1fae5",
    color: "#065f46",
    borderRadius: 20,
    padding: "5px 10px",
    textTransform: "capitalize",
    fontWeight: 800,
    fontSize: 12,
  },
  demo: { fontSize: 11, color: "#92400e", background: "#fef3c7", padding: "5px 8px", borderRadius: 20 },
  eventTitle: { fontSize: 20, lineHeight: 1.4, marginBottom: 6 },
  organizer: { color: "#64748b", fontSize: 13, marginTop: 0 },
  description: { lineHeight: 1.65, fontSize: 14, flexGrow: 1 },
  details: {
    display: "grid",
    gap: 11,
    padding: "15px 0",
    borderTop: "1px solid #e2e8f0",
    fontSize: 13,
    lineHeight: 1.5,
  },
  verified: { fontSize: 11, color: "#64748b" },
  link: {
    display: "inline-block",
    alignSelf: "flex-start",
    marginTop: 10,
    padding: "11px 14px",
    borderRadius: 9,
    background: "#047857",
    color: "#fff",
    textDecoration: "none",
    fontWeight: 700,
    fontSize: 13,
  },
  disclaimer: {
    marginTop: 24,
    padding: 14,
    borderRadius: 10,
    background: "#f8fafc",
    color: "#64748b",
    fontSize: 12,
    lineHeight: 1.7,
  },
};