const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000/api/v1";

function formatError(data, status) {
  if (typeof data?.detail === "string") return data.detail;
  if (Array.isArray(data?.detail)) {
    return data.detail.map((d) => d.msg || JSON.stringify(d)).join("; ");
  }
  return data?.message || `Request failed with status ${status}`;
}

async function request(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;

  const headers = {
    ...options.headers,
  };

  if (!(options.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
  }

  const config = {
    ...options,
    headers,
    credentials: "include", // Sends and receives httpOnly sf_session cookie
  };

  try {
    const response = await fetch(url, config);

    // Handle 204 No Content
    if (response.status === 204) {
      return null;
    }

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      const errorMsg = formatError(data, response.status);
      const error = new Error(errorMsg);
      error.status = response.status;
      error.data = data;
      throw error;
    }

    return data;
  } catch (err) {
    if (err.status) throw err;
    const networkError = new Error("Unable to connect to SkillForage API server. Ensure backend is running on port 8000.");
    networkError.status = 0;
    throw networkError;
  }
}

export const api = {
  // Auth
  auth: {
    register: (body) => request("/auth/register", { method: "POST", body: JSON.stringify(body) }),
    verifyOtp: (body) => request("/auth/verify-otp", { method: "POST", body: JSON.stringify(body) }),
    resendOtp: (body) => request("/auth/resend-otp", { method: "POST", body: JSON.stringify(body) }),
    login: (body) => request("/auth/login", { method: "POST", body: JSON.stringify(body) }),
    logout: () => request("/auth/logout", { method: "POST" }),
    me: () => request("/auth/me", { method: "GET" }),
  },

  // Profile & Settings
  profile: {
    get: () => request("/profile", { method: "GET" }),
    update: (body) => request("/profile", { method: "PUT", body: JSON.stringify(body) }),
    changePassword: (body) => request("/profile/change-password", { method: "POST", body: JSON.stringify(body) }),
    exportData: () => request("/profile/export-data", { method: "GET" }),
    deleteAccount: (body) => request("/profile/delete-account", { method: "DELETE", body: JSON.stringify(body) }),
  },

  // Careers
  careers: {
    list: () => request("/careers", { method: "GET" }),
    get: (id) => request(`/careers/${id}`, { method: "GET" }),
    match: (body) => request("/careers/match", { method: "POST", body: JSON.stringify(body) }),
    compare: (body) => request("/careers/compare", { method: "POST", body: JSON.stringify(body) }),
    setTarget: (body) => request("/careers/set-target", { method: "POST", body: JSON.stringify(body) }),
  },

  // Assessments
  assessments: {
    getCategories: () => request("/assessments/categories", { method: "GET" }),
    start: (category, difficulty) => request(`/assessments/start?category=${encodeURIComponent(category)}&difficulty=${encodeURIComponent(difficulty)}`, { method: "GET" }),
    submit: (body) => request("/assessments/submit", { method: "POST", body: JSON.stringify(body) }),
    history: (params = "") => request(`/assessments/history${params ? `?${params}` : ""}`, { method: "GET" }),
    getDetail: (id) => request(`/assessments/history/${id}`, { method: "GET" }),
  },

  // Skills & Verification
  skills: {
    taxonomy: () => request("/skills/taxonomy", { method: "GET" }),
    verified: () => request("/skills/verified", { method: "GET" }),
    selfReport: (body) => request("/skills/self-report", { method: "POST", body: JSON.stringify(body) }),
  },

  // Market Intelligence & Skill Gap
  market: {
    analytics: (origin = "synthetic_demo", role = "") => {
      let q = `?data_origin=${encodeURIComponent(origin)}`;
      if (role) q += `&role=${encodeURIComponent(role)}`;
      return request(`/market/analytics${q}`, { method: "GET" });
    },
    skillGap: (roleId = "") => request(`/market/skill-gap${roleId ? `?role_id=${encodeURIComponent(roleId)}` : ""}`, { method: "GET" }),
    importFile: (formData) => request("/market/import", { method: "POST", body: formData }),
    status: () => request("/market/status", { method: "GET" }),
  },

  // Roadmaps
  roadmaps: {
    getCurrent: () => request("/roadmaps/current", { method: "GET" }),
    generate: (body) => request("/roadmaps/generate", { method: "POST", body: JSON.stringify(body) }),
    completeTask: (body) => request("/roadmaps/complete-task", { method: "POST", body: JSON.stringify(body) }),
    reschedule: (body) => request("/roadmaps/reschedule", { method: "POST", body: JSON.stringify(body) }),
  },

  // Learning Hub
  learning: {
    list: (category = "", difficulty = "", bookmarked = false) => {
      const p = new URLSearchParams();
      if (category) p.append("category", category);
      if (difficulty) p.append("difficulty", difficulty);
      if (bookmarked) p.append("bookmarked_only", "true");
      return request(`/learning/lessons?${p.toString()}`, { method: "GET" });
    },
    get: (id) => request(`/learning/lessons/${id}`, { method: "GET" }),
    submitQuiz: (id, body) => request(`/learning/lessons/${id}/submit-quiz`, { method: "POST", body: JSON.stringify(body) }),
    toggleBookmark: (id, body) => request(`/learning/lessons/${id}/bookmark`, { method: "POST", body: JSON.stringify(body) }),
  },

  // Projects
  projects: {
    templates: (role = "", difficulty = "", year = "") => {
      const p = new URLSearchParams();
      if (role) p.append("role", role);
      if (difficulty) p.append("difficulty", difficulty);
      if (year) p.append("year", year);
      return request(`/projects/templates?${p.toString()}`, { method: "GET" });
    },
    myProjects: () => request("/projects/my", { method: "GET" }),
    create: (body) => request("/projects/my", { method: "POST", body: JSON.stringify(body) }),
    update: (id, body) => request(`/projects/my/${id}`, { method: "PUT", body: JSON.stringify(body) }),
    delete: (id) => request(`/projects/my/${id}`, { method: "DELETE" }),
  },

  // Challenges & Rewards
  challenges: {
    list: (type = "") => request(`/challenges${type ? `?challenge_type=${encodeURIComponent(type)}` : ""}`, { method: "GET" }),
    submit: (id, body) => request(`/challenges/${id}/submit`, { method: "POST", body: JSON.stringify(body) }),
  },
  rewards: {
    getProfile: () => request("/rewards/profile", { method: "GET" }),
  },

  // Interviews
  interviews: {
    start: (body) => request("/interviews/start", { method: "POST", body: JSON.stringify(body) }),
    submit: (body) => request("/interviews/submit", { method: "POST", body: JSON.stringify(body) }),
    history: () => request("/interviews/history", { method: "GET" }),
    getDetail: (id) => request(`/interviews/history/${id}`, { method: "GET" }),
  },

  // Resumes
  resumes: {
    upload: (formData) => request("/resumes/upload", { method: "POST", body: formData }),
    getProfile: () => request("/resumes/profile", { method: "GET" }),
    updateProfile: (body) => request("/resumes/profile", { method: "PUT", body: JSON.stringify(body) }),
    compareJob: (body) => request("/resumes/compare-job", { method: "POST", body: JSON.stringify(body) }),
    exportHtmlUrl: `${API_BASE}/resumes/export-html`,
    delete: () => request("/resumes/profile", { method: "DELETE" }),
  },

  // P2: What-If, Sprint, Hackathons, Dashboard
  whatIf: {
    simulate: (body) => request("/what-if/simulate", { method: "POST", body: JSON.stringify(body) }),
  },
  sprint: {
    plan: (body) => request("/sprint/plan", { method: "POST", body: JSON.stringify(body) }),
  },
  hackathons: {
    list: (mode = "", search = "") => {
      const p = new URLSearchParams();
      if (mode) p.append("mode", mode);
      if (search) p.append("search", search);
      return request(`/hackathons?${p.toString()}`, { method: "GET" });
    },
    getPopup: () => request("/hackathons/popup", { method: "GET" }),
  },
  dashboard: {
    getStats: () => request("/dashboard", { method: "GET" }),
  },
};
