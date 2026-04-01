import { useState, useEffect } from 'react';
import type { FormEvent } from 'react';

interface Course {
  id: number;
  title: string;
  description: string;
  audience_context: string | null;
}

interface Module {
  id: number;
  title: string;
  description: string;
  learning_objectives: string | null;
  audience_context: string | null;
  course_id: number | null;
  created_at: string;
}

export default function InstructorModuleDashboard() {
  const [modules, setModules] = useState<Module[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [token, setToken] = useState<string>('');
  const [error, setError] = useState<string | null>(null);

  // Global Class (Course) selection
  const [selectedCourseId, setSelectedCourseId] = useState<number | 'none' | 'new'>('none');
  
  // New Course Form State
  const [courseTitle, setCourseTitle] = useState('');
  const [courseDesc, setCourseDesc] = useState('');
  const [courseAudience, setCourseAudience] = useState('');

  // New Module Form State
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [objectives, setObjectives] = useState('');

  const fetchDashboardData = async (currentToken: string) => {
    if (!currentToken) return;
    try {
      const headers = { 'Authorization': `Bearer ${currentToken}` };
      
      const [modulesRes, coursesRes] = await Promise.all([
        fetch('/api/v1/modules', { headers }),
        fetch('/api/v1/courses', { headers })
      ]);
      
      if (!modulesRes.ok || !coursesRes.ok) throw new Error('Failed to fetch data');
      
      const mods = await modulesRes.json();
      const crs = await coursesRes.json();
      
      setModules(mods);
      setCourses(crs);
      setError(null);
    } catch (err: any) {
      setError(err.message);
    }
  };

  useEffect(() => {
    const savedToken = localStorage.getItem('instructorToken');
    if (savedToken) {
      setToken(savedToken);
      fetchDashboardData(savedToken);
    }
  }, []);

  const handleTokenSave = () => {
    localStorage.setItem('instructorToken', token);
    fetchDashboardData(token);
  };

  const handleCreateCourse = async (e: FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/v1/courses', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          title: courseTitle,
          description: courseDesc,
          audience_context: courseAudience
        })
      });
      if (!response.ok) throw new Error('Create course failed');
      
      const newCourse = await response.json();
      setCourseTitle('');
      setCourseDesc('');
      setCourseAudience('');
      await fetchDashboardData(token);
      setSelectedCourseId(newCourse.id);
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleCreateModule = async (e: FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/v1/modules', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          title,
          description,
          learning_objectives: objectives,
          // If no specific class selected, module has no class context
          course_id: selectedCourseId === 'none' || selectedCourseId === 'new' ? null : selectedCourseId,
        })
      });
      if (!response.ok) throw new Error('Create module failed');
      
      setTitle('');
      setDescription('');
      setObjectives('');
      fetchDashboardData(token);
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleUploadMaterial = async (moduleId: number, file: File | null) => {
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    try {
      const response = await fetch(`/api/v1/modules/${moduleId}/materials`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData
      });
      if (!response.ok) throw new Error('Upload failed');
      const result = await response.json();
      alert(`Upload success! URL: ${result.url}`);
    } catch (err: any) {
      alert(err.message);
    }
  };

  // Filter modules to matching course ID, or map all if 'none'/'new' is selected
  const displayModules = selectedCourseId === 'none' 
    ? modules 
    : (selectedCourseId === 'new' ? [] : modules.filter(m => m.course_id === selectedCourseId));

  return (
    <div style={{ fontFamily: 'sans-serif' }}>
      <h1>👨‍🏫 教员工作台 (Instructor Dashboard)</h1>

      <section style={{ border: '2px dashed red', padding: '10px', marginBottom: '20px' }}>
        <h3>0. 认证配置 (Auth Setup)</h3>
        <input 
          type="text" 
          placeholder="Paste JWT Bearer Token..."
          value={token}
          onChange={(e) => setToken(e.target.value)}
          style={{ width: '80%', padding: '5px' }}
        />
        <button onClick={handleTokenSave} style={{ marginLeft: '10px', padding: '5px 10px' }}>加载数据</button>
        {error && <p style={{ color: 'red' }}>错误: {error}</p>}
      </section>

      <section style={{ padding: '20px', backgroundColor: '#eef', marginBottom: '20px' }}>
        <h2>1. 选择班级上下文 (Global Class Context)</h2>
        <div style={{ marginBottom: '15px' }}>
          <strong>当前操作班级：</strong>
          <select 
            value={selectedCourseId} 
            onChange={(e) => setSelectedCourseId(e.target.value === 'none' || e.target.value === 'new' ? e.target.value : Number(e.target.value))}
            style={{ padding: '5px', marginLeft: '10px', width: '300px' }}
          >
            <option value="none">-- 游荡模块 / 全部 (Orphan Modules / All) --</option>
            {courses.map(c => <option key={c.id} value={c.id}>📚 {c.title}</option>)}
            <option value="new">➕ 新建一个班级 (Create New Class)...</option>
          </select>
        </div>

        {selectedCourseId === 'new' && (
          <form onSubmit={handleCreateCourse} style={{ display: 'flex', flexDirection: 'column', gap: '10px', padding: '10px', border: '1px solid blue' }}>
            <h4>快速创建班级</h4>
            <input required placeholder="班级名称 (Class Name)" value={courseTitle} onChange={e => setCourseTitle(e.target.value)} />
            <textarea placeholder="班级介绍 (Description)" value={courseDesc} onChange={e => setCourseDesc(e.target.value)} />
            <textarea placeholder="受众背景/情感敏感度 (Audience Context)" value={courseAudience} onChange={e => setCourseAudience(e.target.value)} />
            <button type="submit">创建并选中班级</button>
          </form>
        )}
      </section>

      <section style={{ padding: '20px', backgroundColor: '#f9f9f9', marginBottom: '20px' }}>
        <h2>2. 在当前上下文中创建模块 (Create Module)</h2>
        <form onSubmit={handleCreateModule} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <input required placeholder="模块标题 (Title)" value={title} onChange={e => setTitle(e.target.value)} />
          <textarea placeholder="基本描述 (Description)" value={description} onChange={e => setDescription(e.target.value)} />
          <textarea placeholder="当前模块具体学习目标 (Learning Objectives)" value={objectives} onChange={e => setObjectives(e.target.value)} />
          <button type="submit" disabled={selectedCourseId === 'new'}>
            ➕ {typeof selectedCourseId === 'number' ? '为选中的班级添加模块' : '创建孤立模块'}
          </button>
        </form>
      </section>

      <section style={{ padding: '20px', borderTop: '2px solid #ccc' }}>
        <h2>3. 模块列表与资料上传 (Modules in Selection)</h2>
        {displayModules.length === 0 ? <p>当前视图暂无模块</p> : (
          <ul style={{ listStyleType: 'none', padding: 0 }}>
            {displayModules.map(mod => (
              <li key={mod.id} style={{ border: '1px solid #ddd', padding: '15px', marginBottom: '15px', backgroundColor: '#fff' }}>
                <h3 style={{ margin: '0 0 10px 0' }}>📄 {mod.title} {mod.course_id ? '(已绑定班级)' : '(孤立)'}</h3>
                <p><small>{mod.description}</small></p>
                <p><strong>Learning Obj:</strong> {mod.learning_objectives}</p>
                
                <div style={{ marginTop: '15px', padding: '10px', backgroundColor: '#f0f0f0' }}>
                  <strong>⬆️ 上传课程资料 (PDF/Image 等): </strong>
                  <input 
                    type="file" 
                    onChange={(e) => {
                      if (e.target.files && e.target.files.length > 0) {
                        handleUploadMaterial(mod.id, e.target.files[0]);
                        e.target.value = '';
                      }
                    }} 
                  />
                </div>
              </li>
            ))}
          </ul>
        )}
      </section>

    </div>
  );
}
