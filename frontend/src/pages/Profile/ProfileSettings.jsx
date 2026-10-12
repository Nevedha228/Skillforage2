
import { useState } from "react";

export default function ProfileSettings() {
  const [profile, setProfile] = useState(() => {
    try {
      return {
        username: localStorage.getItem("username") || "",
        email: localStorage.getItem("email") || "",
        degree: localStorage.getItem("degree") || "",
        branch: localStorage.getItem("branch") || "",
        studyYear: localStorage.getItem("studyYear") || "",
      };
    } catch {
      return {
        username: "",
        email: "",
        degree: "",
        branch: "",
        studyYear: "",
      };
    }
  });

  const [saved, setSaved] = useState(false);

  function updateField(event) {
    const { name, value } = event.target;
    setProfile((current) => ({ ...current, [name]: value }));
    setSaved(false);
  }

  function saveProfile(event) {
    event.preventDefault();

    try {
      Object.entries(profile).forEach(([key, value]) => {
        localStorage.setItem(key, value);
      });
      setSaved(true);
    } catch {
      setSaved(false);
    }
  }

  const fields = [
    { name: "username", label: "Username", placeholder: "Your name" },
    { name: "email", label: "Email address", placeholder: "Your email", type: "email" },
    { name: "degree", label: "Degree", placeholder: "e.g. B.Tech CSE" },
    { name: "branch", label: "Branch / Stream", placeholder: "e.g. Computer Science" },
    { name: "studyYear", label: "Year of study", placeholder: "e.g. 4th Year" },
  ];

  return (
    <main style={styles.page}>
      <header style={styles.hero}>
        <p style={styles.eyebrow}>SKILLFORAGE AI · ACCOUNT</p>
        <h1 style={styles.heading}>Profile Settings ⚙️</h1>
        <p style={styles.subtitle}>
          Manage your student details and personalize your learning journey.
        </p>
      </header>

      <form onSubmit={saveProfile} style={styles.card}>
        <h2 style={styles.sectionTitle}>Personal & Academic Details</h2>

        {fields.map((field) => (
          <label key={field.name} style={styles.label}>
            {field.label}
            <input
              name={field.name}
              type={field.type || "text"}
              value={profile[field.name]}
              onChange={updateField}
              placeholder={field.placeholder}
              style={styles.input}
            />
          </label>
        ))}

        <button type="submit" style={styles.button}>
          Save Profile
        </button>

        {saved && (
          <p role="status" style={styles.success}>
            Profile saved successfully! ✅
          </p>
        )}

        <p style={styles.note}>
          These settings are stored in this browser only. They are not
          synced with your backend account.
        </p>
      </form>
    </main>
  );
}

const styles = {
  page: {
    maxWidth: 900,
    margin: "0 auto",
    padding: "28px 20px",
    color: "var(--text-primary, #20213a)",
    fontFamily: "Inter, system-ui, sans-serif",
  },
  hero: {
    padding: 28,
    borderRadius: 20,
    color: "#fff",
    background: "linear-gradient(120deg, #4338ca, #7c3aed)",
    marginBottom: 24,
  },
  eyebrow: { fontSize: 12, letterSpacing: 1.5, fontWeight: 700 },
  heading: { fontSize: 30, margin: "12px 0" },
  subtitle: { lineHeight: 1.7, marginBottom: 0 },
  card: {
    padding: 26,
    borderRadius: 18,
    border: "1px solid var(--border-color, #e5e7eb)",
    background: "var(--card-bg, #fff)",
  },
  sectionTitle: { fontSize: 19, marginTop: 0, marginBottom: 22 },
  label: {
    display: "block",
    fontSize: 14,
    fontWeight: 600,
    marginBottom: 18,
  },
  input: {
    display: "block",
    width: "100%",
    boxSizing: "border-box",
    padding: "12px 14px",
    marginTop: 8,
    border: "1px solid var(--border-color, #d1d5db)",
    borderRadius: 10,
    fontSize: 14,
    background: "var(--input-bg, #fff)",
    color: "var(--text-primary, #20213a)",
  },
  button: {
    border: 0,
    borderRadius: 10,
    padding: "13px 20px",
    color: "#fff",
    background: "#4f46e5",
    fontWeight: 700,
    cursor: "pointer",
  },
  success: { color: "#15803d", marginTop: 16 },
  note: { fontSize: 12, lineHeight: 1.6, color: "#6b7280", marginTop: 20 },
};