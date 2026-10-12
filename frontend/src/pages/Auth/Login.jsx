import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import AuthShell from "./AuthShell";
import { ErrorMessage } from "../../components/CommonComponents";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [email, setEmail] = useState(location.state?.email || "");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(email.trim(), password);
      const next = location.state?.from || "/dashboard";
      navigate(next, { replace: true });
    } catch (err) {
      if (err.status === 403) {
        navigate("/verify-otp", { state: { email: email.trim() } });
        return;
      }
      setError(err.message || "Unable to sign in.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <AuthShell title="Sign in" subtitle="Email and password. Sessions are stored server-side.">
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label" htmlFor="email">College email</label>
          <input id="email" className="form-control" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>
        <div className="form-group">
          <label className="form-label" htmlFor="password">Password</label>
          <input id="password" className="form-control" type="password" value={password} onChange={(e) => setPassword(e.target.value)} minLength={8} required />
        </div>
        {error && <ErrorMessage message={error} />}
        <button className="btn btn-primary" type="submit" disabled={loading} style={{ width: "100%" }}>
          {loading ? "Signing in..." : "Sign in"}
        </button>
      </form>
      <p style={{ marginTop: 16, fontSize: 14 }}>
        New student? <Link to="/register">Create an account</Link>
      </p>
    </AuthShell>
  );
}
