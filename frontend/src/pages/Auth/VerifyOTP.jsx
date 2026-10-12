import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import AuthShell from "./AuthShell";
import { ErrorMessage } from "../../components/CommonComponents";

export default function VerifyOTP() {
  const { verifyOtp, resendOtp } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const email = location.state?.email || "";
  const [otp, setOtp] = useState("");
  const [error, setError] = useState("");
  const [info, setInfo] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    if (otp.length !== 6) {
      setError("Enter the 6-digit code.");
      return;
    }
    setLoading(true);
    try {
      await verifyOtp(email, otp);
      navigate("/dashboard", { replace: true });
    } catch (err) {
      setError(err.message || "Verification failed.");
    } finally {
      setLoading(false);
    }
  }

  async function handleResend() {
    setError("");
    try {
      await resendOtp(email);
      setInfo("A new code was sent. In development without SMTP, check the backend console.");
    } catch (err) {
      setError(err.message);
    }
  }

  if (!email) {
    return (
      <AuthShell title="Verification required" subtitle="Start from registration or sign-in.">
        <Link to="/register" className="btn btn-primary">Go to registration</Link>
      </AuthShell>
    );
  }

  return (
    <AuthShell title="Verify email" subtitle={`Enter the 6-digit code for ${email}. Development mode prints the code to the backend terminal when SMTP is unset.`}>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label">Code</label>
          <input
            className="form-control"
            inputMode="numeric"
            maxLength={6}
            value={otp}
            onChange={(e) => setOtp(e.target.value.replace(/\D/g, "").slice(0, 6))}
            required
          />
        </div>
        {error && <ErrorMessage message={error} />}
        {info && <div className="alert alert-success">{info}</div>}
        <button className="btn btn-primary" type="submit" disabled={loading} style={{ width: "100%" }}>
          {loading ? "Verifying..." : "Verify and continue"}
        </button>
      </form>
      <button type="button" className="btn btn-secondary" style={{ marginTop: 12, width: "100%" }} onClick={handleResend}>
        Resend code
      </button>
    </AuthShell>
  );
}
