import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { api } from "../../api/client";
import { ErrorMessage, LoadingState, PageHeader } from "../../components/CommonComponents";

export default function LessonDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [lesson, setLesson] = useState(null);
  const [answer, setAnswer] = useState("");
  const [quizResult, setQuizResult] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api.learning.get(id).then(setLesson).catch((e) => setError(e.message));
  }, [id]);

  if (!lesson && !error) return <LoadingState />;
  if (error) return <ErrorMessage message={error} onRetry={() => navigate("/learning")} />;

  const quiz = lesson.quiz || {};

  async function submitQuiz(e) {
    e.preventDefault();
    const data = await api.learning.submitQuiz(id, { selected_answer: answer, time_spent_minutes: Math.max(1, lesson.estimated_minutes) });
    setQuizResult(data);
    const refreshed = await api.learning.get(id);
    setLesson(refreshed);
  }

  async function bookmark() {
    await api.learning.toggleBookmark(id, { is_bookmarked: !lesson.is_bookmarked });
    setLesson({ ...lesson, is_bookmarked: !lesson.is_bookmarked });
  }

  return (
    <div>
      <PageHeader title={lesson.title} subtitle={`${lesson.skill_category} · ${lesson.difficulty} · opening this page does not complete it`} />
      <button className="btn btn-secondary btn-sm" onClick={bookmark}>{lesson.is_bookmarked ? "Bookmarked" : "Bookmark"}</button>
      <div className="card" style={{ padding: 20, marginTop: 16, whiteSpace: "pre-wrap", fontSize: 14, lineHeight: 1.6 }}>
        {lesson.content_markdown}
      </div>
      <div className="card" style={{ padding: 16, marginTop: 16 }}>
        <h3>Required quiz</h3>
        <p>{quiz.question}</p>
        {(quiz.options || []).map((opt) => (
          <label key={opt} style={{ display: "block", marginTop: 6 }}>
            <input type="radio" name="quiz" checked={answer === opt} onChange={() => setAnswer(opt)} /> {opt}
          </label>
        ))}
        <button className="btn btn-primary" style={{ marginTop: 12 }} onClick={submitQuiz}>Submit quiz</button>
        {quizResult && (
          <div className={`alert ${quizResult.is_correct ? "alert-success" : "alert-danger"}`} style={{ marginTop: 12 }}>
            {quizResult.message} {quizResult.lesson_completed ? "Lesson marked complete." : "Try again to complete the lesson."}
            {quizResult.explanation && <div>{quizResult.explanation}</div>}
          </div>
        )}
      </div>
      <div style={{ marginTop: 16 }}>
        <h4>External resources</h4>
        {(lesson.external_resources || []).map((r) => (
          <div key={r.url}><a href={r.url} target="_blank" rel="noreferrer">{r.title}</a> ({r.type})</div>
        ))}
      </div>
    </div>
  );
}
