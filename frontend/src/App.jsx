import { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);

  const [resumeResult, setResumeResult] = useState(null);
  const [atsResult, setAtsResult] = useState(null);

  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!file) {
      alert("Please select a resume PDF");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setResumeResult(null);
    setAtsResult(null);

    try {
      // MODULE 1 — Resume Parsing
      const resumeResponse = await fetch(
        "http://127.0.0.1:8000/parse-resume",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!resumeResponse.ok) {
        throw new Error("Resume parsing failed");
      }

      const resumeData = await resumeResponse.json();
      setResumeResult(resumeData);

      // MODULE 2 — ATS Checker
      const atsFormData = new FormData();
      atsFormData.append("file", file);

      const atsResponse = await fetch(
        "http://127.0.0.1:8000/ats-check",
        {
          method: "POST",
          body: atsFormData,
        }
      );

      if (!atsResponse.ok) {
        throw new Error("ATS checking failed");
      }

      const atsData = await atsResponse.json();
      setAtsResult(atsData);

    } catch (error) {
      console.error(error);
      alert(
        "Something went wrong. Make sure the FastAPI backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">

      {/* HEADER */}
      <header className="hero">
        <div className="logo">SkillForge AI</div>

        <h1>
          Build a <span>Stronger Resume</span>
          <br />
          With AI
        </h1>

        <p>
          Analyze your resume, discover missing skills,
          and improve your chances of getting shortlisted.
        </p>
      </header>


      {/* UPLOAD SECTION */}
      <main>

        <section className="upload-card">

          <div className="upload-icon">
            📄
          </div>

          <h2>Upload Your Resume</h2>

          <p>
            Upload your PDF resume and let SkillForge AI
            analyze it.
          </p>

          <label className="file-input">

            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setFile(e.target.files[0])}
            />

            <span>
              {file ? file.name : "Choose PDF Resume"}
            </span>

          </label>

          <button
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading ? "Analyzing..." : "Analyze Resume →"}
          </button>

        </section>


        {/* ATS RESULT */}
        {atsResult && (
          <section className="ats-section">

            <h2>ATS Resume Checker</h2>

            <div className="score-card">

              <div className="score-circle">
                <strong>
                  {atsResult.ats_analysis.ats_score}
                </strong>

                <span>/100</span>
              </div>

              <div>
                <h3>ATS Score</h3>

                <p>
                  Your resume matches{" "}
                  {atsResult.ats_analysis.ats_score}% of
                  the important keywords.
                </p>
              </div>

            </div>


            {/* MISSING KEYWORDS */}
            <div className="analysis-card">

              <h3>🔑 Missing Keywords</h3>

              {atsResult.ats_analysis.missing_keywords.length > 0 ? (

                <div className="keyword-list">

                  {atsResult.ats_analysis.missing_keywords.map(
                    (keyword, index) => (
                      <span key={index}>
                        {keyword}
                      </span>
                    )
                  )}

                </div>

              ) : (

                <p>No major keywords missing 🎉</p>

              )}

            </div>


            {/* SUGGESTIONS */}
            <div className="analysis-card">

              <h3>💡 Resume Suggestions</h3>

              <ul>

                {atsResult.ats_analysis.suggestions.map(
                  (suggestion, index) => (
                    <li key={index}>
                      {suggestion}
                    </li>
                  )
                )}

              </ul>

            </div>

          </section>
        )}


        {/* MODULE 1 RESULT */}
        {resumeResult && (
          <section className="resume-section">

            <h2>Resume Analysis</h2>

            <div className="resume-card">

              <h3>💻 Skills</h3>
              <p>
                {resumeResult.resume_data.skills}
              </p>

            </div>

            <div className="resume-card">

              <h3>🎓 Education</h3>
              <p>
                {resumeResult.resume_data.education}
              </p>

            </div>

            <div className="resume-card">

              <h3>🚀 Projects</h3>
              <p>
                {resumeResult.resume_data.projects}
              </p>

            </div>

            <div className="resume-card">

              <h3>💼 Experience</h3>
              <p>
                {resumeResult.resume_data.experience}
              </p>

            </div>

          </section>
        )}

      </main>

    </div>
  );
}

export default App;