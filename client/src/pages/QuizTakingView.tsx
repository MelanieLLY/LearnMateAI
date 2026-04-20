import { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------
type Phase = 'setup' | 'loading' | 'taking' | 'results';
type Difficulty = 'Easy' | 'Medium' | 'Hard';

interface QuizQuestion {
  id: number;
  text: string;
  question_type: 'multiple_choice' | 'short_answer';
  options: string[] | null;
  correct_answer: string;
  explanation: string;
}

interface Quiz {
  id: number;
  module_id: number;
  student_id: number;
  title: string;
  difficulty_level: string;
  questions: QuizQuestion[];
  created_at: string;
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
const DIFFICULTY_STYLES: Record<
  Difficulty,
  { active: string; ring: string }
> = {
  Easy: {
    active: 'bg-green-500 text-white border-green-500',
    ring: 'ring-green-400',
  },
  Medium: {
    active: 'bg-yellow-500 text-white border-yellow-500',
    ring: 'ring-yellow-400',
  },
  Hard: {
    active: 'bg-red-500 text-white border-red-500',
    ring: 'ring-red-400',
  },
};

function gradeFromScore(score: number): { letter: string; color: string } {
  if (score >= 90) return { letter: 'A', color: 'text-green-600' };
  if (score >= 80) return { letter: 'B', color: 'text-blue-600' };
  if (score >= 70) return { letter: 'C', color: 'text-yellow-600' };
  if (score >= 60) return { letter: 'D', color: 'text-orange-600' };
  return { letter: 'F', color: 'text-red-600' };
}

function computeScore(quiz: Quiz, answers: Record<number, string>): number {
  const mc = quiz.questions.filter(q => q.question_type === 'multiple_choice');
  const correctMC = mc.filter(
    q => (answers[q.id] ?? '').trim() === q.correct_answer.trim(),
  ).length;
  const saAttempted = quiz.questions.filter(
    q => q.question_type === 'short_answer' && (answers[q.id] ?? '').trim(),
  ).length;
  return Math.round(((correctMC + saAttempted) / quiz.questions.length) * 100);
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------
export default function QuizTakingView(): JSX.Element {
  const { moduleId, quizId } = useParams<{ moduleId?: string, quizId?: string }>();
  const navigate = useNavigate();

  const [phase, setPhase] = useState<Phase>(quizId ? 'loading' : 'setup');
  const [difficulty, setDifficulty] = useState<Difficulty>('Medium');
  const [numQuestions, setNumQuestions] = useState<number>(5);
  const [quiz, setQuiz] = useState<Quiz | null>(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [error, setError] = useState<string | null>(null);
  const [finalScore, setFinalScore] = useState(0);
  const [displayScore, setDisplayScore] = useState(0);

  // Animated count-up for the score circle
  useEffect(() => {
    if (phase !== 'results') return;
    let current = 0;
    const step = Math.max(1, Math.ceil(finalScore / 30));
    const id = setInterval(() => {
      current = Math.min(current + step, finalScore);
      setDisplayScore(current);
      if (current >= finalScore) clearInterval(id);
    }, 40);
    return () => clearInterval(id);
  }, [phase, finalScore]);

  const fetchExistingQuiz = useCallback(async () => {
    try {
      const res = await fetch(`/api/v1/quizzes/${quizId}`, {
        credentials: 'include',
      });
      if (!res.ok) throw new Error('Failed to fetch quiz');
      const data: Quiz = await res.json();
      setQuiz(data);
      setPhase('taking');
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Unknown error');
      setPhase('setup'); // Fallback if error
    }
  }, [quizId]);

  // If taking an existing quiz, fetch it on mount
  useEffect(() => {
    if (quizId && phase === 'loading') {
      fetchExistingQuiz();
    }
  }, [quizId, phase, fetchExistingQuiz]);

  const generateQuiz = async () => {
    if (!moduleId) return;
    setPhase('loading');
    setError(null);
    try {
      const res = await fetch(`/api/v1/modules/${moduleId}/quizzes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ difficulty_level: difficulty, num_questions: numQuestions }),
      });
      if (!res.ok) throw new Error('Failed to generate quiz');
      const data: Quiz = await res.json();
      setQuiz(data);
      setCurrentIndex(0);
      setAnswers({});
      setDisplayScore(0);
      setPhase('taking');
    } catch (err: unknown) {
      setError(
        err instanceof Error ? err.message : 'Failed to generate quiz',
      );
      setPhase('setup');
    }
  };

  const handleAnswer = (questionId: number, answer: string) => {
    setAnswers(prev => ({ ...prev, [questionId]: answer }));
  };

  const handleSubmit = async () => {
    if (!quiz) return;
    const score = computeScore(quiz, answers);
    setFinalScore(score);
    
    try {
      const res = await fetch(`/api/v1/quizzes/${quiz.id}/submit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ score }),
      });
      if (!res.ok) {
        console.error('Failed to save quiz submission:', await res.text());
      }
    } catch (err) {
      console.error('Failed to save quiz submission:', err);
    }
    
    setPhase('results');
  };

  // -------------------------------------------------------------------------
  // Phase: setup
  // -------------------------------------------------------------------------
  if (phase === 'setup' && !quizId) {
    return (
      <div className="max-w-2xl mx-auto space-y-8">
        <header className="pl-2">
          <button
            onClick={() => navigate('/student')}
            className="text-sm text-slate-500 hover:text-brand-600 flex items-center gap-1 mb-4 transition-colors"
          >
            ← Back to Modules
          </button>
          <h1 className="text-3xl font-extrabold text-slate-800 mb-2">
            🧠 Generate Quiz
          </h1>
          <p className="text-slate-500">
            Choose a difficulty level for your AI-powered quiz.
          </p>
        </header>

        {error && (
          <div className="bg-red-50 text-red-600 px-4 py-3 rounded-xl text-sm border border-red-100 flex items-center gap-2">
            <span>⚠️</span>
            <span>{error}</span>
          </div>
        )}

        <div className="glass-panel p-8 rounded-2xl space-y-6">
          <div>
            <h2 className="font-semibold text-slate-700 mb-3">
              Select Difficulty
            </h2>
            <div className="flex gap-3">
              {(['Easy', 'Medium', 'Hard'] as Difficulty[]).map(d => {
                const isActive = difficulty === d;
                return (
                  <button
                    key={d}
                    onClick={() => setDifficulty(d)}
                    className={`flex-1 py-3 rounded-xl font-semibold transition-all shadow-sm border-2 ${
                      isActive
                        ? `${DIFFICULTY_STYLES[d].active} ring-2 ${DIFFICULTY_STYLES[d].ring} ring-offset-2`
                        : 'bg-white text-slate-600 border-slate-200 hover:border-brand-300'
                    }`}
                  >
                    {d}
                  </button>
                );
              })}
            </div>
          </div>

          <div>
            <h2 className="font-semibold text-slate-700 mb-3 flex justify-between items-center">
              <span>Number of Questions</span>
              <span className="text-brand-600 font-bold bg-brand-50 px-2 py-0.5 rounded-md">{numQuestions}</span>
            </h2>
            <input
              type="range"
              min="1"
              max="15"
              value={numQuestions}
              onChange={(e) => setNumQuestions(Number(e.target.value))}
              className="w-full accent-brand-600 cursor-pointer h-2 bg-slate-200 rounded-lg appearance-none"
            />
            <div className="flex justify-between text-xs text-slate-400 mt-2 font-medium">
              <span>1</span>
              <span>15</span>
            </div>
          </div>

          <button
            onClick={generateQuiz}
            className="w-full py-4 bg-brand-600 hover:bg-brand-500 text-white font-bold text-lg rounded-xl transition-all shadow-lg hover:shadow-xl transform active:scale-[0.98]"
          >
            ✨ Generate Quiz
          </button>
        </div>
      </div>
    );
  }

  // -------------------------------------------------------------------------
  // Phase: loading
  // -------------------------------------------------------------------------
  if (phase === 'loading') {
    return (
      <div
        data-testid="quiz-loading"
        className="max-w-2xl mx-auto flex flex-col items-center justify-center py-24"
      >
        <div className="w-16 h-16 border-4 border-brand-200 border-t-brand-600 rounded-full animate-spin mb-6" />
        <p className="text-slate-600 font-medium text-lg">
          Generating your quiz with AI…
        </p>
        <p className="text-slate-400 text-sm mt-2">
          This may take a few seconds
        </p>
      </div>
    );
  }

  // -------------------------------------------------------------------------
  // Phase: taking
  // -------------------------------------------------------------------------
  if (phase === 'taking' && quiz) {
    const question = quiz.questions[currentIndex];
    const isLast = currentIndex === quiz.questions.length - 1;
    const currentAnswer = answers[question.id] ?? '';
    const canProceed = currentAnswer.trim().length > 0;
    const optionLabels = ['A', 'B', 'C', 'D'];

    return (
      <div className="max-w-2xl mx-auto space-y-6">
        {/* Header */}
        <header className="flex items-start justify-between pl-2">
          <div>
            <h1 className="text-xl font-bold text-slate-800">{quiz.title}</h1>
            <p className="text-sm text-slate-500 mt-0.5">
              {quiz.difficulty_level} Difficulty
            </p>
          </div>
          <button
            onClick={() => navigate('/student')}
            className="text-sm text-slate-400 hover:text-slate-600 transition-colors mt-1"
          >
            ✕ Exit
          </button>
        </header>

        {/* Progress bar */}
        <div className="glass-panel px-4 py-3 rounded-xl flex items-center gap-4">
          <div className="flex-1 bg-slate-200 rounded-full h-2">
            <div
              className="bg-brand-500 h-2 rounded-full transition-all duration-500"
              style={{
                width: `${((currentIndex + 1) / quiz.questions.length) * 100}%`,
              }}
            />
          </div>
          <span className="text-sm font-semibold text-slate-600 whitespace-nowrap">
            Question {currentIndex + 1} of {quiz.questions.length}
          </span>
        </div>

        {/* Question card */}
        <div className="glass-panel p-8 rounded-2xl">
          <span
            className={`text-xs font-medium px-2.5 py-1 rounded-full ${
              question.question_type === 'multiple_choice'
                ? 'bg-blue-100 text-blue-700'
                : 'bg-purple-100 text-purple-700'
            }`}
          >
            {question.question_type === 'multiple_choice'
              ? 'Multiple Choice'
              : 'Short Answer'}
          </span>

          <p className="text-xl font-semibold text-slate-800 leading-relaxed mt-4 mb-6">
            {question.text}
          </p>

          {/* Multiple choice options */}
          {question.question_type === 'multiple_choice' &&
            question.options && (
              <div className="space-y-3">
                {question.options.map((option, idx) => {
                  const isSelected = currentAnswer === option;
                  return (
                    <button
                      key={idx}
                      onClick={() => handleAnswer(question.id, option)}
                      className={`w-full text-left p-4 rounded-xl border-2 transition-all flex items-start gap-3 ${
                        isSelected
                          ? 'border-brand-500 bg-brand-50 ring-2 ring-brand-500 ring-offset-1'
                          : 'border-slate-200 hover:border-brand-300 hover:bg-slate-50 bg-white'
                      }`}
                    >
                      <span
                        className={`min-w-[28px] h-7 flex-shrink-0 flex items-center justify-center rounded-full text-sm font-bold ${
                          isSelected
                            ? 'bg-brand-500 text-white'
                            : 'bg-slate-100 text-slate-500'
                        }`}
                      >
                        {optionLabels[idx]}
                      </span>
                      <span
                        className={`leading-relaxed ${
                          isSelected
                            ? 'text-brand-800 font-medium'
                            : 'text-slate-700'
                        }`}
                      >
                        {option}
                      </span>
                    </button>
                  );
                })}
              </div>
            )}

          {/* Short answer textarea */}
          {question.question_type === 'short_answer' && (
            <textarea
              className="w-full min-h-[140px] p-4 bg-white border-2 border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500/50 focus:border-brand-500 transition-all placeholder:text-slate-400 resize-y text-slate-800 leading-relaxed"
              placeholder="Type your answer here..."
              value={currentAnswer}
              onChange={e => handleAnswer(question.id, e.target.value)}
            />
          )}
        </div>

        {/* Navigation */}
        <div className="flex items-center justify-between">
          <button
            onClick={() => setCurrentIndex(prev => prev - 1)}
            disabled={currentIndex === 0}
            className="px-5 py-2.5 rounded-xl border-2 border-slate-200 text-slate-600 font-medium hover:border-slate-300 hover:bg-slate-50 transition-all disabled:opacity-30 disabled:cursor-not-allowed"
          >
            ← Previous
          </button>

          {isLast ? (
            <button
              onClick={handleSubmit}
              disabled={!canProceed}
              className="px-8 py-3 bg-brand-600 hover:bg-brand-500 text-white font-bold rounded-xl transition-all shadow-lg hover:shadow-xl transform active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Submit Quiz →
            </button>
          ) : (
            <button
              onClick={() => setCurrentIndex(prev => prev + 1)}
              disabled={!canProceed}
              className="px-8 py-3 bg-brand-600 hover:bg-brand-500 text-white font-bold rounded-xl transition-all shadow-lg hover:shadow-xl transform active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next →
            </button>
          )}
        </div>
      </div>
    );
  }

  // -------------------------------------------------------------------------
  // Phase: results
  // -------------------------------------------------------------------------
  if (phase === 'results' && quiz) {
    const grade = gradeFromScore(displayScore);
    const mc = quiz.questions.filter(
      q => q.question_type === 'multiple_choice',
    );
    const correctMC = mc.filter(
      q => (answers[q.id] ?? '').trim() === q.correct_answer.trim(),
    ).length;
    const saCount = quiz.questions.length - mc.length;

    // SVG circle animation constants
    const RADIUS = 60;
    const CIRCUMFERENCE = 2 * Math.PI * RADIUS;

    return (
      <div className="max-w-2xl mx-auto space-y-8">
        {/* ---- Score Badge ---- */}
        <style>{`
          @keyframes fadeScaleIn {
            from { opacity: 0; transform: scale(0.75); }
            to   { opacity: 1; transform: scale(1); }
          }
          .quiz-results-enter {
            animation: fadeScaleIn 0.45s cubic-bezier(0.34, 1.56, 0.64, 1) both;
          }
        `}</style>

        <div
          data-testid="score-badge"
          className="quiz-results-enter glass-panel p-10 rounded-3xl flex flex-col items-center text-center"
        >
          {/* Circular progress */}
          <div className="relative w-40 h-40 mb-6">
            <svg
              className="w-40 h-40 -rotate-90"
              viewBox="0 0 144 144"
            >
              {/* Track */}
              <circle
                cx="72"
                cy="72"
                r={RADIUS}
                fill="none"
                stroke="#e2e8f0"
                strokeWidth="10"
              />
              {/* Progress arc */}
              <circle
                cx="72"
                cy="72"
                r={RADIUS}
                fill="none"
                stroke="#16a34a"
                strokeWidth="10"
                strokeLinecap="round"
                strokeDasharray={CIRCUMFERENCE}
                strokeDashoffset={CIRCUMFERENCE * (1 - displayScore / 100)}
                style={{ transition: 'stroke-dashoffset 0.08s linear' }}
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-5xl font-extrabold text-slate-800">
                {displayScore}
              </span>
              <span className="text-sm text-slate-500">/ 100</span>
            </div>
          </div>

          <p className="text-slate-500 uppercase tracking-widest text-xs font-semibold mb-1">
            Your Score
          </p>
          <div className={`text-7xl font-black mb-3 ${grade.color}`}>
            {grade.letter}
          </div>
          <p className="text-slate-600 text-sm">
            {correctMC} of {mc.length} multiple-choice correct
            {saCount > 0 &&
              ` · ${saCount} short-answer attempted`}
          </p>

          <div className="flex gap-3 mt-8">
            <button
              onClick={() => {
                setPhase('setup');
                setQuiz(null);
                setAnswers({});
              }}
              className="px-6 py-2.5 border-2 border-slate-200 text-slate-600 font-medium rounded-xl hover:border-slate-300 hover:bg-slate-50 transition-all"
            >
              Try Again
            </button>
            <button
              onClick={() => navigate('/student')}
              className="px-6 py-2.5 bg-brand-600 text-white font-medium rounded-xl hover:bg-brand-500 transition-all shadow-md"
            >
              Back to Modules
            </button>
          </div>
        </div>

        {/* ---- Question Review ---- */}
        <div className="space-y-4">
          <h2 className="text-xl font-bold text-slate-800 pl-1">
            Question Review
          </h2>

          {quiz.questions.map((q, idx) => {
            const userAnswer = answers[q.id] ?? '';
            const isMC = q.question_type === 'multiple_choice';
            const correct = isMC
              ? userAnswer.trim() === q.correct_answer.trim()
              : userAnswer.trim().length > 0;

            return (
              <div
                key={q.id}
                className={`glass-panel p-6 rounded-2xl border-l-4 ${
                  correct ? 'border-l-green-500' : 'border-l-red-500'
                }`}
              >
                <div className="flex items-start gap-3">
                  {/* Status dot */}
                  <span
                    className={`mt-0.5 flex-shrink-0 w-7 h-7 rounded-full flex items-center justify-center text-sm font-bold ${
                      correct
                        ? 'bg-green-100 text-green-700'
                        : 'bg-red-100 text-red-700'
                    }`}
                  >
                    {correct ? '✓' : '✗'}
                  </span>

                  <div className="flex-1 min-w-0">
                    <p className="font-semibold text-slate-800 mb-3">
                      Q{idx + 1}. {q.text}
                    </p>

                    <div className="space-y-1.5 text-sm mb-3">
                      <div className="flex gap-2">
                        <span className="text-slate-500 flex-shrink-0">
                          Your answer:
                        </span>
                        <span
                          className={`font-medium ${
                            correct ? 'text-green-700' : 'text-red-700'
                          }`}
                        >
                          {userAnswer || (
                            <em className="text-slate-400">No answer given</em>
                          )}
                        </span>
                      </div>

                      {!correct && isMC && (
                        <div className="flex gap-2">
                          <span className="text-slate-500 flex-shrink-0">
                            Correct answer:
                          </span>
                          <span className="font-medium text-green-700">
                            {q.correct_answer}
                          </span>
                        </div>
                      )}

                      {!isMC && (
                        <div className="flex gap-2">
                          <span className="text-slate-500 flex-shrink-0">
                            Reference answer:
                          </span>
                          <span className="text-slate-600 italic">
                            {q.correct_answer}
                          </span>
                        </div>
                      )}
                    </div>

                    {/* LLM Feedback bubble */}
                    <div className="bg-amber-50 border border-amber-100 rounded-xl p-3 flex gap-2.5">
                      <span className="text-amber-500 flex-shrink-0 text-base">
                        🤖
                      </span>
                      <p className="text-amber-800 text-sm leading-relaxed">
                        {q.explanation}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  }

  return <></>;
}
