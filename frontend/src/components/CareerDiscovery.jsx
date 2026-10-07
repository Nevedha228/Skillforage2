import { useEffect, useState } from "react";

const careerOptions = [
  {
    id: "software-developer",
    title: "Software Developer",
    icon: "💻",
    description:
      "Build applications, software systems, and technical solutions using programming.",
    interests: ["Software Development", "Web Development", "App Development"],
    skills: ["Java / Python", "DSA", "OOP", "SQL", "Git"],
  },
  {
    id: "data-analyst",
    title: "Data Analyst",
    icon: "📊",
    description:
      "Analyze data, discover insights, and help organizations make better decisions.",
    interests: ["Data & Analytics", "AI / ML"],
    skills: ["Python", "SQL", "Excel", "Power BI", "Statistics"],
  },
  {
    id: "data-scientist",
    title: "Data Scientist",
    icon: "🧠",
    description:
      "Use statistics, programming, and machine learning to solve data-driven problems.",
    interests: ["Data & Analytics", "AI / ML"],
    skills: ["Python", "SQL", "Statistics", "Machine Learning", "Power BI"],
  },
  {
    id: "ml-engineer",
    title: "Machine Learning Engineer",
    icon: "🤖",
    description:
      "Develop, train, and deploy machine learning models for real-world applications.",
    interests: ["AI / ML", "Data & Analytics"],
    skills: ["Python", "Machine Learning", "Deep Learning", "SQL", "APIs"],
  },
  {
    id: "cloud-engineer",
    title: "Cloud Engineer",
    icon: "☁️",
    description:
      "Design, deploy, and maintain applications and infrastructure on cloud platforms.",
    interests: ["Cloud Computing", "Software Development"],
    skills: ["Cloud Fundamentals", "Linux", "Networking", "Python", "DevOps"],
  },
  {
    id: "cybersecurity",
    title: "Cybersecurity Analyst",
    icon: "🔐",
    description:
      "Protect systems, applications, networks, and data from security threats.",
    interests: ["Cybersecurity"],
    skills: ["Networking", "Linux", "Security Fundamentals", "Python", "Cybersecurity"],
  },
  {
    id: "ui-ux",
    title: "UI / UX Designer",
    icon: "🎨",
    description:
      "Design useful, accessible, and engaging digital experiences for users.",
    interests: ["UI / UX"],
    skills: ["Figma", "UI Design", "UX Research", "Prototyping", "Design Systems"],
  },
];

function CareerDiscovery({ profile, onComplete }) {
  const [recommendedRoles, setRecommendedRoles] = useState([]);
  const [selectedRole, setSelectedRole] = useState(null);

  useEffect(() => {
    if (!profile) return;

    const interests = profile.interests || [];

    const scoredRoles = careerOptions.map((role) => {
      let score = 0;

      role.interests.forEach((interest) => {
        if (interests.includes(interest)) {
          score += 3;
        }
      });

      // Give a small boost to roles that fit the student's situation.
      if (
        profile.careerStatus === "I'm confused" &&
        role.id === "software-developer"
      ) {
        score += 1;
      }

      if (
        profile.careerStatus === "I'm preparing for placements" &&
        ["software-developer", "data-analyst"].includes(role.id)
      ) {
        score += 1;
      }

      return {
        ...role,
        score,
      };
    });

    const sortedRoles = scoredRoles
      .sort((a, b) => b.score - a.score)
      .slice(0, 4);

    setRecommendedRoles(sortedRoles);
  }, [profile]);

  const handleContinue = () => {
    if (!selectedRole) return;

    localStorage.setItem(
      "skillforge_target_role",
      JSON.stringify(selectedRole)
    );

    if (onComplete) {
      onComplete(selectedRole);
    }
  };

  if (!profile) {
    return (
      <section className="career-discovery-section">
        <div className="career-discovery-card">
          <h2>Career Discovery</h2>
          <p>Please complete your student profile first.</p>
        </div>
      </section>
    );
  }

  return (
    <section
      className="career-discovery-section"
      id="career-discovery"
    >
      <div className="career-discovery-header">
        <span className="section-badge">MODULE 2</span>

        <h2>
          Discover Your <span>Career Direction</span>
        </h2>

        <p>
          Based on your interests, career stage, and goals, SkillForge has
          identified career paths you can explore.
        </p>
      </div>

      <div className="career-profile-context">
        <div>
          <span>🎓</span>
          <strong>{profile.year}</strong>
        </div>

        <div>
          <span>🎯</span>
          <strong>{profile.careerStatus}</strong>
        </div>

        <div>
          <span>⏳</span>
          <strong>{profile.timeAvailable}</strong>
        </div>
      </div>

      <div className="career-role-grid">
        {recommendedRoles.map((role) => {
          const isSelected = selectedRole?.id === role.id;

          return (
            <button
              key={role.id}
              className={`career-role-card ${
                isSelected ? "selected" : ""
              }`}
              onClick={() => setSelectedRole(role)}
            >
              <div className="career-role-top">
                <div className="career-role-icon">{role.icon}</div>

                {role.score > 0 && (
                  <span className="career-match">
                    {Math.min(role.score * 10, 100)}% Match
                  </span>
                )}
              </div>

              <h3>{role.title}</h3>

              <p>{role.description}</p>

              <div className="career-skills">
                {role.skills.slice(0, 4).map((skill) => (
                  <span key={skill}>{skill}</span>
                ))}
              </div>

              <div className="career-select">
                {isSelected ? "✓ Selected" : "Choose this path →"}
              </div>
            </button>
          );
        })}
      </div>

      {selectedRole && (
        <div className="career-selected-panel">
          <div>
            <span className="selected-role-icon">
              {selectedRole.icon}
            </span>

            <div>
              <small>Your selected career direction</small>
              <h3>{selectedRole.title}</h3>
            </div>
          </div>

          <button
            className="career-continue-btn"
            onClick={handleContinue}
          >
            Continue with {selectedRole.title}
            <span>→</span>
          </button>
        </div>
      )}
    </section>
  );
}

export default CareerDiscovery;
   