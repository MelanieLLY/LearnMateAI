import { useState, useEffect } from 'react';

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

export default function InstructorQuizSection({ moduleId }: { moduleId: number }) {
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [editingQuiz, setEditingQuiz] = useState<Quiz | null>(null);
  
  const loadQuizzes = async () => {
    try {
      const res = await fetch(`/api/v1/modules/${moduleId}/quizzes`, { credentials: 'include' });
      if (res.ok) {
        setQuizzes(await res.json());
      }
    } catch {
      // ignore
    }
  };

  useEffect(() => {
    loadQuizzes();
  }, [moduleId]);

  const handleGenerateQuiz = async () => {
    setIsGenerating(true);
    try {
      const res = await fetch(`/api/v1/modules/${moduleId}/quizzes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ difficulty_level: 'Medium', num_questions: 5 })
      });
      if (!res.ok) throw new Error('Failed to generate quiz');
      await loadQuizzes();
      alert('已成功生成一套随机标准测验卷！');
    } catch (err: unknown) {
      alert(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleSaveEdit = async () => {
    if (!editingQuiz) return;
    try {
      const res = await fetch(`/api/v1/quizzes/${editingQuiz.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          title: editingQuiz.title,
          questions: editingQuiz.questions
        })
      });
      if (!res.ok) throw new Error('Failed to update quiz');
      setEditingQuiz(null);
      loadQuizzes();
    } catch (err: unknown) {
      alert(err instanceof Error ? err.message : 'Error updating quiz');
    }
  };

  const handleQuestionChange = (qIndex: number, field: keyof QuizQuestion, value: string | string[]) => {
    if (!editingQuiz) return;
    const updated = { ...editingQuiz };
    updated.questions[qIndex] = { ...updated.questions[qIndex], [field]: value };
    setEditingQuiz(updated);
  };

  const handleOptionChange = (qIndex: number, optIndex: number, value: string) => {
    if (!editingQuiz || !editingQuiz.questions[qIndex].options) return;
    const updated = { ...editingQuiz };
    const newOptions = [...updated.questions[qIndex].options!];
    newOptions[optIndex] = value;
    updated.questions[qIndex].options = newOptions;
    setEditingQuiz(updated);
  };

  return (
    <div className="mt-6 bg-purple-50/50 p-5 rounded-xl border border-purple-100">
      <div className="flex items-center justify-between mb-4">
        <h4 className="font-semibold text-purple-800 flex items-center gap-2">
          <span>🧠</span> 随堂测验管理 (Assessments)
        </h4>
        <button 
          onClick={handleGenerateQuiz}
          disabled={isGenerating}
          className="px-4 py-2 bg-purple-600 hover:bg-purple-500 text-white text-sm font-medium rounded-lg transition-colors shadow-sm disabled:opacity-50"
        >
          {isGenerating ? 'AI 生成中...' : '✨ 快速生成新测验'}
        </button>
      </div>

      {quizzes.length === 0 ? (
        <p className="text-slate-500 text-sm">此模块暂未发布任何随堂测验。</p>
      ) : (
        <div className="space-y-4">
          {quizzes.map(quiz => (
            <div key={quiz.id} className="bg-white p-4 rounded-xl border border-purple-200">
              {editingQuiz?.id === quiz.id ? (
                <div className="space-y-5">
                  <div className="font-semibold text-slate-800 border-b pb-2 mb-4">✎ 编辑测验 (Edit Quiz)</div>
                  <div>
                    <label className="block text-xs text-slate-500 mb-1">测验标题</label>
                    <input 
                      className="w-full px-3 py-2 border border-slate-300 rounded focus:border-brand-500 outline-none" 
                      value={editingQuiz.title} 
                      onChange={e => setEditingQuiz({ ...editingQuiz, title: e.target.value })} 
                    />
                  </div>
                  
                  {editingQuiz.questions.map((q, idx) => (
                    <div key={q.id} className="p-3 bg-slate-50 border border-slate-200 rounded text-sm space-y-3">
                      <div className="font-medium text-slate-700">题目 {idx + 1}</div>
                      <textarea 
                        className="w-full px-3 py-2 border border-slate-300 rounded outline-none h-20"
                        value={q.text}
                        onChange={e => handleQuestionChange(idx, 'text', e.target.value)}
                      />
                      
                      {q.question_type === 'multiple_choice' && q.options && (
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-2">
                          {q.options.map((opt, oIdx) => (
                            <div key={oIdx} className="flex items-center gap-2">
                              <span className="text-slate-500 font-bold w-4">{String.fromCharCode(65+oIdx)}.</span>
                              <input 
                                className="flex-1 px-2 py-1 border border-slate-300 rounded outline-none text-xs" 
                                value={opt}
                                onChange={e => handleOptionChange(idx, oIdx, e.target.value)}
                              />
                            </div>
                          ))}
                        </div>
                      )}

                      <div className="mt-2">
                        <label className="text-xs font-semibold text-green-700 block mb-1">正确答案 (必须与上方一致)</label>
                        <input 
                          className="w-full px-3 py-1.5 border border-green-300 bg-green-50 rounded outline-none" 
                          value={q.correct_answer} 
                          onChange={e => handleQuestionChange(idx, 'correct_answer', e.target.value)} 
                        />
                      </div>
                    </div>
                  ))}

                  <div className="flex gap-2 pt-2">
                    <button onClick={handleSaveEdit} className="px-4 py-2 bg-green-600 text-white text-sm rounded shadow-sm hover:bg-green-500">保存修改</button>
                    <button onClick={() => setEditingQuiz(null)} className="px-4 py-2 bg-slate-200 text-slate-700 text-sm rounded hover:bg-slate-300">取消</button>
                  </div>
                </div>
              ) : (
                <div className="flex items-center justify-between">
                  <div>
                    <h5 className="font-bold text-slate-800">{quiz.title}</h5>
                    <p className="text-xs text-slate-500 mt-1">包含 {quiz.questions.length} 题 • {new Date(quiz.created_at).toLocaleDateString()}</p>
                  </div>
                  <button onClick={() => setEditingQuiz(quiz)} className="px-3 py-1.5 text-xs font-medium text-purple-700 bg-purple-100 rounded hover:bg-purple-200 transition-colors">
                    ✏️ 编辑题目
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
