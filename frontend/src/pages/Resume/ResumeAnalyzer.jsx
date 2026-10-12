
import { useState } from "react";

const API_BASE = "http://127.0.0.1:8000";

export default function ResumeAnalyzer() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    const selected = event.target.files?.[0];

    setError("");
    setResult(null);

    if (!selected) {
      setFile(null);
      return;
    }

    if (!selected.name.toLowerCase().endsWith(".pdf")) {
      setFile(null);
      setError("Please upload your resume as a PDF file.");
      event.target.value = "";
      return;
    }

    if (selected.size > 5 * 1024 * 1024) {
      setFile(null);
      setError("Your resume must be smaller than 5 MB.");
      event.target.value = "";
      return;
    }

    setFile(selected);
  };

  const analyzeResume = async () => {
    if (!file) {
      setError("Please select your resume PDF first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      // This endpoint must match the route in your FastAPI backend.
      const response = await fetch(`${API_BASE}/analyze-resume`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(
          data.detail ||
            `Resume analysis failed (HTTP ${response.status}).`
        );
      }

      setResult(data);
    } catch (err) {
      if (err instanceof TypeError) {
        setError(
          "Cannot connect to the backend. Start your FastAPI server and check the API endpoint."
        );
      } else {
        setError(
          err.message || "Something went wrong while analyzing your resume."
        );
      }
    } finally {
      setLoading(false);
    }
  };

  const displayLabel = (key) =>
    key
      .replace(/([A-Z])/g, " $1")
      .replace(/[_-]/g, " ")
      .replace(/\b\w/g, (letter) => letter.toUpperCase());

  const renderValue = (value) => {
    if (value === null || value === undefined || value === "") {
      return "Not available";
    }

    if (Array.isArray(value)) {
      return value.length
        ? value
            .map((item) =>
              typeof item === "object"
                ? JSON.stringify(item)
                : String(item)
            )
            .join(", ")
        : "None found";
    }

    if (typeof value === "object") {
      return JSON.stringify(value, null, 2);
    }

    return String(value);
  };

  const scoreEntry = result
    ? Object.entries(result).find(
        ([key, value]) =>
          /^(ats_?score|score|overall_?score)$/i.test(key) &&
          typeof value === "number"
      )
    : null;

  const score = scoreEntry ? scoreEntry[1] : null;

  return (
    <main className="ra-page">
      <style>{`
        .ra-page {
          max-width: 1100px;
          margin: 0 auto;
          padding: 32px 24px 48px;
          color: var(--text-primary, #20213a);
          font-family: Inter, system-ui, sans-serif;
        }
        .ra-hero {
          padding: 30px;
          border-radius: 22px;
          background: linear-gradient(125deg, #4338ca, #7c3aed);
          color: white;
          margin-bottom: 24px;
        }
        .ra-eyebrow {
          font-size: 12px;
          font-weight: 700;
          letter-spacing: 1.5px;
          text-transform: uppercase;
          opacity: .85;
        }
        .ra-hero h1 {
          font-size: clamp(26px, 4vw, 36px);
          margin: 12px 0;
        }
        .ra-hero p {
          line-height: 1.7;
          max-width: 650px;
          margin: 0;
          opacity: .92;
        }
        .ra-card {
          background: var(--card-bg, #fff);
          border: 1px solid var(--border-color, #e5e7eb);
          border-radius: 18px;
          padding: 24px;
          margin-bottom: 20px;
        }
        .ra-card h2 {
          font-size: 19px;
          margin: 0 0 8px;
        }
        .ra-muted {
          color: var(--text-secondary, #6b7280);
          font-size: 14px;
          line-height: 1.6;
        }
        .ra-upload {
          display: block;
          border: 2px dashed #a5b4fc;
          border-radius: 14px;
          padding: 30px 18px;
          text-align: center;
          cursor: pointer;
          margin: 20px 0;
          background: var(--upload-bg, #f8f7ff);
        }
        .ra-upload:hover {
          border-color: #6366f1;
        }
        .ra-upload input {
          display: block;
          width: 100%;
          max-width: 330px;
          margin: 16px auto 0;
        }
        .ra-primary {
          background: #4f46e5;
          color: white;
          border: 0;
          border-radius: 10px;
          padding: 13px 20px;
          font-size: 14px;
          font-weight: 700;
          cursor: pointer;
        }
        .ra-primary:hover {
          background: #4338ca;
        }
        .ra-primary:disabled {
          opacity: .55;
          cursor: not-allowed;
        }
        .ra-error {
          padding: 14px;
          border-radius: 10px;
          background: #fef2f2;
          color: #b91c1c;
          font-size: 14px;
          margin-top: 16px;
          overflow-wrap: anywhere;
        }
        .ra-score {
          display: flex;
          gap: 20px;
          align-items: center;
          flex-wrap: wrap;
          margin-bottom: 20px;
          padding: 20px;
          border-radius: 14px;
          background: var(--upload-bg, #f8f7ff);
        }
        .ra-score-number {
          font-size: 38px;
          font-weight: 800;
          color: #6366f1;
        }
        .ra-results {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
          gap: 14px;
        }
        .ra-result-item {
          border: 1px solid var(--border-color, #e5e7eb);
          border-radius: 12px;
          padding: 16px;
          min-width: 0;
        }
        .ra-result-item h3 {
          font-size: 13px;
          margin: 0 0 10px;
          color: var(--text-secondary, #6b7280);
        }
        .ra-result-item p {
          white-space: pre-wrap;
          overflow-wrap: anywhere;
          margin: 0;
          font-size: 14px;
          line-height: 1.6;
        }
        .ra-status {
          font-size: 13px;
          margin-top: 12px;
          color: var(--text-secondary, #6b7280);
        }
        @media (max-width: 600px) {
          .ra-page { padding: 18px 12px 32px; }
          .ra-hero, .ra-card { padding: 20px; }
        }
      `}</style>

      <section className="ra-hero">
        <div className="ra-eyebrow">SkillForage AI · Career Toolkit</div>
        <h1>AI Resume Analyzer 📄</h1>
        <p>
          Understand your resume, review the analysis returned by your
          backend, and identify areas to improve your job readiness.
        </p>
      </section>

      <section className="ra-card">
        <h2>Upload your resume</h2>
        <p className="ra-muted">
          Upload a PDF resume to begin. Your analysis depends on the
          capabilities implemented in your backend.
        </p>

        <label className="ra-upload">
          <span style={{ fontSize: 30 }}>☁️</span>
          <p>
            <strong>Choose your resume PDF</strong>
          </p>
          <span className="ra-muted">
            PDF format · Maximum size 5 MB
          </span>
          <input
            type="file"
            accept=".pdf,application/pdf"
            onChange={handleFileChange}
          />
        </label>

        {file && (
          <p className="ra-muted">
            Selected: <strong>{file.name}</strong> (
            {(file.size / 1024).toFixed(1)} KB)
          </p>
        )}

        <button
          className="ra-primary"
          onClick={analyzeResume}
          disabled={!file || loading}
        >
          {loading ? "Analyzing resume..." : "Analyze Resume →"}
        </button>

        {loading && (
          <p className="ra-status">
            Please wait while the backend processes your resume.
          </p>
        )}

        {error && <div className="ra-error">{error}</div>}
      </section>

      {result && (
        <section className="ra-card">
          <h2>Analysis Results</h2>
          <p className="ra-muted">
            Results received successfully from the backend.
          </p>

          {score !== null && (
            <div className="ra-score">
              <div>
                <div className="ra-muted">Reported Resume Score</div>
                <div className="ra-score-number">
                  {score}
                  <span style={{ fontSize: 18 }}>/100</span>
                </div>
              </div>
            </div>
          )}

          <div className="ra-results">
            {Object.entries(result).map(([key, value]) => (
              <article className="ra-result-item" key={key}>
                <h3>{displayLabel(key)}</h3>
                <p>{renderValue(value)}</p>
              </article>
            ))}
          </div>
        </section>
      )}
    </main>
  );
}