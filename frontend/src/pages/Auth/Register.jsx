import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import AuthShell from "./AuthShell";
import { ErrorMessage } from "../../components/CommonComponents";

const DEGREES = ["B.E.", "B.Tech.", "B.Sc.", "BCA", "MBA", "Other"];
const BRANCHES = ["Computer Science", "Information Technology", "Electronics", "Mechanical", "Civil", "Electrical", "Business", "Other"];

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    year: "1",
    degree: "B.Tech.",
    branch: "Computer Science",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function update(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    if (form.password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }
    setLoading(true);
    try {
      await register({
        ...form,
        year: Number(form.year),
        email: form.email.trim(),
      });
      navigate("/verify-otp", { state: { email: form.email.trim() } });
    } catch (err) {
      setError(err.message || "Unable to register.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <AuthShell title="Create student account" subtitle="Verify your email with a 6-digit code (console in development if SMTP is unset).">
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label">Username</label>
          <input className="form-control" name="username" value={form.username} onChange={update} minLength={2} required />
        </div>
        <div className="form-group">
          <label className="form-label">Email</label>
          <input className="form-control" type="email" name="email" value={form.email} onChange={update} required />
        </div>
        <div className="form-group">
          <label className="form-label">Password</label>
          <input className="form-control" type="password" name="password" value={form.password} onChange={update} minLength={8} required />
        </div>
        <div className="form-group">
          <label className="form-label">Year of study</label>
          <select className="form-select" name="year" value={form.year} onChange={update}>
            <option value="1">Year 1</option>
            <option value="2">Year 2</option>
            <option value="3">Year 3</option>
            <option value="4">Year 4</option>
          </select>
        </div>
        <div className="form-group">
          <label className="form-label">Degree</label>
          <select className="form-select" name="degree" value={form.degree} onChange={update}>
            {DEGREES.map((d) => <option key={d}>{d}</option>)}
          </select>
        </div>
        <div className="form-group">
          <label className="form-label">Branch</label>
          <select className="form-select" name="branch" value={form.branch} onChange={update}>
            {BRANCHES.map((d) => <option key={d}>{d}</option>)}
          </select>
        </div>
        {error && <ErrorMessage message={error} />}
        <button className="btn btn-primary" type="submit" disabled={loading} style={{ width: "100%" }}>
          {loading ? "Sending code..." : "Continue to verification"}
        </button>
      </form>
      <p style={{ marginTop: 16, fontSize: 14 }}>
        Already registered? <Link to="/login">Sign in</Link>
      </p>
    </AuthShell>
  );
}
