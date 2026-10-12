import { useEffect, useState } from "react";
import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { api } from "../../api/client";
import { ErrorMessage, LoadingState, PageHeader, ProgressBar, StatCard } from "../../components/CommonComponents";

export default function Rewards() {
  const [profile, setProfile] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api.rewards.getProfile().then(setProfile).catch((e) => setError(e.message));
  }, []);

  if (!profile && !error) return <LoadingState />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div>
      <PageHeader title="Streaks and rewards" subtitle="Streaks use DailyActivity in your timezone. A missed day never erases history. No gambling mechanics." breadcrumbs="Practice / Rewards" />
      <div className="grid-4">
        <StatCard title="XP" value={profile.total_xp} />
        <StatCard title="Level" value={profile.current_level} subtext={profile.level_title} />
        <StatCard title="Current streak" value={`${profile.current_streak_days} days`} />
        <StatCard title="Longest streak" value={`${profile.longest_streak_days} days`} />
      </div>
      <div className="card" style={{ padding: 16, marginTop: 16 }}>
        <p>Next milestone: {profile.next_milestone}</p>
        <ProgressBar percentage={profile.level_progress_percentage} />
      </div>
      <div className="card" style={{ padding: 16, height: 240, marginTop: 16 }}>
        <h3 className="card-title">Weekly activity</h3>
        <ResponsiveContainer>
          <BarChart data={profile.weekly_activity || []}>
            <XAxis dataKey="day" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="xp" fill="#6366f1" />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <h3 style={{ marginTop: 16 }}>Recent badges</h3>
      {(profile.recent_badges || []).length === 0 && <p style={{ fontSize: 14, color: "var(--neutral-500)" }}>No badges yet.</p>}
      {(profile.recent_badges || []).map((b) => (
        <div key={b.id} className="badge badge-primary" style={{ margin: 4 }}>{b.name}</div>
      ))}
    </div>
  );
}
