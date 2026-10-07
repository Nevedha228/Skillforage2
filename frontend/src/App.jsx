import StudentProfile from "./components/StudentProfile";
import CareerDiscovery from "./components/CareerDiscovery";
import { useState } from "react";
import "./App.css";

const API_BASE_URL = "http://localhost:8000";

function App() {
  // =========================================================
  // STUDENT PROFILE
  // =========================================================

  const [showStudentProfile, setShowStudentProfile] =
    useState(false);

  const [studentProfile, setStudentProfile] = useState(() => {
    try {
      const saved = localStorage.getItem(
        "skillforge_student_profile"
      );

      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });

  // =========================================================
  // TARGET CAREER
  // =========================================================

  const [targetRole, setTargetRole] = useState(() => {
    try {
      const saved = localStorage.getItem(
        "skillforge_target_role"
      );

      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });

  // =========================================================
  // ANALYZER STATE
  // =========================================================

  const [education, setEducation] = useState("");
  const [year, setYear] = useState("");
  const [branch, setBranch] = useState("");
  const [file, setFile] = useState(null);

  const [resumeSkills, setResumeSkills] = useState([]);
  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState("");

  // =========================================================
  // MARKET INTELLIGENCE
  // =========================================================

  const [marketRole, setMarketRole] = useState("Data Analyst");
  const [marketResult, setMarketResult] = useState(null);
  const [marketLoading, setMarketLoading] = useState(false);
  const [marketError, setMarketError] = useState("");

  // =========================================================
  // EDUCATION OPTIONS
  // =========================================================

  const educationOptions = {
    Engineering: {
      duration: "4 Years",
      short: "B.Tech / B.E",
      description:
        "Build strong technical and engineering skills.",
      years: [
        "1st Year",
        "2nd Year",
        "3rd Year",
        "4th Year",
      ],
      branches: ["CSE", "IT"],
    },

    "Arts & Science": {
      duration: "3 Years",
      short: "UG Degree",
      description:
        "Develop academic and industry-ready skills.",
      years: [
        "1st Year",
        "2nd Year",
        "3rd Year",
      ],
      branches: ["BCA"],
    },

    Postgraduate: {
      duration: "2 Years",
      short: "PG Degree",
      description:
        "Advance your technical and professional skills.",
      years: [
        "1st Year",
        "2nd Year",
      ],
      branches: ["MCA"],
    },
  };

  // =========================================================
  // BASE ROADMAP
  // =========================================================

  const roadmapData = {
    "1st Year": [
      {
        priority: "FOUNDATION",
        title: "Programming Fundamentals",
        description:
          "Learn programming basics, problem solving, Git and computer science fundamentals.",
      },
      {
        priority: "SKILLS",
        title: "Build Your Technical Base",
        description:
          "Strengthen one programming language and start solving beginner coding problems.",
      },
      {
        priority: "PROJECT",
        title: "Build Your First Project",
        description:
          "Create a small practical project and publish it on GitHub.",
      },
    ],

    "2nd Year": [
      {
        priority: "CORE",
        title: "Master DSA",
        description:
          "Practice arrays, strings, sorting, searching, recursion and common coding patterns.",
      },
      {
        priority: "DEVELOPMENT",
        title: "Learn Development",
        description:
          "Choose a development path and build real-world applications.",
      },
      {
        priority: "PROJECT",
        title: "Build Portfolio Projects",
        description:
          "Create 2 to 3 meaningful projects that demonstrate your skills.",
      },
    ],

    "3rd Year": [
      {
        priority: "ADVANCED",
        title: "Advanced Technical Skills",
        description:
          "Strengthen DSA, databases, APIs, frameworks and system fundamentals.",
      },
      {
        priority: "INTERNSHIP",
        title: "Prepare for Internships",
        description:
          "Build your resume, GitHub profile and start applying for internships.",
      },
      {
        priority: "INTERVIEW",
        title: "Start Interview Preparation",
        description:
          "Practice aptitude, coding, technical interviews and communication.",
      },
    ],

    "4th Year": [
      {
        priority: "PLACEMENT",
        title: "Placement Preparation",
        description:
          "Focus on coding rounds, aptitude, technical interviews and HR preparation.",
      },
      {
        priority: "PROJECT",
        title: "Finalize Major Project",
        description:
          "Complete a strong final-year project and clearly understand every technology used.",
      },
      {
        priority: "CAREER",
        title: "Become Industry Ready",
        description:
          "Apply consistently to companies and prepare for real interview scenarios.",
      },
    ],
  };

  // =========================================================
  // MAP PROFILE YEAR → ANALYZER YEAR
  // =========================================================

  const getAnalyzerYear = (
    profileYear,
    educationType
  ) => {
    if (!profileYear) return "";

    if (profileYear === "Final Year") {
      if (educationType === "Engineering") {
        return "4th Year";
      }

      if (educationType === "Arts & Science") {
        return "3rd Year";
      }

      if (educationType === "Postgraduate") {
        return "2nd Year";
      }
    }

    return profileYear;
  };

  // =========================================================
  // PERSONALIZED ROADMAP
  // =========================================================

  const getPersonalizedRoadmap = () => {
    const selectedYear =
      studentProfile?.year || year || "1st Year";

    // Final Year has a different name in StudentProfile
    const roadmapYear =
      selectedYear === "Final Year"
        ? "4th Year"
        : selectedYear;

    const status =
      studentProfile?.careerStatus || "";

    const interests =
      studentProfile?.interests || [];

    const time =
      studentProfile?.timeAvailable || "";

    const baseRoadmap =
      roadmapData[roadmapYear] ||
      roadmapData["1st Year"];

    const roadmap = [...baseRoadmap];

    // -------------------------------------------------------
    // TARGET ROLE
    // -------------------------------------------------------

    if (targetRole) {
      roadmap.unshift({
        priority: "TARGET ROLE",
        title: `Prepare for ${targetRole.title}`,
        description:
          `Your roadmap is now aligned toward ${targetRole.title}. Focus your learning and projects around the skills required for this career direction.`,
      });
    }

    // -------------------------------------------------------
    // CAREER STATUS
    // -------------------------------------------------------

    if (
      status === "I'm confused" ||
      status === "I want to explore"
    ) {
      roadmap.unshift({
        priority: "DISCOVERY",
        title: "Explore Your Career Direction",
        description:
          "Explore different technology paths and identify the roles that best match your interests before committing to one specialization.",
      });
    }

    if (
      status === "I'm preparing for placements"
    ) {
      roadmap.unshift({
        priority: "PLACEMENT",
        title: "Build Interview Readiness",
        description:
          "Start focusing on coding, aptitude, SQL, technical fundamentals and communication alongside your core technical skills.",
      });
    }

    if (
      status === "I know my career"
    ) {
      roadmap.unshift({
        priority: "SPECIALIZATION",
        title: "Strengthen Your Career Path",
        description:
          "Focus your learning around your selected interests and build projects that demonstrate job-ready skills.",
      });
    }

    // -------------------------------------------------------
    // INTEREST PERSONALIZATION
    // -------------------------------------------------------

    if (
      interests.includes("Data & Analytics") ||
      interests.includes("AI / ML")
    ) {
      roadmap.push({
        priority: "DATA & AI",
        title: "Build a Data / AI Project",
        description:
          "Practice Python, SQL, data analysis and machine learning through a practical project that can be added to your portfolio.",
      });
    }

    if (
      interests.includes("Software Development") ||
      interests.includes("Web Development")
    ) {
      roadmap.push({
        priority: "DEVELOPMENT",
        title: "Build a Real-World Application",
        description:
          "Develop a practical application and strengthen programming, APIs, databases and version control.",
      });
    }

    if (
      interests.includes("Cloud Computing")
    ) {
      roadmap.push({
        priority: "CLOUD",
        title: "Build Cloud Foundations",
        description:
          "Understand cloud fundamentals and deploy a small project to gain practical cloud experience.",
      });
    }

    if (
      interests.includes("Cybersecurity")
    ) {
      roadmap.push({
        priority: "SECURITY",
        title: "Build Security Foundations",
        description:
          "Learn networking, authentication, common security concepts and safe application practices.",
      });
    }

    // -------------------------------------------------------
    // TIME PERSONALIZATION
    // -------------------------------------------------------

    if (
      time === "Less than 1 month" ||
      time === "1 – 3 months"
    ) {
      roadmap.push({
        priority: "HIGH IMPACT",
        title: "Prioritize High-Impact Preparation",
        description:
          "Focus on the most important skills, resume improvements, coding practice and interview preparation instead of trying to learn everything at once.",
      });
    }

    if (
      time === "3 – 6 months"
    ) {
      roadmap.push({
        priority: "CONSISTENCY",
        title: "Follow a Structured Preparation Plan",
        description:
          "Balance technical learning, projects, coding practice and interview preparation throughout your preparation period.",
      });
    }

    if (
      time === "6 – 12 months" ||
      time === "More than 1 year"
    ) {
      roadmap.push({
        priority: "LONG TERM",
        title: "Build Deep Technical Expertise",
        description:
          "Use your longer preparation window to build strong fundamentals, complete substantial projects and gradually specialize.",
      });
    }

    return roadmap;
  };

  const roadmap = getPersonalizedRoadmap();

  // =========================================================
  // PROFILE COMPLETION
  // =========================================================

  const handleProfileComplete = (
    profile
  ) => {
    setStudentProfile(profile);
    setShowStudentProfile(false);

    localStorage.setItem(
      "skillforge_student_profile",
      JSON.stringify(profile)
    );

    // Do not directly set "Final Year".
    // We will map it when education is selected.

    if (education) {
      setYear(
        getAnalyzerYear(
          profile?.year,
          education
        )
      );
    } else {
      setYear("");
    }

    // Clear previous analysis

    setResult(null);
    setResumeSkills([]);
    setError("");

    // Scroll to analyzer

    setTimeout(() => {
      document
        .getElementById("analyzer")
        ?.scrollIntoView({
          behavior: "smooth",
        });
    }, 200);
  };

  // =========================================================
  // CAREER DISCOVERY COMPLETE
  // =========================================================

  const handleCareerComplete = (
    role
  ) => {
    setTargetRole(role);
    setMarketRole(role?.title || "Data Analyst");
    setMarketResult(null);
    setMarketError("");

    localStorage.setItem(
      "skillforge_target_role",
      JSON.stringify(role)
    );

    setTimeout(() => {
      document
        .getElementById("analyzer")
        ?.scrollIntoView({
          behavior: "smooth",
        });
    }, 200);
  };

  // =========================================================
  // MARKET INTELLIGENCE
  // =========================================================

  const handleMarketAnalysis = async () => {
    const role = marketRole.trim();

    if (!role) {
      setMarketError("Please enter a target role.");
      return;
    }

    setMarketLoading(true);
    setMarketError("");
    setMarketResult(null);

    try {
      console.log("=================================");
      console.log("SKILLFORGE MARKET INTELLIGENCE");
      console.log("=================================");
      console.log("Target Role:", role);

      const response = await fetch(
        `${API_BASE_URL}/market/analyze?role=${encodeURIComponent(
          role
        )}&country=in&pages=1&results_per_page=20`,
        {
          method: "POST",
        }
      );

      if (!response.ok) {
        const errorText = await response.text();

        console.error(
          "MARKET ANALYSIS SERVER ERROR:",
          errorText
        );

        throw new Error(
          `Market analysis failed (${response.status}).`
        );
      }

      const payload = await response.json();

      console.log("MARKET ANALYSIS RESPONSE:");
      console.log(payload);

      if (payload?.success === false) {
        throw new Error(
          payload.message ||
            "Market analysis failed."
        );
      }

      const marketData =
        payload?.data ||
        payload?.market_analysis ||
        payload;

      setMarketResult(marketData);

      console.log(
        "Market analysis completed successfully."
      );
    } catch (err) {
      console.error(
        "MARKET INTELLIGENCE ERROR:",
        err
      );

      setMarketError(
        err.message ||
          "Unable to load market intelligence. Make sure the FastAPI backend is running."
      );
    } finally {
      setMarketLoading(false);
    }
  };

  // =========================================================
  // OPEN STUDENT PROFILE
  // =========================================================

  const openStudentProfile = () => {
    setShowStudentProfile(true);

    setTimeout(() => {
      document
        .getElementById("student-profile")
        ?.scrollIntoView({
          behavior: "smooth",
        });
    }, 100);
  };

  // =========================================================
  // EDUCATION CHANGE
  // =========================================================

  const handleEducationChange = (
    value
  ) => {
    setEducation(value);

    // Automatically map profile year
    const mappedYear =
      getAnalyzerYear(
        studentProfile?.year,
        value
      );

    setYear(mappedYear);

    setBranch("");
    setResult(null);
    setResumeSkills([]);
    setError("");
  };

  // =========================================================
  // FILE HANDLING
  // =========================================================

  const handleFileChange = (
    selectedFile
  ) => {
    if (!selectedFile) return;

    const fileName =
      selectedFile.name.toLowerCase();

    const valid =
      fileName.endsWith(".pdf") ||
      fileName.endsWith(".doc") ||
      fileName.endsWith(".docx");

    if (!valid) {
      setError(
        "Please upload a PDF, DOC or DOCX resume."
      );
      return;
    }

    if (
      selectedFile.size >
      5 * 1024 * 1024
    ) {
      setError(
        "Resume size must be less than 5 MB."
      );
      return;
    }

    setFile(selectedFile);
    setResumeSkills([]);
    setResult(null);
    setError("");
  };

  const handleInputFile = (
    event
  ) => {
    handleFileChange(
      event.target.files[0]
    );
  };

  const handleDragOver = (
    event
  ) => {
    event.preventDefault();
    setDragActive(true);
  };

  const handleDragLeave = (
    event
  ) => {
    event.preventDefault();
    setDragActive(false);
  };

  const handleDrop = (
    event
  ) => {
    event.preventDefault();
    setDragActive(false);

    const droppedFile =
      event.dataTransfer.files[0];

    handleFileChange(
      droppedFile
    );
  };

  // =========================================================
  // ANALYZE RESUME
  // =========================================================

  const analyzeSkillGap =
    async () => {
      setError("");
      setResult(null);

      if (!education) {
        setError(
          "Please select your education level."
        );
        return;
      }

      if (!year) {
        setError(
          "Please select your current year."
        );
        return;
      }

      if (!branch) {
        setError(
          "Please select your branch."
        );
        return;
      }

      if (!file) {
        setError(
          "Please upload your resume."
        );
        return;
      }

      setLoading(true);

      try {
        // -----------------------------------------------------
        // Convert frontend values to backend values
        // -----------------------------------------------------

        const educationValue =
          education === "Engineering"
            ? "engineering"
            : education === "Arts & Science"
            ? "arts_science"
            : "pg";

        const yearValue =
          year.charAt(0);

        const branchValue =
          branch.toLowerCase();

        // -----------------------------------------------------
        // Create FormData
        // -----------------------------------------------------

        const formData =
          new FormData();

        formData.append(
          "file",
          file
        );

        formData.append(
          "education",
          educationValue
        );

        formData.append(
          "year",
          yearValue
        );

        formData.append(
          "branch",
          branchValue
        );

        // -----------------------------------------------------
        // Student Profile
        // -----------------------------------------------------

        if (studentProfile) {
          formData.append(
            "career_status",
            studentProfile.careerStatus || ""
          );

          formData.append(
            "interests",
            JSON.stringify(
              studentProfile.interests || []
            )
          );

          formData.append(
            "time_available",
            studentProfile.timeAvailable || ""
          );
        }

        // -----------------------------------------------------
        // Target Career
        // -----------------------------------------------------

        if (targetRole) {
          formData.append(
            "target_role",
            targetRole.title || ""
          );
        }

        console.log(
          "================================="
        );

        console.log(
          "SKILLFORGE AI ANALYSIS"
        );

        console.log(
          "================================="
        );

        console.log(
          "Education:",
          educationValue
        );

        console.log(
          "Year:",
          yearValue
        );

        console.log(
          "Branch:",
          branchValue
        );

        console.log(
          "Student Profile:",
          studentProfile
        );

        console.log(
          "Target Role:",
          targetRole
        );

        console.log(
          "File:",
          file.name
        );

        console.log(
          "Endpoint:",
          `${API_BASE_URL}/analyze`
        );

        // -----------------------------------------------------
        // CALL BACKEND
        // -----------------------------------------------------

        let response;

        try {
          response =
            await fetch(
              `${API_BASE_URL}/analyze`,
              {
                method: "POST",
                body: formData,
              }
            );
        } catch (
          networkError
        ) {
          console.error(
            "ANALYSIS NETWORK ERROR:",
            networkError
          );

          throw new Error(
            "Cannot connect to SkillForge AI backend. Make sure FastAPI is running on http://localhost:8000."
          );
        }

        // -----------------------------------------------------
        // SERVER RESPONSE
        // -----------------------------------------------------

        if (!response.ok) {
          const errorText =
            await response.text();

          console.error(
            "ANALYSIS SERVER ERROR:",
            errorText
          );

          throw new Error(
            `Analysis failed (${response.status}).`
          );
        }

        // -----------------------------------------------------
        // READ JSON
        // -----------------------------------------------------

        const data =
          await response.json();

        console.log(
          "================================="
        );

        console.log(
          "ANALYZE RESPONSE"
        );

        console.log(
          "================================="
        );

        console.log(data);

        // -----------------------------------------------------
        // BACKEND FAILURE
        // -----------------------------------------------------

        if (!data.success) {
          throw new Error(
            data.message ||
              "Resume analysis failed."
          );
        }

        // -----------------------------------------------------
        // RESUME SKILLS
        // -----------------------------------------------------

        if (
          Array.isArray(
            data.resume_skills
          )
        ) {
          setResumeSkills(
            data.resume_skills
          );
        }

        // -----------------------------------------------------
        // COMPLETE RESULT
        // -----------------------------------------------------

        setResult(data);

        console.log(
          "ATS SCORE:",
          data.ats_score
        );

        console.log(
          "SKILL GAP SCORE:",
          data.skill_gap_score
        );

        console.log(
          "MATCHED SKILLS:",
          data.matched_skills
        );

        console.log(
          "MISSING SKILLS:",
          data.missing_skills
        );

        // -----------------------------------------------------
        // SCROLL TO RESULTS
        // -----------------------------------------------------

        setTimeout(() => {
          document
            .getElementById(
              "results"
            )
            ?.scrollIntoView({
              behavior:
                "smooth",
            });
        }, 300);
      } catch (err) {
        console.error(
          "ANALYSIS ERROR:",
          err
        );

        setError(
          err.message ||
            "Something went wrong while analyzing your resume."
        );
      } finally {
        setLoading(false);
      }
    };

  // =========================================================
  // RESET ANALYSIS
  // =========================================================

  const resetAnalysis =
    () => {
      setEducation("");

      setYear("");

      setBranch("");

      setFile(null);

      setResumeSkills([]);

      setResult(null);

      setError("");

      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    };

  // =========================================================
  // RESET COMPLETE JOURNEY
  // =========================================================

  const resetJourney =
    () => {
      localStorage.removeItem(
        "skillforge_student_profile"
      );

      localStorage.removeItem(
        "skillforge_target_role"
      );

      setStudentProfile(null);

      setTargetRole(null);
      setMarketRole("Data Analyst");
      setMarketResult(null);
      setMarketError("");

      setShowStudentProfile(
        false
      );

      setEducation("");

      setYear("");

      setBranch("");

      setFile(null);

      setResumeSkills([]);

      setResult(null);

      setError("");

      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    };

  // =========================================================
  // RESULT DATA
  // =========================================================

  const skillGapScore =
    Number(
      result?.skill_gap_score ??
        result?.skill_gap
          ?.skill_gap_score ??
        result?.score ??
        0
    );

  const atsScore =
    Number(
      result?.ats_score ??
        result?.ats_analysis
          ?.ats_score ??
        0
    );

  const matchedSkills =
    Array.isArray(
      result?.matched_skills
    )
      ? result.matched_skills
      : Array.isArray(
          result?.skill_gap
            ?.matched_skills
        )
      ? result.skill_gap
          .matched_skills
      : [];

  const missingSkills =
    Array.isArray(
      result?.missing_skills
    )
      ? result.missing_skills
      : Array.isArray(
          result?.skill_gap
            ?.missing_skills
        )
      ? result.skill_gap
          .missing_skills
      : [];

  // =========================================================
  // ANALYZER PROGRESS
  // =========================================================

  const progressPercent =
    result
      ? 100
      : file
      ? 80
      : branch
      ? 60
      : year
      ? 40
      : education
      ? 20
      : 0;

  const progressText =
    result
      ? "Analysis Complete"
      : education
      ? year
        ? branch
          ? file
            ? "Ready to Analyze"
            : "Upload your resume"
          : "Select your branch"
        : "Select your year"
      : "Start by selecting education";

  // =========================================================
  // UI
  // =========================================================

  return (
    <div className="app">

      {/* =====================================================
          NAVBAR
      ===================================================== */}

      <nav className="navbar">

        <div className="nav-inner">

          <a
            href="#home"
            className="brand"
          >

            <div className="brand-icon">
              ⚡
            </div>

            <div>

              <span className="brand-name">
                SkillForge
              </span>

              <span className="brand-ai">
                AI
              </span>

            </div>

          </a>

          <div className="nav-links">

            <a href="#home">
              Home
            </a>

            <a href="#how-it-works">
              How It Works
            </a>

            <a href="#career-discovery">
              Career Discovery
            </a>

            <a href="#analyzer">
              Analyzer
            </a>

            <a href="#roadmap">
              Roadmap
            </a>

            <a href="#market-pulse">
              Market Pulse
            </a>

          </div>

          <div className="nav-status">

            <span className="status-dot"></span>

            AI Engine Online

          </div>

        </div>

      </nav>


      {/* =====================================================
          HERO
      ===================================================== */}

      <section
        className="hero"
        id="home"
      >

        <div className="hero-glow glow-one"></div>

        <div className="hero-glow glow-two"></div>

        <div className="hero-content">

          <div className="hero-badge">
            ✨ AI-POWERED CAREER INTELLIGENCE
          </div>

          <h1>
            Forge Your Skills.
            <br />

            <span>
              Shape Your Future.
            </span>

          </h1>

          <p>
            Discover your skill gaps, understand exactly
            what to learn next, and follow a personalized
            roadmap built around your academic journey.
          </p>

          <div className="hero-actions">

            <button
              className="primary-hero-btn"
              onClick={
                openStudentProfile
              }
            >

              {studentProfile
                ? "Update My Journey"
                : "Start Your Journey"}

              <span>
                →
              </span>

            </button>

            <button
              className="secondary-hero-btn"
              onClick={() =>
                document
                  .getElementById(
                    "how-it-works"
                  )
                  ?.scrollIntoView({
                    behavior:
                      "smooth",
                  })
              }
            >
              See How It Works
            </button>

          </div>

          <div className="hero-trust">

            <div>

              <strong>
                AI
              </strong>

              <span>
                Resume Analysis
              </span>

            </div>

            <div>

              <strong>
                100+
              </strong>

              <span>
                Skills Tracked
              </span>

            </div>

            <div>

              <strong>
                4
              </strong>

              <span>
                Career Stages
              </span>

            </div>

          </div>

        </div>


        {/* =====================================================
            DASHBOARD PREVIEW
        ===================================================== */}

        <div className="hero-dashboard">

          <div className="dashboard-window">

            <div className="window-header">

              <div className="window-dots">

                <span></span>
                <span></span>
                <span></span>

              </div>

              <div className="window-title">
                skillforge-ai / dashboard
              </div>

            </div>

            <div className="dashboard-body">

              <div className="mini-welcome">

                <div>

                  <small>
                    YOUR CAREER DASHBOARD
                  </small>

                  <h3>
                    Skill Analysis Overview
                  </h3>

                </div>

                <div className="mini-avatar">
                  AI
                </div>

              </div>

              <div className="mini-stats">

                <div className="mini-card">

                  <span>
                    Skill Match
                  </span>

                  <strong>
                    72%
                  </strong>

                  <small>
                    ↑ Improving
                  </small>

                </div>

                <div className="mini-card">

                  <span>
                    Matched Skills
                  </span>

                  <strong>
                    12
                  </strong>

                  <small>
                    ✓ Strong
                  </small>

                </div>

                <div className="mini-card">

                  <span>
                    Skills to Learn
                  </span>

                  <strong>
                    8
                  </strong>

                  <small>
                    → Your roadmap
                  </small>

                </div>

              </div>

              <div className="mini-analysis">

                <div className="mini-panel">

                  <div className="panel-heading">

                    <span>
                      Technical Skill Strength
                    </span>

                    <small>
                      AI Analysis
                    </small>

                  </div>

                  <div className="skill-bars">

                    <div>

                      <span>
                        Java
                      </span>

                      <div className="bar">

                        <i
                          style={{
                            width:
                              "88%",
                          }}
                        ></i>

                      </div>

                      <b>
                        88%
                      </b>

                    </div>

                    <div>

                      <span>
                        Python
                      </span>

                      <div className="bar">

                        <i
                          style={{
                            width:
                              "76%",
                          }}
                        ></i>

                      </div>

                      <b>
                        76%
                      </b>

                    </div>

                    <div>

                      <span>
                        React
                      </span>

                      <div className="bar">

                        <i
                          style={{
                            width:
                              "61%",
                          }}
                        ></i>

                      </div>

                      <b>
                        61%
                      </b>

                    </div>

                    <div>

                      <span>
                        SQL
                      </span>

                      <div className="bar">

                        <i
                          style={{
                            width:
                              "82%",
                          }}
                        ></i>

                      </div>

                      <b>
                        82%
                      </b>

                    </div>

                  </div>

                </div>


                <div className="mini-panel">

                  <div className="panel-heading">

                    <span>
                      Career Roadmap
                    </span>

                    <small>
                      4 stages
                    </small>

                  </div>

                  <div className="preview-step active">

                    <span>
                      01
                    </span>

                    <div>

                      <strong>
                        Foundation
                      </strong>

                      <small>
                        Core fundamentals
                      </small>

                    </div>

                  </div>

                  <div className="preview-step">

                    <span>
                      02
                    </span>

                    <div>

                      <strong>
                        Development
                      </strong>

                      <small>
                        Build projects
                      </small>

                    </div>

                  </div>

                  <div className="preview-step">

                    <span>
                      03
                    </span>

                    <div>

                      <strong>
                        Internship
                      </strong>

                      <small>
                        Gain experience
                      </small>

                    </div>

                  </div>

                </div>

              </div>

            </div>

          </div>

        </div>

      </section>


      {/* =====================================================
          STUDENT PROFILE
      ===================================================== */}

      {showStudentProfile && (

        <section
          id="student-profile"
          className="student-profile-wrapper"
        >

          <StudentProfile
            onComplete={
              handleProfileComplete
            }
          />

        </section>

      )}


      {/* =====================================================
          PROFILE SUMMARY
      ===================================================== */}

      {studentProfile &&
        !showStudentProfile && (

          <section className="profile-summary-section">

            <div className="profile-summary-card">

              <div>

                <div className="eyebrow">
                  YOUR PERSONALIZED JOURNEY
                </div>

                <h3>
                  SkillForge knows where you're going.
                </h3>

                <p>
                  Your roadmap is being personalized using
                  your academic year, career direction,
                  interests and preparation time.
                </p>

              </div>

              <div className="profile-summary-tags">

                <span>
                  🎓 {studentProfile.year}
                </span>

                <span>
                  🧭 {studentProfile.careerStatus}
                </span>

                <span>
                  ⏱️ {studentProfile.timeAvailable}
                </span>

                {studentProfile.interests
                  ?.slice(0, 3)
                  .map(
                    (
                      interest
                    ) => (

                      <span
                        key={interest}
                      >
                        🎯 {interest}
                      </span>

                    )
                  )}

              </div>

              <div className="profile-summary-actions">

                <button
                  type="button"
                  onClick={
                    openStudentProfile
                  }
                >
                  Update Journey
                </button>

                <button
                  type="button"
                  onClick={
                    resetJourney
                  }
                >
                  Reset Journey
                </button>

              </div>

            </div>

          </section>

        )}


      {/* =====================================================
          CAREER DISCOVERY
      ===================================================== */}

      {studentProfile &&
        !showStudentProfile && (

          <CareerDiscovery
            profile={
              studentProfile
            }
            onComplete={
              handleCareerComplete
            }
          />

        )}


      {/* =====================================================
          SELECTED CAREER SUMMARY
      ===================================================== */}

      {targetRole &&
        studentProfile &&
        !showStudentProfile && (

          <section
            style={{
              maxWidth:
                "1200px",
              margin:
                "0 auto 40px",
              padding:
                "0 24px",
            }}
          >

            <div
              style={{
                padding:
                  "18px 20px",
                borderRadius:
                  "16px",
                background:
                  "linear-gradient(135deg, #f5f3ff, #fafaff)",
                border:
                  "1px solid #e4e0ff",
                display:
                  "flex",
                alignItems:
                  "center",
                justifyContent:
                  "space-between",
                gap:
                  "15px",
                flexWrap:
                  "wrap",
              }}
            >

              <div>

                <div
                  style={{
                    fontSize:
                      "10px",
                    fontWeight:
                      "800",
                    letterSpacing:
                      "1.4px",
                    color:
                      "#6366f1",
                    marginBottom:
                      "5px",
                  }}
                >
                  YOUR TARGET CAREER
                </div>

                <strong
                  style={{
                    fontSize:
                      "20px",
                  }}
                >
                  {targetRole.icon}{" "}
                  {targetRole.title}
                </strong>

              </div>

              <button
                type="button"
                onClick={() =>
                  document
                    .getElementById(
                      "career-discovery"
                    )
                    ?.scrollIntoView({
                      behavior:
                        "smooth",
                    })
                }
                style={{
                  border:
                    "1px solid #6366f1",
                  background:
                    "white",
                  color:
                    "#6366f1",
                  padding:
                    "10px 15px",
                  borderRadius:
                    "10px",
                  fontWeight:
                    "700",
                  cursor:
                    "pointer",
                }}
              >
                Change Career →
              </button>

            </div>

          </section>

        )}


      {/* =====================================================
          MARKET INTELLIGENCE / MARKET PULSE
      ===================================================== */}

      <section
        className="market-pulse-section"
        id="market-pulse"
        style={{
          maxWidth: "1200px",
          margin: "0 auto 70px",
          padding: "0 24px",
        }}
      >
        <div
          style={{
            padding: "30px",
            borderRadius: "24px",
            background: "linear-gradient(135deg, #f8f7ff, #ffffff, #f5f3ff)",
            border: "1px solid #e7e3ff",
            boxShadow: "0 18px 45px rgba(99,102,241,0.08)",
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: "20px", flexWrap: "wrap" }}>
            <div>
              <div style={{ fontSize: "10px", fontWeight: "800", letterSpacing: "1.6px", color: "#6366f1", marginBottom: "8px" }}>
                📊 LABOR MARKET INTELLIGENCE
              </div>
              <h2 style={{ margin: "0 0 8px", fontSize: "32px", lineHeight: "1.15" }}>
                What Does the Market Want?
              </h2>
              <p style={{ margin: 0, maxWidth: "680px", color: "#667085", fontSize: "14px", lineHeight: "1.7" }}>
                SkillForage analyzes collected job-posting data to show which skills are currently appearing most often for your target career.
              </p>
            </div>
            <div style={{ padding: "10px 13px", borderRadius: "999px", background: "#ffffff", border: "1px solid #e4e7ec", color: "#475467", fontSize: "10px", fontWeight: "800", letterSpacing: "0.8px" }}>
              LIVE MARKET ENGINE
            </div>
          </div>

          <div style={{ marginTop: "25px", padding: "18px", borderRadius: "18px", background: "#ffffff", border: "1px solid #e4e7ec", display: "flex", alignItems: "center", gap: "12px", flexWrap: "wrap" }}>
            <div style={{ flex: "1 1 300px" }}>
              <label style={{ display: "block", fontSize: "10px", fontWeight: "800", letterSpacing: "1px", color: "#667085", marginBottom: "7px" }}>
                TARGET ROLE
              </label>
              <input
                type="text"
                value={marketRole}
                onChange={(event) => setMarketRole(event.target.value)}
                onKeyDown={(event) => { if (event.key === "Enter") handleMarketAnalysis(); }}
                placeholder="e.g. Data Analyst"
                style={{ width: "100%", boxSizing: "border-box", padding: "13px 14px", borderRadius: "12px", border: "1px solid #d0d5dd", outline: "none", fontSize: "14px", fontWeight: "600", color: "#101828", background: "#ffffff" }}
              />
            </div>
            <button
              type="button"
              onClick={handleMarketAnalysis}
              disabled={marketLoading}
              style={{ minHeight: "47px", padding: "0 20px", border: "none", borderRadius: "12px", background: "linear-gradient(135deg, #6366f1, #7c3aed)", color: "#ffffff", fontWeight: "800", cursor: marketLoading ? "wait" : "pointer", opacity: marketLoading ? 0.75 : 1, whiteSpace: "nowrap" }}
            >
              {marketLoading ? "Analyzing..." : "Analyze Market →"}
            </button>
          </div>

          {marketError && (
            <div style={{ marginTop: "14px", padding: "13px 15px", borderRadius: "12px", background: "#fff5f5", border: "1px solid #fecaca", color: "#dc2626", fontSize: "12px", fontWeight: "600" }}>
              ⚠️ {marketError}
            </div>
          )}

          {marketResult && (
            <div style={{ marginTop: "25px" }}>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: "12px", marginBottom: "22px" }}>
                <div style={{ padding: "20px", borderRadius: "17px", background: "#ffffff", border: "1px solid #e4e7ec" }}>
                  <span style={{ fontSize: "10px", fontWeight: "800", color: "#667085" }}>ROLE ANALYZED</span>
                  <strong style={{ display: "block", marginTop: "8px", fontSize: "20px", color: "#101828" }}>{marketResult.role || marketRole}</strong>
                </div>
                <div style={{ padding: "20px", borderRadius: "17px", background: "#ffffff", border: "1px solid #e4e7ec" }}>
                  <span style={{ fontSize: "10px", fontWeight: "800", color: "#667085" }}>JOBS ANALYZED</span>
                  <strong style={{ display: "block", marginTop: "8px", fontSize: "28px", color: "#6366f1" }}>{marketResult.top_skills?.[0]?.total_jobs ?? 0}</strong>
                </div>
                <div style={{ padding: "20px", borderRadius: "17px", background: "#ffffff", border: "1px solid #e4e7ec" }}>
                  <span style={{ fontSize: "10px", fontWeight: "800", color: "#667085" }}>TOP SKILL</span>
                  <strong style={{ display: "block", marginTop: "8px", fontSize: "20px", color: "#101828" }}>{marketResult.top_skills?.[0]?.skill || "No data"}</strong>
                  <small style={{ color: "#667085" }}>{marketResult.top_skills?.[0] ? `${marketResult.top_skills[0].demand_percentage}% demand` : ""}</small>
                </div>
                <div style={{ padding: "20px", borderRadius: "17px", background: "#ffffff", border: "1px solid #e4e7ec" }}>
                  <span style={{ fontSize: "10px", fontWeight: "800", color: "#667085" }}>SALARY DATA</span>
                  <strong style={{ display: "block", marginTop: "8px", fontSize: "20px", color: "#101828" }}>
                    {marketResult.salary?.average_min_salary != null ? `₹${Number(marketResult.salary.average_min_salary).toLocaleString("en-IN")}` : "Not available"}
                  </strong>
                  <small style={{ color: "#667085" }}>Average minimum salary from available listings</small>
                </div>
              </div>

              <div style={{ display: "grid", gridTemplateColumns: "minmax(0, 1.5fr) minmax(280px, 1fr)", gap: "18px" }}>
                <div style={{ padding: "22px", borderRadius: "18px", background: "#ffffff", border: "1px solid #e4e7ec" }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: "12px", marginBottom: "18px" }}>
                    <div>
                      <div style={{ fontSize: "10px", fontWeight: "800", letterSpacing: "1.2px", color: "#6366f1" }}>DEMAND SIGNALS</div>
                      <h3 style={{ margin: "5px 0 0", fontSize: "21px" }}>Most Demanded Skills</h3>
                    </div>
                    <span style={{ padding: "7px 10px", borderRadius: "999px", background: "#f5f3ff", color: "#6366f1", fontSize: "10px", fontWeight: "800" }}>
                      {marketResult.top_skills?.length || 0} skills
                    </span>
                  </div>

                  {marketResult.top_skills?.length ? (
                    <div style={{ display: "grid", gap: "13px" }}>
                      {marketResult.top_skills.map((item, index) => (
                        <div key={`${item.skill}-${index}`}>
                          <div style={{ display: "flex", justifyContent: "space-between", gap: "12px", marginBottom: "6px" }}>
                            <span style={{ fontWeight: "750", fontSize: "13px" }}>{item.skill}</span>
                            <span style={{ fontWeight: "800", fontSize: "12px", color: "#6366f1" }}>{item.demand_percentage}%</span>
                          </div>
                          <div style={{ height: "8px", borderRadius: "999px", background: "#ececf4", overflow: "hidden" }}>
                            <div style={{ width: `${Math.min(Number(item.demand_percentage) || 0, 100)}%`, height: "100%", borderRadius: "999px", background: "linear-gradient(90deg, #6366f1, #8b5cf6)" }}></div>
                          </div>
                          <small style={{ color: "#98a2b3", fontSize: "10px" }}>Appears in {item.job_count} of {item.total_jobs} analyzed jobs</small>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div style={{ padding: "20px", borderRadius: "12px", background: "#fafafa", color: "#667085", fontSize: "13px" }}>
                      No market data was found for this role yet. Try a role that exists in the collected dataset.
                    </div>
                  )}
                </div>

                <div style={{ padding: "22px", borderRadius: "18px", background: "#ffffff", border: "1px solid #e4e7ec" }}>
                  <div style={{ fontSize: "10px", fontWeight: "800", letterSpacing: "1.2px", color: "#6366f1" }}>GEOGRAPHIC SIGNAL</div>
                  <h3 style={{ margin: "5px 0 17px", fontSize: "21px" }}>Top Job Locations</h3>
                  {marketResult.locations?.length ? (
                    <div style={{ display: "grid", gap: "10px" }}>
                      {marketResult.locations.slice(0, 6).map((item, index) => (
                        <div key={`${item.location}-${index}`} style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: "10px", padding: "11px 12px", borderRadius: "11px", background: "#fafbff", border: "1px solid #eef0f5" }}>
                          <span style={{ fontSize: "12px", fontWeight: "700" }}>📍 {item.location}</span>
                          <span style={{ fontSize: "11px", fontWeight: "800", color: "#6366f1" }}>{item.job_count}</span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p style={{ color: "#667085", fontSize: "13px" }}>No location data available.</p>
                  )}
                  <div style={{ marginTop: "18px", padding: "13px", borderRadius: "12px", background: "#f8f7ff", color: "#667085", fontSize: "10px", lineHeight: "1.6" }}>
                    💡 Market demand is calculated from the job postings currently stored in SkillForage's market database.
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </section>


      {/* =====================================================
          HOW IT WORKS
      ===================================================== */}

      <section
        className="how-section"
        id="how-it-works"
      >

        <div className="section-heading">

          <div className="eyebrow">
            HOW IT WORKS
          </div>

          <h2>
            From Resume to
            <span>
              Career Roadmap.
            </span>
          </h2>

          <p>
            SkillForge AI transforms your resume into
            actionable career intelligence in four simple steps.
          </p>

        </div>

        <div className="process-grid">

          <div className="process-card">

            <div className="process-number">
              01
            </div>

            <div className="process-icon">
              🎓
            </div>

            <h3>
              Understand You
            </h3>

            <p>
              Tell SkillForge your academic year,
              interests, career direction and available
              preparation time.
            </p>

          </div>

          <div className="process-card">

            <div className="process-number">
              02
            </div>

            <div className="process-icon">
              📄
            </div>

            <h3>
              Analyze Your Resume
            </h3>

            <p>
              Upload your resume and let SkillForge
              extract your skills and evaluate your ATS
              compatibility.
            </p>

          </div>

          <div className="process-card">

            <div className="process-number">
              03
            </div>

            <div className="process-icon">
              🎯
            </div>

            <h3>
              Find Skill Gaps
            </h3>

            <p>
              See exactly which skills you already have
              and which ones you need to develop.
            </p>

          </div>

          <div className="process-card">

            <div className="process-number">
              04
            </div>

            <div className="process-icon">
              🚀
            </div>

            <h3>
              Follow Your Roadmap
            </h3>

            <p>
              Receive a personalized career journey
              based on your profile, skills and academic stage.
            </p>

          </div>

        </div>

      </section>


      {/* =====================================================
          ANALYZER
      ===================================================== */}

      <main
        className="main-content"
        id="analyzer"
      >

        <div className="analyzer-heading">

          <div className="eyebrow">
            SKILLFORGE ANALYZER
          </div>

          <h2>
            Let's Build Your
            <span>
              Career Intelligence.
            </span>
          </h2>

          <p>
            Complete your academic profile and upload
            your resume. SkillForge will analyze your
            current skills and identify what you should
            learn next.
          </p>

        </div>


        {/* PROFILE REMINDER */}

        {!studentProfile && (

          <div
            style={{
              marginBottom:
                "20px",
              padding:
                "18px",
              borderRadius:
                "16px",
              background:
                "linear-gradient(135deg, #fafaff, #f5f3ff)",
              border:
                "1px solid #e8e5ff",
              display:
                "flex",
              alignItems:
                "center",
              justifyContent:
                "space-between",
              gap:
                "15px",
              flexWrap:
                "wrap",
            }}
          >

            <div>

              <strong
                style={{
                  display:
                    "block",
                  marginBottom:
                    "5px",
                }}
              >
                🎓 Personalize your journey first
              </strong>

              <span
                style={{
                  color:
                    "#667085",
                  fontSize:
                    "13px",
                }}
              >
                Tell SkillForge about your goals so
                your roadmap can adapt to you.
              </span>

            </div>

            <button
              type="button"
              onClick={
                openStudentProfile
              }
              style={{
                border:
                  "none",
                padding:
                  "11px 17px",
                borderRadius:
                  "10px",
                background:
                  "#6366f1",
                color:
                  "#ffffff",
                fontWeight:
                  "700",
                cursor:
                  "pointer",
              }}
            >
              Create Profile →
            </button>

          </div>

        )}


        {/* PROGRESS */}

        <div className="progress-card">

          <div className="progress-top">

            <div>

              <span>
                ANALYSIS PROGRESS
              </span>

              <strong>
                {progressText}
              </strong>

            </div>

            <div className="progress-percent">
              {progressPercent}%
            </div>

          </div>

          <div className="progress-track">

            <div
              className="progress-fill"
              style={{
                width:
                  `${progressPercent}%`,
              }}
            ></div>

          </div>

        </div>


        {/* STEP 1 — EDUCATION */}

        <div className="forge-card reveal">

          <div className="card-heading">

            <div className="card-step">
              01
            </div>

            <div>

              <span>
                EDUCATION
              </span>

              <h3>
                Choose Your Education
              </h3>

              <p>
                Your academic path determines your
                personalized roadmap.
              </p>

            </div>

          </div>

          <div className="education-grid">

            {Object.entries(
              educationOptions
            ).map(
              (
                [
                  key,
                  option,
                ]
              ) => (

                <button
                  key={key}
                  type="button"
                  className={
                    education ===
                    key
                      ? "education-card active"
                      : "education-card"
                  }
                  onClick={() =>
                    handleEducationChange(
                      key
                    )
                  }
                >

                  <div className="education-top">

                    <div className="education-icon">

                      {key ===
                      "Engineering"
                        ? "💻"
                        : key ===
                          "Postgraduate"
                        ? "🎓"
                        : "🔬"}

                    </div>

                    <div className="selection-check">

                      {education ===
                      key
                        ? "✓"
                        : ""}

                    </div>

                  </div>

                  <strong>
                    {key}
                  </strong>

                  <span className="education-short">
                    {option.short}
                  </span>

                  <p>
                    {option.description}
                  </p>

                  <div className="education-footer">

                    <span>
                      Duration
                    </span>

                    <span>
                      {option.duration}
                    </span>

                  </div>

                </button>

              )
            )}

          </div>

        </div>


        {/* STEP 2 — YEAR */}

        {education && (

          <div className="forge-card reveal">

            <div className="card-heading">

              <div className="card-step">
                02
              </div>

              <div>

                <span>
                  ACADEMIC YEAR
                </span>

                <h3>
                  Where Are You Now?
                </h3>

                <p>
                  Choose your current academic year
                  to personalize your roadmap.
                </p>

              </div>

            </div>

            <div className="year-grid">

              {educationOptions[
                education
              ].years.map(
                (
                  item,
                  index
                ) => (

                  <button
                    key={item}
                    type="button"
                    className={
                      year ===
                      item
                        ? "year-btn active"
                        : "year-btn"
                    }
                    onClick={() => {

                      setYear(
                        item
                      );

                      setBranch(
                        ""
                      );

                      setResult(
                        null
                      );

                      setError(
                        ""
                      );

                    }}
                  >

                    <span className="year-icon">

                      {index ===
                      0
                        ? "🌱"
                        : index ===
                          1
                        ? "⚙️"
                        : index ===
                          2
                        ? "🚀"
                        : "🎯"}

                    </span>

                    <span className="year-number">
                      YEAR {index + 1}
                    </span>

                    <span className="year-title">
                      {item}
                    </span>

                    <small>
                      Personalized roadmap
                    </small>

                  </button>

                )
              )}

            </div>

          </div>

        )}


        {/* STEP 3 — BRANCH */}

        {education &&
          year && (

            <div className="forge-card reveal">

              <div className="card-heading">

                <div className="card-step">
                  03
                </div>

                <div>

                  <span>
                    SPECIALIZATION
                  </span>

                  <h3>
                    Choose Your Branch
                  </h3>

                  <p>
                    Select your course or specialization.
                  </p>

                </div>

              </div>

              <div className="select-wrapper">

                <div className="select-icon">
                  🎓
                </div>

                <select
                  value={branch}
                  onChange={(
                    event
                  ) => {

                    setBranch(
                      event.target
                        .value
                    );

                    setResult(
                      null
                    );

                    setError(
                      ""
                    );

                  }}
                >

                  <option value="">
                    Select your branch / course
                  </option>

                  {educationOptions[
                    education
                  ].branches.map(
                    (
                      item
                    ) => (

                      <option
                        key={item}
                        value={item}
                      >
                        {item}
                      </option>

                    )
                  )}

                </select>

                <div className="select-arrow">
                  ▼
                </div>

              </div>

            </div>

          )}


        {/* STEP 4 — RESUME */}

        {education &&
          year &&
          branch && (

            <div className="forge-card reveal">

              <div className="card-heading">

                <div className="card-step">
                  04
                </div>

                <div>

                  <span>
                    RESUME
                  </span>

                  <h3>
                    Upload Your Resume
                  </h3>

                  <p>
                    Our AI will extract your technical
                    skills automatically.
                  </p>

                </div>

              </div>


              {!file ? (

                <label
                  className={
                    dragActive
                      ? "upload-zone drag-active"
                      : "upload-zone"
                  }
                  onDragOver={
                    handleDragOver
                  }
                  onDragLeave={
                    handleDragLeave
                  }
                  onDrop={
                    handleDrop
                  }
                >

                  <input
                    type="file"
                    accept=".pdf,.doc,.docx"
                    onChange={
                      handleInputFile
                    }
                    hidden
                  />

                  <div className="upload-icon">
                    ☁
                  </div>

                  <h3>
                    Drop your resume here
                  </h3>

                  <p>
                    or choose a file from your computer
                  </p>

                  <span className="browse-btn">
                    Browse Files
                  </span>

                  <div className="upload-meta">

                    <span>
                      ✓ PDF / DOC / DOCX
                    </span>

                    <span>
                      ✓ Maximum 5 MB
                    </span>

                    <span>
                      ✓ Secure processing
                    </span>

                  </div>

                </label>

              ) : (

                <div className="file-success">

                  <div className="file-icon">
                    PDF
                  </div>

                  <div className="file-details">

                    <strong>
                      {file.name}
                    </strong>

                    <span>
                      ✓ Resume ready for AI analysis
                    </span>

                  </div>

                  <button
                    type="button"
                    className="remove-file"
                    onClick={() => {

                      setFile(
                        null
                      );

                      setResumeSkills(
                        []
                      );

                      setResult(
                        null
                      );

                      setError(
                        ""
                      );

                    }}
                  >
                    Remove
                  </button>

                </div>

              )}


              {/* ERROR */}

              {error && (

                <div
                  style={{
                    marginTop:
                      "15px",
                    padding:
                      "12px 15px",
                    borderRadius:
                      "10px",
                    background:
                      "#fff5f5",
                    border:
                      "1px solid #fecaca",
                    color:
                      "#dc2626",
                    fontSize:
                      "12px",
                    fontWeight:
                      "600",
                  }}
                >
                  ⚠️ {error}
                </div>

              )}


              {/* ANALYZE BUTTON */}

              <button
                type="button"
                className="analyze-btn"
                onClick={
                  analyzeSkillGap
                }
                disabled={
                  loading
                }
              >

                {loading ? (

                  <>

                    <span className="spinner"></span>

                    <span>
                      Analyzing Resume...
                    </span>

                  </>

                ) : (

                  <>

                    <span>
                      ✨
                    </span>

                    <span>
                      Analyze My Skill Gap
                    </span>

                    <span>
                      →
                    </span>

                  </>

                )}

              </button>


              {/* LOADING */}

              {loading && (

                <div className="analysis-loading">

                  <div className="loading-pulse"></div>

                  <div>

                    <strong>
                      AI is analyzing your resume...
                    </strong>

                    <span>
                      Extracting skills, calculating ATS
                      compatibility and identifying your
                      skill gaps.
                    </span>

                  </div>

                </div>

              )}


              {/* DETECTED SKILLS */}

              {resumeSkills.length >
                0 && (

                  <div
                    style={{
                      marginTop:
                        "20px",
                      padding:
                        "18px",
                      border:
                        "1px solid #e4e7ec",
                      borderRadius:
                        "13px",
                      background:
                        "#fafbff",
                    }}
                  >

                    <div
                      style={{
                        fontSize:
                          "10px",
                        fontWeight:
                          "800",
                        color:
                          "#6366f1",
                        letterSpacing:
                          "1px",
                        marginBottom:
                          "12px",
                      }}
                    >
                      ✓ SKILLS DETECTED FROM YOUR RESUME
                    </div>

                    <div
                      style={{
                        display:
                          "flex",
                        flexWrap:
                          "wrap",
                        gap:
                          "7px",
                      }}
                    >

                      {resumeSkills.map(
                        (
                          skill,
                          index
                        ) => (

                          <span
                            key={`${skill}-${index}`}
                            style={{
                              padding:
                                "7px 10px",
                              borderRadius:
                                "999px",
                              background:
                                "#ede9fe",
                              color:
                                "#5b21b6",
                              fontSize:
                                "10px",
                              fontWeight:
                                "700",
                            }}
                          >
                            {skill}
                          </span>

                        )
                      )}

                    </div>

                  </div>

                )}

            </div>

          )}


        {/* =====================================================
            RESULTS
        ===================================================== */}

        {result && (

          <section
            className="results-section reveal"
            id="results"
          >

            <div className="result-header">

              <div>

                <div className="eyebrow">
                  AI ANALYSIS COMPLETE
                </div>

                <h2>
                  Your Skill Gap
                  <span>
                    Report.
                  </span>
                </h2>

                <p>
                  {education} · {year} · {branch}
                </p>

              </div>

              <div className="success-badge">

                <span>
                  ✓
                </span>

                Analysis Complete

              </div>

            </div>


            {/* TARGET ROLE */}

            {targetRole && (

              <div
                style={{
                  marginBottom:
                    "22px",
                  padding:
                    "20px",
                  borderRadius:
                    "18px",
                  background:
                    "linear-gradient(135deg, #f5f3ff, #fafaff)",
                  border:
                    "1px solid #e8e5ff",
                }}
              >

                <div
                  style={{
                    fontSize:
                      "10px",
                    fontWeight:
                      "800",
                    letterSpacing:
                      "1.5px",
                    color:
                      "#6366f1",
                    marginBottom:
                      "8px",
                  }}
                >
                  TARGET CAREER
                </div>

                <h3
                  style={{
                    margin:
                      "0 0 8px",
                    fontSize:
                      "22px",
                  }}
                >
                  {targetRole.icon}{" "}
                  {targetRole.title}
                </h3>

                <p
                  style={{
                    margin:
                      "0",
                    color:
                      "#667085",
                    fontSize:
                      "13px",
                  }}
                >
                  {targetRole.description}
                </p>

              </div>

            )}


            {/* PROFILE INTELLIGENCE */}

            {studentProfile && (

              <div
                style={{
                  marginBottom:
                    "22px",
                  padding:
                    "20px",
                  borderRadius:
                    "18px",
                  background:
                    "linear-gradient(135deg, #fafaff, #f5f3ff)",
                  border:
                    "1px solid #e8e5ff",
                }}
              >

                <div
                  style={{
                    fontSize:
                      "10px",
                    fontWeight:
                      "800",
                    letterSpacing:
                      "1.5px",
                    color:
                      "#6366f1",
                    marginBottom:
                      "8px",
                  }}
                >
                  PERSONALIZATION CONTEXT
                </div>

                <h3
                  style={{
                    margin:
                      "0 0 8px",
                    fontSize:
                      "20px",
                  }}
                >
                  Your roadmap is built around you.
                </h3>

                <div
                  style={{
                    display:
                      "flex",
                    flexWrap:
                      "wrap",
                    gap:
                      "8px",
                  }}
                >

                  <span
                    style={{
                      padding:
                        "8px 11px",
                      borderRadius:
                        "999px",
                      background:
                        "#ffffff",
                      border:
                        "1px solid #e4e7ec",
                      fontSize:
                        "11px",
                      fontWeight:
                        "700",
                    }}
                  >
                    🎓 {studentProfile.year}
                  </span>

                  <span
                    style={{
                      padding:
                        "8px 11px",
                      borderRadius:
                        "999px",
                      background:
                        "#ffffff",
                      border:
                        "1px solid #e4e7ec",
                      fontSize:
                        "11px",
                      fontWeight:
                        "700",
                    }}
                  >
                    🧭 {studentProfile.careerStatus}
                  </span>

                  <span
                    style={{
                      padding:
                        "8px 11px",
                      borderRadius:
                        "999px",
                      background:
                        "#ffffff",
                      border:
                        "1px solid #e4e7ec",
                      fontSize:
                        "11px",
                      fontWeight:
                        "700",
                    }}
                  >
                    ⏱️ {studentProfile.timeAvailable}
                  </span>

                </div>

              </div>

            )}


            {/* RESULT DASHBOARD */}

            <div className="result-dashboard">

              {/* ATS */}

              <div className="result-stat-card ats-card">

                <div className="stat-icon purple">
                  🤖
                </div>

                <span>
                  ATS SCORE
                </span>

                <strong>
                  {atsScore}%
                </strong>

                <small>
                  Resume compatibility score
                </small>

              </div>


              {/* SKILL MATCH */}

              <div className="score-card">

                <span className="score-label">
                  OVERALL SKILL MATCH
                </span>

                <div className="score-circle">

                  <svg
                    className="score-svg"
                    viewBox="0 0 120 120"
                  >

                    <circle
                      className="score-bg"
                      cx="60"
                      cy="60"
                      r="50"
                    />

                    <circle
                      className="score-progress"
                      cx="60"
                      cy="60"
                      r="50"
                      strokeDasharray="314"
                      strokeDashoffset={
                        314 -
                        (314 *
                          skillGapScore) /
                          100
                      }
                    />

                  </svg>

                  <div className="score-value">

                    <strong>
                      {skillGapScore}%
                    </strong>

                  </div>

                </div>

                <strong className="score-title">
                  Career Readiness
                </strong>

                <p>
                  Your current skill match based
                  on the selected career path.
                </p>

              </div>


              {/* MATCHED */}

              <div className="result-stat-card">

                <div className="stat-icon green">
                  ✓
                </div>

                <span>
                  MATCHED SKILLS
                </span>

                <strong>
                  {matchedSkills.length}
                </strong>

                <small>
                  Skills you already demonstrate
                </small>

              </div>


              {/* MISSING */}

              <div className="result-stat-card">

                <div className="stat-icon red">
                  +
                </div>

                <span>
                  SKILLS TO LEARN
                </span>

                <strong>
                  {missingSkills.length}
                </strong>

                <small>
                  Skills recommended for you
                </small>

              </div>


              {/* ROADMAP */}

              <div className="result-stat-card">

                <div className="stat-icon purple">
                  🚀
                </div>

                <span>
                  ROADMAP
                </span>

                <strong>
                  {roadmap.length}
                </strong>

                <small>
                  Personalized priority areas
                </small>

              </div>

            </div>


            {/* ATS DETAILS */}

            <div
              style={{
                marginTop:
                  "22px",
                padding:
                  "22px",
                borderRadius:
                  "18px",
                background:
                  "linear-gradient(135deg, #fafaff, #f5f3ff)",
                border:
                  "1px solid #e8e5ff",
              }}
            >

              <div
                style={{
                  display:
                    "flex",
                  justifyContent:
                    "space-between",
                  alignItems:
                    "center",
                  gap:
                    "20px",
                  flexWrap:
                    "wrap",
                }}
              >

                <div>

                  <div
                    style={{
                      fontSize:
                        "10px",
                      fontWeight:
                        "800",
                      letterSpacing:
                        "1.5px",
                      color:
                        "#6366f1",
                      marginBottom:
                        "6px",
                    }}
                  >
                    RESUME INTELLIGENCE
                  </div>

                  <h3
                    style={{
                      margin:
                        "0 0 6px",
                      fontSize:
                        "22px",
                    }}
                  >
                    ATS Compatibility
                  </h3>

                  <p
                    style={{
                      margin:
                        0,
                      color:
                        "#667085",
                      fontSize:
                        "13px",
                    }}
                  >
                    How well your resume matches
                    common technical ATS keywords.
                  </p>

                </div>

                <div
                  style={{
                    minWidth:
                      "120px",
                    textAlign:
                      "center",
                    padding:
                      "15px 22px",
                    borderRadius:
                      "16px",
                    background:
                      "#ffffff",
                    border:
                      "1px solid #e4e7ec",
                  }}
                >

                  <div
                    style={{
                      fontSize:
                        "34px",
                      fontWeight:
                        "900",
                      color:
                        atsScore >=
                        75
                          ? "#16a34a"
                          : atsScore >=
                            50
                          ? "#d97706"
                          : "#dc2626",
                    }}
                  >
                    {atsScore}%
                  </div>

                  <div
                    style={{
                      fontSize:
                        "9px",
                      fontWeight:
                        "800",
                      letterSpacing:
                        "1px",
                      color:
                        "#667085",
                    }}
                  >
                    ATS SCORE
                  </div>

                </div>

              </div>


              <div
                style={{
                  marginTop:
                    "20px",
                  height:
                    "9px",
                  background:
                    "#e9e7f7",
                  borderRadius:
                    "99px",
                  overflow:
                    "hidden",
                }}
              >

                <div
                  style={{
                    width: `${Math.min(
                      Math.max(
                        atsScore,
                        0
                      ),
                      100
                    )}%`,
                    height:
                      "100%",
                    borderRadius:
                      "99px",
                    background:
                      "linear-gradient(90deg, #6366f1, #8b5cf6)",
                    transition:
                      "width 0.8s ease",
                  }}
                ></div>

              </div>


              {result?.ats_analysis && (

                <div
                  style={{
                    marginTop:
                      "18px",
                    display:
                      "grid",
                    gridTemplateColumns:
                      "repeat(auto-fit, minmax(220px, 1fr))",
                    gap:
                      "15px",
                  }}
                >

                  <div
                    style={{
                      padding:
                        "15px",
                      background:
                        "#ffffff",
                      borderRadius:
                        "13px",
                      border:
                        "1px solid #e4e7ec",
                    }}
                  >

                    <span
                      style={{
                        display:
                          "block",
                        fontSize:
                          "9px",
                        fontWeight:
                          "800",
                        color:
                          "#16a34a",
                        letterSpacing:
                          "1px",
                        marginBottom:
                          "8px",
                      }}
                    >
                      FOUND KEYWORDS
                    </span>

                    <strong
                      style={{
                        fontSize:
                          "22px",
                      }}
                    >
                      {result
                        .ats_analysis
                        .keyword_match_count ??
                        result
                          .ats_analysis
                          .found_keywords
                          ?.length ??
                        0}
                    </strong>

                  </div>


                  <div
                    style={{
                      padding:
                        "15px",
                      background:
                        "#ffffff",
                      borderRadius:
                        "13px",
                      border:
                        "1px solid #e4e7ec",
                    }}
                  >

                    <span
                      style={{
                        display:
                          "block",
                        fontSize:
                          "9px",
                        fontWeight:
                          "800",
                        color:
                          "#dc2626",
                        letterSpacing:
                          "1px",
                        marginBottom:
                          "8px",
                      }}
                    >
                      MISSING KEYWORDS
                    </span>

                    <strong
                      style={{
                        fontSize:
                          "22px",
                      }}
                    >
                      {result
                        .ats_analysis
                        .missing_keywords
                        ?.length ??
                        0}
                    </strong>

                  </div>

                </div>

              )}

            </div>


            {/* =================================================
                SKILLS
            ================================================= */}

            <div className="skills-dashboard">

              <div className="skill-column">

                <div className="skill-column-header">

                  <div>

                    <div className="column-label green-label">
                      YOU HAVE
                    </div>

                    <h3>
                      Matched Skills
                    </h3>

                  </div>

                  <div className="count-badge green-badge">
                    {matchedSkills.length}
                  </div>

                </div>


                {matchedSkills.length >
                0 ? (

                  matchedSkills.map(
                    (
                      skill,
                      index
                    ) => (

                      <div
                        className="skill-row matched-row"
                        key={`${skill}-${index}`}
                      >

                        <div className="skill-check">
                          ✓
                        </div>

                        <strong>
                          {skill}
                        </strong>

                        <span className="skill-status">
                          MATCHED
                        </span>

                      </div>

                    )
                  )

                ) : (

                  <div className="empty-state">
                    No matched skills returned.
                  </div>

                )}

              </div>


              <div className="skill-column">

                <div className="skill-column-header">

                  <div>

                    <div className="column-label red-label">
                      FOCUS AREA
                    </div>

                    <h3>
                      Skills to Learn
                    </h3>

                  </div>

                  <div className="count-badge red-badge">
                    {missingSkills.length}
                  </div>

                </div>


                {missingSkills.length >
                0 ? (

                  missingSkills.map(
                    (
                      skill,
                      index
                    ) => (

                      <div
                        className="skill-row missing-row"
                        key={`${skill}-${index}`}
                      >

                        <div className="skill-plus">
                          +
                        </div>

                        <strong>
                          {skill}
                        </strong>

                        <span className="skill-status">
                          PRIORITY
                        </span>

                      </div>

                    )
                  )

                ) : (

                  <div className="empty-state">
                    Great! No major skill gaps detected.
                  </div>

                )}

              </div>

            </div>


            {/* =================================================
                PERSONALIZED ROADMAP
            ================================================= */}

            <div
              className="roadmap-section"
              id="roadmap"
            >

              <div className="roadmap-header">

                <div>

                  <div className="eyebrow">
                    PERSONALIZED ROADMAP
                  </div>

                  <h3>
                    Your{" "}
                    {studentProfile?.year ||
                      year}{" "}
                    Career Journey
                  </h3>

                  <p>
                    {education} ·{" "}
                    {branch}
                  </p>

                </div>

                <div className="roadmap-badge">
                  PERSONALIZED PATH
                </div>

              </div>


              {/* ROADMAP CONTEXT */}

              {studentProfile && (

                <div
                  style={{
                    marginBottom:
                      "25px",
                    padding:
                      "15px 18px",
                    borderRadius:
                      "14px",
                    background:
                      "#fafaff",
                    border:
                      "1px solid #e4e7ec",
                    display:
                      "flex",
                    flexWrap:
                      "wrap",
                    gap:
                      "8px",
                  }}
                >

                  <span
                    style={{
                      fontSize:
                        "11px",
                      fontWeight:
                        "700",
                      color:
                        "#475467",
                    }}
                  >
                    🧠 Personalized using:
                  </span>

                  <span>
                    {studentProfile.year}
                  </span>

                  <span>
                    •
                  </span>

                  <span>
                    {studentProfile.careerStatus}
                  </span>

                  <span>
                    •
                  </span>

                  <span>
                    {studentProfile.timeAvailable}
                  </span>

                  {targetRole && (
                    <>
                      <span>
                        •
                      </span>

                      <span>
                        🎯 {targetRole.title}
                      </span>
                    </>
                  )}

                </div>

              )}


              <div className="timeline">

                {roadmap.map(
                  (
                    item,
                    index
                  ) => (

                    <div
                      className="timeline-item"
                      key={`${item.title}-${index}`}
                    >

                      <div className="timeline-line"></div>

                      <div className="timeline-number">

                        {String(
                          index + 1
                        ).padStart(
                          2,
                          "0"
                        )}

                      </div>

                      <div className="timeline-content">

                        <div>

                          <div className="timeline-priority">
                            {item.priority}
                          </div>

                          <h4>
                            {item.title}
                          </h4>

                          <p>
                            {item.description}
                          </p>

                        </div>

                        <div className="timeline-action">

                          <span>
                            NEXT STEP
                          </span>

                          <button
                            type="button"
                          >
                            Learn →
                          </button>

                        </div>

                      </div>

                    </div>

                  )
                )}

              </div>

            </div>


            {/* NEW ANALYSIS */}

            <button
              type="button"
              className="new-analysis-btn"
              onClick={
                resetAnalysis
              }
            >
              ← Start a New Analysis
            </button>

          </section>

        )}

      </main>


      {/* =====================================================
          FOOTER
      ===================================================== */}

      <footer className="footer">

        <div className="footer-inner">

          <div className="footer-brand">

            <div className="brand">

              <div className="brand-icon">
                ⚡
              </div>

              <div>

                <span className="brand-name">
                  SkillForge
                </span>

                <span className="brand-ai">
                  AI
                </span>

              </div>

            </div>

            <p>
              Forge your skills. Shape your future.
            </p>

          </div>

          <div className="footer-copy">
            © 2026 SkillForge AI · Built for the next generation.
          </div>

        </div>

      </footer>

    </div>
  );
}

export default App;