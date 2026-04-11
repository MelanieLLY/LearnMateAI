import { useState, useEffect } from 'react';

interface Module {
  id: number;
  title: string;
  description: string;
  learning_objectives: string | null;
  course_id: number | null;
}

export default function StudentModuleView() {
  const [modules, setModules] = useState<Module[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [notes, setNotes] = useState<Record<number, string>>({});
  const [submitting, setSubmitting] = useState<Record<number, boolean>>({});

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
      const data = await response.json();
      setModules(data);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unknown error occurred');
      }
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

      alert('Note uploaded successfully!');
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
    <div style={{ fontFamily: 'sans-serif', maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <h1>👨‍🎓 学生端：模块浏览与学习</h1>
      <p>在这里，学生可以浏览发布的课程模块，下载学习材料，并上传学习笔记。</p>
      
      {error && <p style={{ color: 'red', padding: '10px', border: '1px solid red' }}>错误: {error}</p>}

      <section>
        {modules.length === 0 ? (
          <p>暂无可用模块</p>
        ) : (
          <ul style={{ listStyleType: 'none', padding: 0 }}>
            {modules.map(mod => (
              <li key={mod.id} style={{ border: '1px solid #ddd', padding: '20px', marginBottom: '20px', borderRadius: '8px', backgroundColor: '#f9f9f9' }}>
                <h3 style={{ margin: '0 0 10px 0', color: '#333' }}>📄 {mod.title}</h3>
                <p style={{ color: '#555' }}>{mod.description}</p>
                {mod.learning_objectives && (
                  <p><strong>重点目标 (Objectives):</strong> {mod.learning_objectives}</p>
                )}
                
                <div style={{ marginTop: '15px', padding: '15px', backgroundColor: '#e2f0d9', borderRadius: '4px' }}>
                  <h4 style={{ margin: '0 0 10px 0' }}>📝 提交学习笔记</h4>
                  <textarea 
                    style={{ width: '100%', minHeight: '80px', padding: '8px', marginBottom: '10px', boxSizing: 'border-box' }}
                    placeholder="在这里输入你的学习笔记、问题或心得..."
                    value={notes[mod.id] || ''}
                    onChange={(e) => handleNoteChange(mod.id, e.target.value)}
                  />
                  <button 
                    onClick={() => handleUploadNote(mod.id)}
                    disabled={submitting[mod.id] || !notes[mod.id]?.trim()}
                    style={{ 
                      padding: '8px 16px', 
                      backgroundColor: (submitting[mod.id] || !notes[mod.id]?.trim()) ? '#ccc' : '#4CAF50', 
                      color: 'white', 
                      border: 'none', 
                      borderRadius: '4px', 
                      cursor: (submitting[mod.id] || !notes[mod.id]?.trim()) ? 'not-allowed' : 'pointer' 
                    }}
                  >
                    {submitting[mod.id] ? '提交中...' : '提交笔记'}
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
