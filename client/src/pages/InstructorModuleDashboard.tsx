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

interface Material {
  id: number;
  module_id: number;
  filename: string;
  url: string;
  annotation?: string | null;
}

export default function InstructorModuleDashboard() {
  const [modules, setModules] = useState<Module[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [materialsByModule, setMaterialsByModule] = useState<Record<number, Material[]>>({});
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

  // Edit Course State
  const [editingCourseId, setEditingCourseId] = useState<number | null>(null);
  const [editCourseForm, setEditCourseForm] = useState<Partial<Course>>({});

  // Edit Module State
  const [editingModuleId, setEditingModuleId] = useState<number | null>(null);
  const [editForm, setEditForm] = useState<Partial<Module>>({});

  // Pending Upload State
  const [pendingFiles, setPendingFiles] = useState<Record<number, File | null>>({});
  const [uploadAnnotations, setUploadAnnotations] = useState<Record<number, string>>({});

  // Material Edit State
  const [editingMaterialId, setEditingMaterialId] = useState<number | null>(null);
  const [materialEditAnnotation, setMaterialEditAnnotation] = useState('');

  const fetchDashboardData = async () => {
    try {
      const fetchOpts = { credentials: 'include' as RequestCredentials };
      
      const [modulesRes, coursesRes] = await Promise.all([
        fetch('/api/v1/modules', fetchOpts),
        fetch('/api/v1/courses', fetchOpts)
      ]);
      
      if (!modulesRes.ok || !coursesRes.ok) throw new Error('Failed to fetch data');
      
      const mods = await modulesRes.json();
      const crs = await coursesRes.json();
      
      setModules(mods);
      setCourses(crs);
      setError(null);

      // Fetch materials
      const matsMap: Record<number, Material[]> = {};
      await Promise.all(mods.map(async (m: Module) => {
        try {
          const res = await fetch(`/api/v1/modules/${m.id}/materials`, fetchOpts);
          if (res.ok) matsMap[m.id] = await res.json();
        } catch (e) {
          // Ignore failures
        }
      }));
      setMaterialsByModule(matsMap);
    } catch (err: any) {
      setError(err.message);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const handleCreateCourse = async (e: FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/v1/courses', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
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
      await fetchDashboardData();
      setSelectedCourseId(newCourse.id);
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleEditCourse = async () => {
    try {
      const res = await fetch(`/api/v1/courses/${editingCourseId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(editCourseForm)
      });
      if (!res.ok) throw new Error('Failed to update course');
      setEditingCourseId(null);
      fetchDashboardData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleDeleteCourse = async (courseId: number) => {
    if (!confirm('确定要删除这个班级吗？相关联的模块将失去关联变成游荡模块。')) return;
    try {
      const res = await fetch(`/api/v1/courses/${courseId}`, {
        method: 'DELETE',
        credentials: 'include'
      });
      if (!res.ok) throw new Error('Failed to delete course');
      if (selectedCourseId === courseId) {
        setSelectedCourseId('none');
      }
      fetchDashboardData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const startEditingCourse = () => {
    const activeCourse = courses.find(c => c.id === selectedCourseId);
    if (!activeCourse) return;
    setEditingCourseId(activeCourse.id);
    setEditCourseForm({
      title: activeCourse.title,
      description: activeCourse.description,
      audience_context: activeCourse.audience_context
    });
  };

  const handleCreateModule = async (e: FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/v1/modules', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          title,
          description,
          learning_objectives: objectives,
          course_id: selectedCourseId === 'none' || selectedCourseId === 'new' ? null : selectedCourseId,
        })
      });
      if (!response.ok) throw new Error('Create module failed');
      
      setTitle('');
      setDescription('');
      setObjectives('');
      fetchDashboardData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleDeleteModule = async (moduleId: number) => {
    if (!confirm('确定要删除这个模块吗？')) return;
    try {
      const res = await fetch(`/api/v1/modules/${moduleId}`, {
        method: 'DELETE',
        credentials: 'include'
      });
      if (!res.ok) throw new Error('Failed to delete module');
      fetchDashboardData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const startEditing = (mod: Module) => {
    setEditingModuleId(mod.id);
    setEditForm({
      title: mod.title,
      description: mod.description,
      learning_objectives: mod.learning_objectives,
      course_id: mod.course_id
    });
  };

  const saveEdit = async () => {
    try {
      const res = await fetch(`/api/v1/modules/${editingModuleId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(editForm)
      });
      if (!res.ok) throw new Error('Failed to update module');
      setEditingModuleId(null);
      fetchDashboardData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleUploadMaterial = async (moduleId: number) => {
    const file = pendingFiles[moduleId];
    if (!file) {
      alert('请先选择要上传的文件');
      return;
    }
    const formData = new FormData();
    formData.append('file', file);
    const annotation = uploadAnnotations[moduleId] || '';
    if (annotation) {
      formData.append('annotation', annotation);
    }
    try {
      const response = await fetch(`/api/v1/modules/${moduleId}/materials`, {
        method: 'POST',
        body: formData,
        credentials: 'include'
      });
      if (!response.ok) throw new Error('Upload failed');
      const result = await response.json();
      // Optimistically update
      setMaterialsByModule(prev => ({
        ...prev,
        [moduleId]: [...(prev[moduleId] || []), result]
      }));
      // Clear pending state
      setPendingFiles(prev => ({ ...prev, [moduleId]: null }));
      setUploadAnnotations(prev => ({ ...prev, [moduleId]: '' }));
      
      const fileInput = document.getElementById(`file-input-${moduleId}`) as HTMLInputElement;
      if (fileInput) fileInput.value = '';

      alert(`上传成功！`);
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleSaveMaterialAnnotation = async (materialId: number, moduleId: number) => {
    try {
      const response = await fetch(`/api/v1/materials/${materialId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ annotation: materialEditAnnotation })
      });
      if (!response.ok) throw new Error('Failed to update annotation');
      
      const updatedMaterial = await response.json();
      
      // Update local state
      setMaterialsByModule(prev => {
        const moduleMats = prev[moduleId] || [];
        return {
          ...prev,
          [moduleId]: moduleMats.map(m => m.id === materialId ? updatedMaterial : m)
        };
      });
      
      setEditingMaterialId(null);
      setMaterialEditAnnotation('');
    } catch (err: any) {
      alert(err.message);
    }
  };

  const displayModules = selectedCourseId === 'none' 
    ? modules 
    : (selectedCourseId === 'new' ? [] : modules.filter(m => m.course_id === selectedCourseId));

  return (
    <div style={{ fontFamily: 'sans-serif' }}>
      <h1>👨‍🏫 教员工作台 (Instructor Dashboard)</h1>
      {error && <p style={{ color: 'red', padding: '10px', border: '1px solid red' }}>错误: {error}</p>}

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

        {typeof selectedCourseId === 'number' && (
          <div style={{ marginTop: '15px', padding: '15px', border: '1px solid #ccc', backgroundColor: '#fff', borderRadius: '5px' }}>
            {editingCourseId === selectedCourseId ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                <h4>📝 编辑班级信息</h4>
                <input 
                  value={editCourseForm.title || ''} 
                  onChange={e => setEditCourseForm({...editCourseForm, title: e.target.value})} 
                  placeholder="班级名称" 
                  style={{ padding: '8px' }}
                />
                <textarea 
                  value={editCourseForm.description || ''} 
                  onChange={e => setEditCourseForm({...editCourseForm, description: e.target.value})} 
                  placeholder="简介" 
                  style={{ padding: '8px' }}
                />
                <textarea 
                  value={editCourseForm.audience_context || ''} 
                  onChange={e => setEditCourseForm({...editCourseForm, audience_context: e.target.value})} 
                  placeholder="受众" 
                  style={{ padding: '8px' }}
                />
                <div>
                  <button onClick={handleEditCourse} style={{ padding: '6px 12px', background: '#4CAF50', color: '#fff', border: 'none', cursor: 'pointer', borderRadius: '4px' }}>保存 (Save)</button>
                  <button onClick={() => setEditingCourseId(null)} style={{ marginLeft: '10px', padding: '6px 12px' }}>取消 (Cancel)</button>
                </div>
              </div>
            ) : (() => {
              const activeCourse = courses.find(c => c.id === selectedCourseId);
              return activeCourse && (
                <>
                  <h3 style={{ margin: '0 0 10px 0' }}>📘 {activeCourse.title}</h3>
                  <p><strong>简介:</strong> {activeCourse.description || '无'}</p>
                  <p><strong>受众/背景:</strong> {activeCourse.audience_context || '无'}</p>
                  <div style={{ marginTop: '10px' }}>
                    <button onClick={startEditingCourse} style={{ marginRight: '10px', padding: '4px 8px' }}>✏️ 编辑班级 (Edit)</button>
                    <button onClick={() => handleDeleteCourse(activeCourse.id)} style={{ color: 'red', padding: '4px 8px' }}>🗑️ 删除班级 (Delete)</button>
                  </div>
                </>
              );
            })()}
          </div>
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
        <h2>3. 模块列表与资料展示 (Modules in Selection)</h2>
        {displayModules.length === 0 ? <p>当前视图暂无模块</p> : (
          <ul style={{ listStyleType: 'none', padding: 0 }}>
            {displayModules.map(mod => {
              const isEditing = editingModuleId === mod.id;

              return (
                <li key={mod.id} style={{ border: '1px solid #ddd', padding: '15px', marginBottom: '15px', backgroundColor: '#fff' }}>
                  {isEditing ? (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                      <input 
                        value={editForm.title || ''} 
                        onChange={e => setEditForm({...editForm, title: e.target.value})} 
                        placeholder="标题" 
                      />
                      <textarea 
                        value={editForm.description || ''} 
                        onChange={e => setEditForm({...editForm, description: e.target.value})} 
                        placeholder="描述" 
                      />
                      <textarea 
                        value={editForm.learning_objectives || ''} 
                        onChange={e => setEditForm({...editForm, learning_objectives: e.target.value})} 
                        placeholder="学习目标" 
                      />
                      <select 
                        value={editForm.course_id || 'none'} 
                        onChange={e => setEditForm({...editForm, course_id: e.target.value === 'none' ? null : Number(e.target.value)})}
                      >
                        <option value="none">-- 无班级关联 --</option>
                        {courses.map(c => <option key={c.id} value={c.id}>{c.title}</option>)}
                      </select>
                      <div>
                        <button onClick={saveEdit}>保存 (Save)</button>
                        <button onClick={() => setEditingModuleId(null)} style={{ marginLeft: '10px' }}>取消 (Cancel)</button>
                      </div>
                    </div>
                  ) : (
                    <>
                      <h3 style={{ margin: '0 0 10px 0' }}>
                        📄 {mod.title} {mod.course_id ? '(已绑定班级)' : '(孤立)'}
                        <div style={{ float: 'right' }}>
                          <button onClick={() => startEditing(mod)} style={{ marginRight: '5px' }}>编辑 (Edit)</button>
                          <button onClick={() => handleDeleteModule(mod.id)} style={{ color: 'red' }}>删除 (Delete)</button>
                        </div>
                      </h3>
                      <p><small>{mod.description}</small></p>
                      <p><strong>Learning Obj:</strong> {mod.learning_objectives}</p>
                      
                      <div style={{ marginTop: '10px' }}>
                        <strong>已上传资料 (Materials):</strong>
                        {(materialsByModule[mod.id] || []).length === 0 ? (
                          <p style={{ color: '#888', margin: '5px 0' }}>暂无上传的内容</p>
                        ) : (
                          <ul style={{ paddingLeft: '20px' }}>
                            {materialsByModule[mod.id].map(mat => (
                              <li key={mat.id} style={{ marginBottom: '8px' }}>
                                <a href={mat.url} target="_blank" rel="noreferrer" style={{ fontWeight: 'bold', textDecoration: 'none', color: '#1e3a8a' }}>{mat.filename}</a>
                                
                                {editingMaterialId === mat.id ? (
                                  <div style={{ display: 'inline-flex', alignItems: 'center', marginLeft: '10px', gap: '5px' }}>
                                    <input 
                                      type="text"
                                      value={materialEditAnnotation}
                                      onChange={e => setMaterialEditAnnotation(e.target.value)}
                                      placeholder="修改批注"
                                      style={{ padding: '2px 5px' }}
                                    />
                                    <button onClick={() => handleSaveMaterialAnnotation(mat.id, mod.id)} style={{ padding: '2px 8px' }}>保存</button>
                                    <button onClick={() => setEditingMaterialId(null)} style={{ padding: '2px 8px' }}>取消</button>
                                  </div>
                                ) : (
                                  <>
                                    {mat.annotation && <span style={{ marginLeft: '10px', color: '#555', fontStyle: 'italic' }}>- {mat.annotation}</span>}
                                    <button 
                                      onClick={() => {
                                        setEditingMaterialId(mat.id);
                                        setMaterialEditAnnotation(mat.annotation || '');
                                      }}
                                      style={{ marginLeft: '10px', fontSize: '0.8rem', padding: '2px 6px', background: '#eee', border: '1px solid #ccc', cursor: 'pointer' }}
                                    >
                                      ✏️ 修改批注
                                    </button>
                                  </>
                                )}
                              </li>
                            ))}
                          </ul>
                        )}
                      </div>
  
                      <div style={{ marginTop: '15px', padding: '15px', backgroundColor: '#f5f5f5', borderRadius: '5px', border: '1px dashed #ccc' }}>
                        <strong style={{ display: 'block', marginBottom: '10px' }}>⬆️ 暂存/准备上传课程资料:</strong>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                          <input 
                            type="file" 
                            id={`file-input-${mod.id}`}
                            onChange={(e) => {
                              if (e.target.files && e.target.files.length > 0) {
                                setPendingFiles(prev => ({ ...prev, [mod.id]: e.target.files![0] }));
                              } else {
                                setPendingFiles(prev => ({ ...prev, [mod.id]: null }));
                              }
                            }} 
                          />
                          {pendingFiles[mod.id] && (
                            <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
                              <input 
                                type="text" 
                                placeholder="添加资料批注 (可选)" 
                                value={uploadAnnotations[mod.id] || ''}
                                onChange={(e) => setUploadAnnotations(prev => ({ ...prev, [mod.id]: e.target.value }))}
                                style={{ padding: '5px', flex: 1 }}
                              />
                              <button 
                                onClick={() => handleUploadMaterial(mod.id)}
                                style={{ backgroundColor: '#2563eb', color: 'white', border: 'none', padding: '6px 12px', borderRadius: '4px', cursor: 'pointer' }}
                              >
                                确认上传 (Upload)
                              </button>
                            </div>
                          )}
                        </div>
                      </div>
                    </>
                  )}
                </li>
              );
            })}
          </ul>
        )}
      </section>
    </div>
  );
}
