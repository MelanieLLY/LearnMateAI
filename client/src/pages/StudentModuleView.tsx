import { useState, useEffect } from 'react';

interface Module {
  id: number;
  title: string;
  description: string;
  learning_objectives: string | null;
  course_id: number | null;
}

interface Note {
  id: number;
  content: string;
  uploaded_at: string;
}

export default function StudentModuleView() {
  const [modules, setModules] = useState<Module[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [notes, setNotes] = useState<Record<number, string>>({});
  const [pastNotes, setPastNotes] = useState<Record<number, Note[]>>({});
  const [submitting, setSubmitting] = useState<Record<number, boolean>>({});
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchModules();
  }, []);

  const fetchModules = async () => {
    try {
      const isDebug = localStorage.getItem('DEBUG_STUDENT') === 'true';
      const headers: HeadersInit = isDebug ? { 'X-Debug-Student': 'true' } : {};
      
      const response = await fetch('/api/v1/modules', { 
        credentials: 'include',
        headers 
      });
      if (!response.ok) throw new Error('Failed to fetch modules');
      const data: Module[] = await response.json();
      setModules(data);

      // Fetch history notes for all fetched modules
      const notesRecord: Record<number, Note[]> = {};
      await Promise.all(data.map(async (mod) => {
        try {
          const notesRes = await fetch(`/api/v1/modules/${mod.id}/notes`, { credentials: 'include' });
          if (notesRes.ok) {
            notesRecord[mod.id] = await notesRes.json();
          } else {
            notesRecord[mod.id] = [];
          }
        } catch (e) {
          notesRecord[mod.id] = [];
        }
      }));
      setPastNotes(notesRecord);

    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unknown error occurred');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleNoteChange = (moduleId: number, value: string) => {
    setNotes(prev => ({ ...prev, [moduleId]: value }));
  };

  const handleUploadNote = async (moduleId: number) => {
    const content = notes[moduleId];
    if (!content || !content.trim()) {
      alert('Note content cannot be empty');
      return;
    }

    setSubmitting(prev => ({ ...prev, [moduleId]: true }));
    try {
      const response = await fetch(`/api/v1/modules/${moduleId}/notes`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify({ content })
      });

      if (!response.ok) {
        throw new Error('Failed to upload note');
      }

      const newNote: Note = await response.json();
      alert('Note uploaded successfully!');
      
      // Update pastNotes state directly
      setPastNotes(prev => ({
        ...prev,
        [moduleId]: [newNote, ...(prev[moduleId] || [])]
      }));

      // Clear the input after successful upload
      setNotes(prev => ({ ...prev, [moduleId]: '' }));
    } catch (err: unknown) {
      if (err instanceof Error) {
        alert(err.message);
      } else {
        alert('An unknown error occurred');
      }
    } finally {
      setSubmitting(prev => ({ ...prev, [moduleId]: false }));
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <header className="mb-8 pl-2">
        <h1 className="text-3xl font-extrabold text-slate-800 mb-2">👨‍🎓 学生端：模块浏览与学习</h1>
        <p className="text-slate-500">在这里，你可以浏览课程模块，下载学习材料，并记录学习笔记。</p>
      </header>
      
      {error && (
        <div className="bg-red-50 text-red-600 px-4 py-3 rounded-xl mb-6 text-sm flex items-center shadow-sm border border-red-100">
          <span className="mr-2">⚠️</span> 错误: {error}
        </div>
      )}

      <section>
        {isLoading ? (
          <div className="space-y-6">
            {[1, 2].map(i => (
              <div key={i} className="glass-panel p-6 rounded-2xl animate-pulse">
                <div className="h-6 bg-slate-200 rounded w-1/3 mb-4"></div>
                <div className="space-y-3">
                  <div className="h-4 bg-slate-200 rounded w-full"></div>
                  <div className="h-4 bg-slate-200 rounded w-5/6"></div>
                </div>
                <div className="mt-6 h-32 bg-slate-100 rounded-xl"></div>
              </div>
            ))}
          </div>
        ) : modules.length === 0 ? (
          <div className="text-center py-16 glass-panel rounded-2xl">
            <div className="text-4xl mb-4">📭</div>
            <p className="text-slate-500 text-lg">暂无可用模块</p>
          </div>
        ) : (
          <ul className="space-y-6">
            {modules.map(mod => (
              <li key={mod.id} className="glass-panel p-6 sm:p-8 rounded-2xl transition-all hover:shadow-xl hover:border-brand-500/30">
                <h3 className="text-2xl font-bold text-slate-800 mb-3 flex items-center gap-2">
                  <span className="text-brand-500">📄</span> {mod.title}
                </h3>
                <p className="text-slate-600 leading-relaxed mb-4">{mod.description}</p>
                {mod.learning_objectives && (
                  <div className="bg-blue-50/50 rounded-xl p-4 mb-6 border border-blue-100/50 text-sm">
                    <strong className="text-blue-800 block mb-1">重点目标 (Objectives)</strong>
                    <span className="text-blue-700/80">{mod.learning_objectives}</span>
                  </div>
                )}
                
                <div className="mt-6 bg-brand-50/50 rounded-xl p-5 border border-brand-100 shadow-sm">
                  <h4 className="font-semibold text-brand-800 mb-3 flex items-center gap-2">
                    <span>📝</span> 提交学习笔记
                  </h4>
                  <textarea 
                    className="w-full min-h-[100px] p-4 bg-white border border-brand-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500/50 focus:border-brand-500 transition-all placeholder:text-slate-400 resize-y mb-4 shadow-sm"
                    placeholder="在这里输入你的学习笔记、问题或心得..."
                    value={notes[mod.id] || ''}
                    onChange={(e) => handleNoteChange(mod.id, e.target.value)}
                  />
                  <div className="flex justify-end">
                    <button 
                      onClick={() => handleUploadNote(mod.id)}
                      disabled={submitting[mod.id] || !notes[mod.id]?.trim()}
                      className="px-6 py-2.5 bg-brand-600 hover:bg-brand-500 text-white font-medium rounded-xl transition-all shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transform active:scale-[0.98]"
                    >
                      {submitting[mod.id] ? '提交中...' : '提交笔记'}
                    </button>
                  </div>
                </div>

                {/* --- History Notes Section --- */}
                {pastNotes[mod.id] && pastNotes[mod.id].length > 0 && (
                  <div className="mt-6 relative">
                    <h4 className="font-semibold text-slate-700 mb-4 px-1 flex items-center gap-2">
                      <span>📚</span> 我的历史笔记
                      <span className="bg-slate-100 text-slate-500 text-xs py-0.5 px-2 rounded-full font-medium">
                        {pastNotes[mod.id].length} 篇
                      </span>
                    </h4>
                    <div className="space-y-3">
                      {pastNotes[mod.id].map(note => (
                        <div key={note.id} className="bg-white p-4 rounded-xl border border-slate-100 shadow-sm hover:shadow-md transition-shadow">
                          <div className="text-xs font-medium tracking-wide text-brand-600/80 mb-2 uppercase">
                            {new Date(note.uploaded_at).toLocaleString()}
                          </div>
                          <p className="text-slate-700 whitespace-pre-wrap leading-relaxed text-sm">
                            {note.content}
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
