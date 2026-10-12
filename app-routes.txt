import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { AppLayout } from "./components/AppLayout";
import { ProtectedRoute } from "./components/ProtectedRoute";
import Landing from "./pages/Landing/Landing";
import Login from "./pages/Auth/Login";
import Register from "./pages/Auth/Register";
import VerifyOTP from "./pages/Auth/VerifyOTP";
import Dashboard from "./pages/Dashboard/Dashboard";
import CareerDiscovery from "./pages/Career/CareerDiscovery";
import SkillAssessment from "./pages/Skills/SkillAssessment";
import AssessmentHistory from "./pages/Skills/AssessmentHistory";
import SkillVerification from "./pages/Skills/SkillVerification";
import MarketIntelligence from "./pages/Market/MarketIntelligence";
import Roadmap from "./pages/Roadmap/Roadmap";
import LearningHub from "./pages/Learning/LearningHub";
import LessonDetail from "./pages/Learning/LessonDetail";
import Projects from "./pages/Projects/Projects";
import Challenges from "./pages/Challenges/Challenges";
import Rewards from "./pages/Rewards/Rewards";
import InterviewHub from "./pages/Interviews/InterviewHub";
import ResumeAnalyzer from "./pages/Resume/ResumeAnalyzer";
import ProfileSettings from "./pages/Profile/ProfileSettings";
import WhatIf from "./pages/WhatIf/WhatIf";
import EmergencySprint from "./pages/Sprint/EmergencySprint";
import Hackathons from "./pages/Hackathons/Hackathons";

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/verify-otp" element={<VerifyOTP />} />

          <Route element={<ProtectedRoute />}>
            <Route element={<AppLayout />}>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/careers" element={<CareerDiscovery />} />
              <Route path="/career" element={<Navigate to="/careers" replace />} />
              <Route path="/assessments" element={<SkillAssessment />} />
              <Route path="/skills" element={<SkillVerification />} />
              <Route path="/assessment-history" element={<AssessmentHistory />} />
              <Route path="/market" element={<MarketIntelligence />} />
              <Route path="/roadmap" element={<Roadmap />} />
              <Route path="/learning" element={<LearningHub />} />
              <Route path="/learning/:id" element={<LessonDetail />} />
              <Route path="/projects" element={<Projects />} />
              <Route path="/challenges" element={<Challenges />} />
              <Route path="/rewards" element={<Rewards />} />
              <Route path="/interviews" element={<InterviewHub />} />
              <Route path="/resume" element={<ResumeAnalyzer />} />
              <Route path="/settings" element={<ProfileSettings />} />
              <Route path="/profile" element={<Navigate to="/settings" replace />} />
              <Route path="/what-if" element={<WhatIf />} />
              <Route path="/sprint" element={<EmergencySprint />} />
              <Route path="/hackathons" element={<Hackathons />} />
            </Route>
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
