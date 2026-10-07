import { useState } from "react";

function StudentProfile({ onComplete }) {
  const [year, setYear] = useState("");
  const [careerStatus, setCareerStatus] = useState("");
  const [interests, setInterests] = useState([]);
  const [timeAvailable, setTimeAvailable] = useState("");

  const interestOptions = [
    "Software Development",
    "Data & Analytics",
    "AI / ML",
    "Cloud Computing",
    "Cybersecurity",
    "Web Development",
    "App Development",
    "UI / UX",
  ];

  const toggleInterest = (interest) => {
    setInterests((current) =>
      current.includes(interest)
        ? current.filter((item) => item !== interest)
        : [...current, interest]
    );
  };

  const handleContinue = () => {
    if (!year) {
      alert("Please select your current year.");
      return;
    }

    if (!careerStatus) {
      alert("Please tell us where you are in your career journey.");
      return;
    }

    if (interests.length === 0) {
      alert("Please select at least one area of interest.");
      return;
    }

    if (!timeAvailable) {
      alert("Please select your available preparation time.");
      return;
    }

    const profile = {
      year,
      careerStatus,
      interests,
      timeAvailable,
    };

    localStorage.setItem(
      "skillforge_student_profile",
      JSON.stringify(profile)
    );

    onComplete(profile);
  };

  return (
    <section className="student-profile-section">

      <div className="student-profile-card">

        <div className="profile-icon">
          🎓
        </div>

        <div className="eyebrow">
          BUILD YOUR JOURNEY
        </div>

        <h2>
          Let's understand
          <span> you first.</span>
        </h2>

        <p className="profile-description">
          SkillForge creates a different learning journey for every
          student. Tell us a little about yourself so we can personalize
          your roadmap.
        </p>

        {/* YEAR */}

        <div className="profile-group">

          <label>
            01 · Where are you in your college journey?
          </label>

          <div className="profile-options year-options">

            {[
              ["1st Year", "🌱", "Explore & build foundations"],
              ["2nd Year", "🌿", "Build skills & projects"],
              ["3rd Year", "🚀", "Specialize & prepare"],
              ["Final Year", "🎯", "Placement focused"],
            ].map(([value, icon, description]) => (

              <button
                key={value}
                type="button"
                className={`profile-option ${
                  year === value ? "selected" : ""
                }`}
                onClick={() => setYear(value)}
              >

                <span className="profile-option-icon">
                  {icon}
                </span>

                <strong>
                  {value}
                </strong>

                <small>
                  {description}
                </small>

                <span className="profile-check">
                  {year === value ? "✓" : ""}
                </span>

              </button>

            ))}

          </div>

        </div>

        {/* CAREER STATUS */}

        <div className="profile-group">

          <label>
            02 · Where are you right now?
          </label>

          <div className="profile-options status-options">

            {[
              [
                "I'm confused",
                "🤔",
                "I don't know which career path suits me",
              ],
              [
                "I want to explore",
                "🔍",
                "I want to discover different career options",
              ],
              [
                "I know my career",
                "🧭",
                "I already have a career direction",
              ],
              [
                "I'm preparing for placements",
                "💼",
                "I want to become interview ready",
              ],
            ].map(([value, icon, description]) => (

              <button
                key={value}
                type="button"
                className={`profile-option ${
                  careerStatus === value ? "selected" : ""
                }`}
                onClick={() => setCareerStatus(value)}
              >

                <span className="profile-option-icon">
                  {icon}
                </span>

                <strong>
                  {value}
                </strong>

                <small>
                  {description}
                </small>

                <span className="profile-check">
                  {careerStatus === value ? "✓" : ""}
                </span>

              </button>

            ))}

          </div>

        </div>

        {/* INTERESTS */}

        <div className="profile-group">

          <label>
            03 · What are you interested in?
          </label>

          <p className="group-hint">
            Select one or more areas.
          </p>

          <div className="interest-grid">

            {interestOptions.map((interest) => (

              <button
                key={interest}
                type="button"
                className={`interest-chip ${
                  interests.includes(interest)
                    ? "selected"
                    : ""
                }`}
                onClick={() => toggleInterest(interest)}
              >

                <span>
                  {interest}
                </span>

                {interests.includes(interest) && (
                  <b>✓</b>
                )}

              </button>

            ))}

          </div>

        </div>

        {/* TIME */}

        <div className="profile-group">

          <label>
            04 · How much time do you have to prepare?
          </label>

          <div className="time-grid">

            {[
              ["Less than 1 month", "⚡"],
              ["1 – 3 months", "🔥"],
              ["3 – 6 months", "🚀"],
              ["6 – 12 months", "🌱"],
              ["More than 1 year", "🌳"],
            ].map(([value, icon]) => (

              <button
                key={value}
                type="button"
                className={`time-option ${
                  timeAvailable === value
                    ? "selected"
                    : ""
                }`}
                onClick={() => setTimeAvailable(value)}
              >

                <span>
                  {icon}
                </span>

                <strong>
                  {value}
                </strong>

              </button>

            ))}

          </div>

        </div>

        {/* CONTINUE */}

        <button
          type="button"
          className="profile-continue-btn"
          onClick={handleContinue}
        >
          Create My Learning Journey
          <span>→</span>
        </button>

      </div>

    </section>
  );
}

export default StudentProfile;