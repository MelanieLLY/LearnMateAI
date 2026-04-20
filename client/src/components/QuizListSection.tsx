import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

interface QuizQuestion {
  id: number;
  text: string;
  question_type: string;
  options?: string[];
  correct_answer: string;
  explanation: string;
}

export interface Quiz {
  id: number;
  module_id: number;
  student_id: number;
  is_instructor_assigned: boolean;
  title: string;
  difficulty_level: string;
  questions: QuizQuestion[];
  created_at: string;
}

interface QuizListSectionProps {
  moduleId: number;
}

export default function QuizListSection({ moduleId }: QuizListSectionProps) {
  const navigate = useNavigate();
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadQuizzes = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const res = await fetch(`/api/v1/modules/${moduleId}/quizzes`, {
        credentials: 'include',
      });
      if (!res.ok) throw new Error('Failed to load quizzes');
      const data: Quiz[] = await res.json();
      setQuizzes(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadQuizzes();
  }, [moduleId]);

  if (isLoading) {
    return (
      <div className="py-6 flex flex-col items-center gap-4 animate-pulse">
        <div className="w-full h-16 bg-slate-200 rounded-xl" />
        <div className="w-full h-16 bg-slate-200 rounded-xl" />
      </div>
    );
  }

  const instructorQuizzes = quizzes.filter((q) => q.is_instructor_assigned);
  const studentQuizzes = quizzes.filter((q) => !q.is_instructor_assigned);

  return (
    <div className="space-y-6">
      {error && (
        <div className="bg-red-50 text-red-600 px-4 py-3 rounded-xl text-sm border border-red-100">
          ⚠️ {error}
        </div>
      )}

      {/* Instructor Quizzes Section */}
      <div className="bg-brand-50/50 rounded-xl p-5 border border-brand-100 shadow-sm">
        <h4 className="font-semibold text-brand-800 mb-3 flex items-center gap-2">
          <span>📚</span> 随堂测验 (Instructor Assessments)
        </h4>
        {instructorQuizzes.length === 0 ? (
          <p className="text-slate-500 text-sm">暂无老师布置的测验</p>
        ) : (
          <div className="space-y-3">
            {instructorQuizzes.map((quiz) => (
              <div 
                key={quiz.id} 
                className="flex items-center justify-between bg-white p-4 rounded-xl border border-brand-200 shadow-sm hover:shadow-md transition-shadow cursor-pointer"
                onClick={() => navigate(`/student/take-quiz/${quiz.id}`)}
              >
                <div>
                  <h5 className="font-bold text-slate-800">{quiz.title}</h5>
                  <p className="text-xs text-slate-500 mt-1">
                    {quiz.questions.length} 题 • {new Date(quiz.created_at).toLocaleDateString()}
                  </p>
                </div>
                <button className="px-4 py-2 bg-brand-600 hover:bg-brand-500 text-white font-medium text-sm rounded-lg transition-colors">
                  开始作答
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Student Self-Practice Quizzes */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h4 className="font-semibold text-slate-700 flex items-center gap-2">
            <span>✨</span> 我的自测练习 (Self-Practice)
          </h4>
          <button
            onClick={() => navigate(`/student/quiz/${moduleId}`)}
            className="px-4 py-2 text-sm font-semibold bg-white border border-slate-300 hover:border-brand-500 hover:text-brand-600 text-slate-700 rounded-lg shadow-sm transition-all"
          >
            + 自动生成新练习
          </button>
        </div>
        
        {studentQuizzes.length === 0 ? (
          <p className="text-slate-500 text-sm italic">还没有生成过任何自测练手卷...</p>
        ) : (
          <div className="space-y-3">
            {studentQuizzes.map((quiz) => (
              <div 
                key={quiz.id} 
                className="flex items-center justify-between bg-slate-50 p-4 rounded-xl border border-slate-200 hover:bg-white transition-colors cursor-pointer"
                onClick={() => navigate(`/student/take-quiz/${quiz.id}`)}
              >
                <div>
                  <h5 className="font-medium text-slate-700">{quiz.title}</h5>
                  <p className="text-xs text-slate-400 mt-1">
                    难度: {quiz.difficulty_level} • {quiz.questions.length} 题
                  </p>
                </div>
                <button className="text-brand-600 hover:text-brand-700 font-medium text-sm px-3 py-1.5 hover:bg-brand-50 rounded bg-transparent">
                  继续练习
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
