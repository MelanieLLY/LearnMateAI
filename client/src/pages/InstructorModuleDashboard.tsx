import { useState, useEffect } from 'react';
import type { FormEvent } from 'react';
import InstructorQuizSection from '../components/InstructorQuizSection';

interface Course {
  id: number;
  title: string;
  description: string;
  audience_context: string | null;
}

interface StudentUser {
  id: number;
  email: string;
  full_name: string;
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

interface ModuleStat {
  module_name: string;
  average_score: number;
  completion_rate: number;
}

interface CourseReportResponse {
  overall_average: number;
  total_students: number;
  common_gaps: string[];
  module_stats: ModuleStat[];
}

export default function InstructorModuleDashboard() {
  const [modules, setModules] = useState<Module[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [materialsByModule, setMaterialsByModule] = useState<Record<number, Material[]>>({});
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

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

  // Course Students State
  const [courseStudents, setCourseStudents] = useState<StudentUser[]>([]);

  // Course Report State
  const [courseReport, setCourseReport] = useState<CourseReportResponse | null>(null);
  const [isReportLoading, setIsReportLoading] = useState(false);

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
        } catch {
          // Ignore failures
        }
      }));
      setMaterialsByModule(matsMap);
    } catch (error) {
      const err = error as Error;
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  useEffect(() => {
    if (typeof selectedCourseId === 'number') {
      fetch(`/api/v1/courses/${selectedCourseId}/students`, { credentials: 'include' })
        .then(res => res.ok ? res.json() : [])
        .then(data => setCourseStudents(data))
        .catch(() => setCourseStudents([]));

      setIsReportLoading(true);
      fetch(`/api/v1/courses/${selectedCourseId}/report`, { credentials: 'include' })
        .then(res => res.ok ? res.json() : null)
        .then(data => setCourseReport(data))
        .catch(() => setCourseReport(null))
        .finally(() => setIsReportLoading(false));
    } else {
      setCourseStudents([]);
      setCourseReport(null);
    }
  }, [selectedCourseId]);

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
    } catch (error) {
      const err = error as Error;
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
    } catch (error) {
      const err = error as Error;
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
    } catch (error) {
      const err = error as Error;
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
    } catch (error) {
      const err = error as Error;
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
    } catch (error) {
      const err = error as Error;
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
    } catch (error) {
      const err = error as Error;
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
    } catch (error) {
      const err = error as Error;
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
    } catch (error) {
      const err = error as Error;
      alert(err.message);
    }
  };

  const displayModules = selectedCourseId === 'none' 
    ? modules 
    : (selectedCourseId === 'new' ? [] : modules.filter(m => m.course_id === selectedCourseId));

  return (
    <div className="max-w-6xl mx-auto space-y-8 pb-12">
      <header className="mb-8 pl-2">
        <h1 className="text-3xl font-extrabold text-slate-800 mb-2">👨‍🏫 教员工作台 (Instructor Dashboard)</h1>
        <p className="text-slate-500">管理您的课程、模块，并上传教学资料。</p>
      </header>
      
      {error && (
        <div className="bg-red-50 text-red-600 px-4 py-3 rounded-xl mb-6 text-sm flex items-center shadow-sm border border-red-100">
          <span className="mr-2">⚠️</span> 错误: {error}
        </div>
      )}

      {isLoading ? (
        <div className="space-y-6">
          <div className="glass-panel p-6 rounded-2xl animate-pulse h-48 bg-slate-100"></div>
          <div className="glass-panel p-6 rounded-2xl animate-pulse h-48 bg-slate-100"></div>
          <div className="glass-panel p-6 rounded-2xl animate-pulse h-64 bg-slate-100"></div>
        </div>
      ) : (
        <>
          <section className="glass-panel p-6 sm:p-8 rounded-2xl hover:shadow-xl transition-shadow">
            <h2 className="text-xl font-bold text-slate-800 mb-6 flex items-center gap-2">
              <span className="bg-brand-100 text-brand-600 rounded-full w-8 h-8 flex items-center justify-center text-sm">1</span>
              选择班级上下文 (Global Class Context)
            </h2>
            <div className="mb-6 flex flex-col sm:flex-row sm:items-center gap-3">
              <strong className="text-slate-700 whitespace-nowrap">当前操作班级：</strong>
              <select 
                value={selectedCourseId} 
                onChange={(e) => setSelectedCourseId(e.target.value === 'none' || e.target.value === 'new' ? e.target.value : Number(e.target.value))}
                className="w-full sm:max-w-md px-4 py-2 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500/50 bg-white shadow-sm"
              >
                <option value="none">-- 游荡模块 / 全部 (Orphan Modules / All) --</option>
                {courses.map(c => <option key={c.id} value={c.id}>📚 {c.title}</option>)}
                <option value="new">➕ 新建一个班级 (Create New Class)...</option>
              </select>
            </div>

            {selectedCourseId === 'new' && (
              <form onSubmit={handleCreateCourse} className="flex flex-col gap-4 p-5 border border-brand-200 bg-brand-50/30 rounded-xl shadow-sm mt-4">
                <h4 className="font-semibold text-brand-800">快速创建班级</h4>
                <input 
                  required 
                  placeholder="班级名称 (Class Name)" 
                  value={courseTitle} 
                  onChange={e => setCourseTitle(e.target.value)} 
                  className="px-4 py-2 bg-white border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500/50"
                />
                <textarea 
                  placeholder="班级介绍 (Description)" 
                  value={courseDesc} 
                  onChange={e => setCourseDesc(e.target.value)} 
                  className="px-4 py-2 bg-white border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500/50 min-h-[80px]"
                />
                <textarea 
                  placeholder="受众背景/情感敏感度 (Audience Context)" 
                  value={courseAudience} 
                  onChange={e => setCourseAudience(e.target.value)} 
                  className="px-4 py-2 bg-white border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500/50 min-h-[80px]"
                />
                <button type="submit" className="py-2.5 bg-brand-600 hover:bg-brand-500 text-white font-medium rounded-xl transition-all shadow-sm">
                  创建并选中班级
                </button>
              </form>
            )}

            {typeof selectedCourseId === 'number' && (
              <div className="mt-6 p-6 border border-slate-200 bg-slate-50/50 rounded-xl">
                {editingCourseId === selectedCourseId ? (
                  <div className="flex flex-col gap-4">
                    <h4 className="font-semibold text-slate-800 flex items-center gap-2">📝 编辑班级信息</h4>
                    <input 
                      value={editCourseForm.title || ''} 
                      onChange={e => setEditCourseForm({...editCourseForm, title: e.target.value})} 
                      placeholder="班级名称" 
                      className="px-4 py-2 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-brand-500/50 outline-none"
                    />
                    <textarea 
                      value={editCourseForm.description || ''} 
                      onChange={e => setEditCourseForm({...editCourseForm, description: e.target.value})} 
                      placeholder="简介" 
                      className="px-4 py-2 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-brand-500/50 outline-none"
                    />
                    <textarea 
                      value={editCourseForm.audience_context || ''} 
                      onChange={e => setEditCourseForm({...editCourseForm, audience_context: e.target.value})} 
                      placeholder="受众" 
                      className="px-4 py-2 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-brand-500/50 outline-none"
                    />
                    <div className="flex gap-3 mt-2">
                      <button onClick={handleEditCourse} className="px-5 py-2 bg-green-500 hover:bg-green-600 text-white font-medium rounded-lg transition-colors">
                        保存 (Save)
                      </button>
                      <button onClick={() => setEditingCourseId(null)} className="px-5 py-2 bg-slate-200 hover:bg-slate-300 text-slate-700 font-medium rounded-lg transition-colors">
                        取消 (Cancel)
                      </button>
                    </div>
                  </div>
                ) : (() => {
                  const activeCourse = courses.find(c => c.id === selectedCourseId);
                  return activeCourse && (
                    <>
                      <h3 className="text-xl font-bold text-slate-800 mb-3">📘 {activeCourse.title}</h3>
                      <div className="space-y-2 mb-6">
                        <p className="text-slate-600"><strong className="text-slate-800">简介:</strong> {activeCourse.description || '无'}</p>
                        <p className="text-slate-600"><strong className="text-slate-800">受众/背景:</strong> {activeCourse.audience_context || '无'}</p>
                        <div className="text-slate-600">
                          <strong className="text-slate-800 block mb-1 mt-2">已加入本班级的学生:</strong>
                          {courseStudents.length === 0 ? <span className="text-sm italic">暂无学生选修此课</span> : (
                            <div className="flex flex-wrap gap-2 mt-1">
                              {courseStudents.map(s => (
                                <span key={s.id} className="bg-emerald-50 text-emerald-700 border border-emerald-200 px-2 py-1 rounded-md text-sm font-medium">
                                  👤 {s.full_name} <span className="text-emerald-500 font-normal">({s.email})</span>
                                </span>
                              ))}
                            </div>
                          )}
                        </div>
                      </div>
                      <div className="flex gap-3">
                        <button onClick={startEditingCourse} className="px-4 py-2 border border-slate-300 rounded-lg hover:bg-slate-100 text-slate-700 transition-colors text-sm font-medium">
                          ✏️ 编辑班级 (Edit)
                        </button>
                        <button onClick={() => handleDeleteCourse(activeCourse.id)} className="px-4 py-2 border border-red-200 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition-colors text-sm font-medium">
                          🗑️ 删除班级 (Delete)
                        </button>
                      </div>
                    </>
                  );
                })()}
              </div>
            )}
          </section>

          {typeof selectedCourseId === 'number' && courseReport && (
            <section className="glass-panel p-6 sm:p-8 rounded-2xl hover:shadow-xl transition-shadow bg-gradient-to-br from-white to-slate-50/50">
              <h2 className="text-xl font-bold text-slate-800 mb-2 flex items-center gap-2">
                <span className="text-brand-500 text-2xl">📊</span>
                班级学情诊断报告 (Class Performance)
              </h2>
              <p className="text-slate-500 text-sm mb-6 flex items-center gap-1.5">
                <span className="text-brand-400">ℹ️</span> 评分统计包含 <strong>Instructor-assigned Quiz</strong> (随堂测试) 与 <strong>AI-generated Self-practice</strong> (自主练习) 成绩。
              </p>
              {isReportLoading ? (
                <div className="animate-pulse flex space-x-4">
                  <div className="flex-1 space-y-4 py-1">
                    <div className="h-4 bg-slate-200 rounded w-3/4"></div>
                    <div className="space-y-2">
                      <div className="h-4 bg-slate-200 rounded"></div>
                      <div className="h-4 bg-slate-200 rounded w-5/6"></div>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="space-y-8">
                  {/* Summary Cards */}
                  <div className="grid grid-cols-2 gap-4">
                    <div className="p-5 rounded-2xl bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-100/50 shadow-sm flex flex-col justify-center items-center">
                      <p className="text-sm text-slate-500 font-medium mb-1">班级平均分</p>
                      <p className="text-4xl font-black text-indigo-600">{courseReport.overall_average}</p>
                    </div>
                    <div className="p-5 rounded-2xl bg-gradient-to-br from-emerald-50 to-teal-50 border border-emerald-100/50 shadow-sm flex flex-col justify-center items-center">
                      <p className="text-sm text-slate-500 font-medium mb-1">已接入学生数</p>
                      <p className="text-4xl font-black text-teal-600">{courseReport.total_students}</p>
                    </div>
                  </div>
                  
                  {/* Common Gaps */}
                  <div>
                    <h3 className="text-sm font-bold text-slate-700 mb-3 uppercase tracking-wider">⚠️ 高频易错点 (Common Gaps)</h3>
                    <div className="flex flex-wrap gap-2">
                      {courseReport.common_gaps.length > 0 ? courseReport.common_gaps.map((gap, idx) => (
                        <span key={idx} className="bg-red-50 text-red-700 border border-red-200 px-3 py-1.5 rounded-lg text-sm font-semibold shadow-sm">
                          {gap}
                        </span>
                      )) : (
                        <span className="text-slate-400 text-sm italic">暂无足够数据分析易错点</span>
                      )}
                    </div>
                  </div>

                  {/* Module Stats Progress */}
                  <div>
                    <h3 className="text-sm font-bold text-slate-700 mb-4 uppercase tracking-wider">📈 各模块掌握进度 (Module Mastery)</h3>
                    <div className="space-y-4">
                      {courseReport.module_stats.length > 0 ? courseReport.module_stats.map((mod, idx) => (
                        <div key={idx} className="flex flex-col gap-1.5">
                          <div className="flex justify-between items-end text-sm">
                            <span className="font-medium text-slate-700">{mod.module_name}</span>
                            <span className="font-bold text-slate-600">{mod.average_score} 分</span>
                          </div>
                          <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
                            <div 
                              className={`h-full rounded-full transition-all duration-1000 ${mod.average_score >= 85 ? 'bg-emerald-500' : mod.average_score >= 75 ? 'bg-amber-400' : 'bg-red-400'}`}
                              style={{ width: `${mod.average_score}%` }}
                            ></div>
                          </div>
                        </div>
                      )) : (
                        <span className="text-slate-400 text-sm italic">暂无模块进度数据</span>
                      )}
                    </div>
                  </div>
                </div>
              )}
            </section>
          )}

          <section className="glass-panel p-6 sm:p-8 rounded-2xl hover:shadow-xl transition-shadow">
            <h2 className="text-xl font-bold text-slate-800 mb-6 flex items-center gap-2">
              <span className="bg-brand-100 text-brand-600 rounded-full w-8 h-8 flex items-center justify-center text-sm">2</span>
              在当前上下文中创建模块 (Create Module)
            </h2>
            <form onSubmit={handleCreateModule} className="flex flex-col gap-4">
              <input 
                required 
                placeholder="模块标题 (Title)" 
                value={title} 
                onChange={e => setTitle(e.target.value)} 
                className="px-4 py-2.5 bg-white border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500/50"
              />
              <textarea 
                placeholder="基本描述 (Description)" 
                value={description} 
                onChange={e => setDescription(e.target.value)} 
                className="px-4 py-2.5 bg-white border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500/50 min-h-[80px]"
              />
              <textarea 
                placeholder="当前模块具体学习目标 (Learning Objectives)" 
                value={objectives} 
                onChange={e => setObjectives(e.target.value)} 
                className="px-4 py-2.5 bg-white border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500/50 min-h-[80px]"
              />
              <button 
                type="submit" 
                disabled={selectedCourseId === 'new'}
                className="py-3 bg-brand-600 hover:bg-brand-500 text-white font-medium rounded-xl transition-all shadow-md disabled:bg-slate-300 disabled:cursor-not-allowed"
              >
                ➕ {typeof selectedCourseId === 'number' ? '为选中的班级添加模块' : '创建孤立模块'}
              </button>
            </form>
          </section>

          <section className="glass-panel p-6 sm:p-8 rounded-2xl hover:shadow-xl transition-shadow">
            <h2 className="text-xl font-bold text-slate-800 mb-6 flex items-center gap-2">
              <span className="bg-brand-100 text-brand-600 rounded-full w-8 h-8 flex items-center justify-center text-sm">3</span>
              模块列表与资料展示 (Modules in Selection)
            </h2>
            {displayModules.length === 0 ? (
              <div className="text-center py-12 border-2 border-dashed border-slate-200 rounded-2xl bg-slate-50/50">
                <p className="text-slate-500">当前视图暂无模块</p>
              </div>
            ) : (
              <ul className="space-y-6">
                {displayModules.map(mod => {
                  const isEditing = editingModuleId === mod.id;

                  return (
                    <li key={mod.id} className="border border-slate-200 bg-white p-6 rounded-2xl shadow-sm hover:border-brand-300 hover:shadow-md transition-all">
                      {isEditing ? (
                        <div className="flex flex-col gap-4">
                          <input 
                            value={editForm.title || ''} 
                            onChange={e => setEditForm({...editForm, title: e.target.value})} 
                            placeholder="标题" 
                            className="px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-brand-500/50 outline-none"
                          />
                          <textarea 
                            value={editForm.description || ''} 
                            onChange={e => setEditForm({...editForm, description: e.target.value})} 
                            placeholder="描述" 
                            className="px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-brand-500/50 outline-none"
                          />
                          <textarea 
                            value={editForm.learning_objectives || ''} 
                            onChange={e => setEditForm({...editForm, learning_objectives: e.target.value})} 
                            placeholder="学习目标" 
                            className="px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-brand-500/50 outline-none"
                          />
                          <select 
                            value={editForm.course_id || 'none'} 
                            onChange={e => setEditForm({...editForm, course_id: e.target.value === 'none' ? null : Number(e.target.value)})}
                            className="px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-brand-500/50 outline-none w-full max-w-sm"
                          >
                            <option value="none">-- 无班级关联 --</option>
                            {courses.map(c => <option key={c.id} value={c.id}>{c.title}</option>)}
                          </select>
                          <div className="flex gap-3 mt-2">
                            <button onClick={saveEdit} className="px-5 py-2 bg-brand-600 hover:bg-brand-500 text-white font-medium rounded-lg">保存 (Save)</button>
                            <button onClick={() => setEditingModuleId(null)} className="px-5 py-2 bg-slate-200 hover:bg-slate-300 text-slate-700 font-medium rounded-lg">取消 (Cancel)</button>
                          </div>
                        </div>
                      ) : (
                        <>
                          <div className="flex flex-wrap items-start justify-between gap-4 mb-4">
                            <h3 className="text-xl font-bold text-slate-800 flex items-center gap-2">
                              <span className="text-brand-500">📄</span> {mod.title}
                              <span className="text-xs font-medium bg-slate-100 text-slate-500 px-2 py-1 rounded-full whitespace-nowrap">
                                {mod.course_id ? '已绑定班级' : '孤立模块'}
                              </span>
                            </h3>
                            <div className="flex gap-2 shrink-0">
                              <button onClick={() => startEditing(mod)} className="px-3 py-1.5 text-sm border border-slate-300 rounded hover:bg-slate-50 text-slate-600 transition-colors">
                                编辑
                              </button>
                              <button onClick={() => handleDeleteModule(mod.id)} className="px-3 py-1.5 text-sm border border-red-200 bg-red-50 text-red-600 rounded hover:bg-red-100 transition-colors">
                                删除
                              </button>
                            </div>
                          </div>
                          <p className="text-slate-600 mb-3">{mod.description}</p>
                          {mod.learning_objectives && (
                            <div className="bg-slate-50 border border-slate-100 p-3 rounded-lg mb-4 text-sm">
                              <strong className="text-slate-700">Learning Obj:</strong> <span className="text-slate-600">{mod.learning_objectives}</span>
                            </div>
                          )}
                          
                          <div className="mt-6 border-t border-slate-100 pt-4">
                            <h4 className="font-semibold text-slate-800 mb-3">已上传资料 (Materials):</h4>
                            {(materialsByModule[mod.id] || []).length === 0 ? (
                              <p className="text-slate-400 text-sm italic">暂无上传的内容</p>
                            ) : (
                              <ul className="space-y-2">
                                {materialsByModule[mod.id].map(mat => (
                                  <li key={mat.id} className="flex flex-wrap items-center gap-3 p-3 bg-slate-50 rounded-lg border border-slate-100 group">
                                    <a href={mat.url} target="_blank" rel="noreferrer" className="font-medium text-brand-600 hover:text-brand-700 hover:underline">
                                      🔗 {mat.filename}
                                    </a>
                                    
                                    {editingMaterialId === mat.id ? (
                                      <div className="flex items-center gap-2 flex-wrap ml-auto">
                                        <input 
                                          type="text"
                                          value={materialEditAnnotation}
                                          onChange={e => setMaterialEditAnnotation(e.target.value)}
                                          placeholder="修改批注"
                                          className="px-2 py-1 text-sm border border-brand-300 rounded focus:outline-none focus:ring-1 focus:ring-brand-500"
                                        />
                                        <button onClick={() => handleSaveMaterialAnnotation(mat.id, mod.id)} className="px-3 py-1 text-xs bg-brand-500 text-white rounded hover:bg-brand-600">保存</button>
                                        <button onClick={() => setEditingMaterialId(null)} className="px-3 py-1 text-xs bg-slate-200 text-slate-700 rounded hover:bg-slate-300">取消</button>
                                      </div>
                                    ) : (
                                      <div className="flex items-center gap-3 ml-auto">
                                        {mat.annotation && <span className="text-sm text-slate-500 italic bg-white px-2 py-0.5 rounded border border-slate-100">📝 {mat.annotation}</span>}
                                        <button 
                                          onClick={() => {
                                            setEditingMaterialId(mat.id);
                                            setMaterialEditAnnotation(mat.annotation || '');
                                          }}
                                          className="text-xs px-2 py-1 bg-white border border-slate-200 rounded text-slate-500 hover:bg-slate-50 hover:text-brand-600 opacity-0 group-hover:opacity-100 transition-opacity"
                                        >
                                          ✏️
                                        </button>
                                      </div>
                                    )}
                                  </li>
                                ))}
                              </ul>
                            )}
                          </div>
      
                          <div className="mt-6 bg-brand-50/30 p-5 rounded-xl border border-brand-100">
                            <h4 className="font-semibold text-brand-800 mb-4 flex items-center gap-2">
                              <span>⬆️</span> 暂存/准备上传课程资料
                            </h4>
                            <div className="flex flex-col gap-4">
                              <input 
                                type="file" 
                                id={`file-input-${mod.id}`}
                                className="block w-full text-sm text-slate-500 file:mr-4 file:py-2.5 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-brand-50 file:text-brand-700 hover:file:bg-brand-100 transition-colors border border-dashed border-slate-300 rounded-lg p-2 bg-white"
                                onChange={(e) => {
                                  if (e.target.files && e.target.files.length > 0) {
                                    setPendingFiles(prev => ({ ...prev, [mod.id]: e.target.files![0] }));
                                  } else {
                                    setPendingFiles(prev => ({ ...prev, [mod.id]: null }));
                                  }
                                }} 
                              />
                              {pendingFiles[mod.id] && (
                                <div className="flex flex-col sm:flex-row gap-3">
                                  <input 
                                    type="text" 
                                    placeholder="添加资料批注 (可选)" 
                                    value={uploadAnnotations[mod.id] || ''}
                                    onChange={(e) => setUploadAnnotations(prev => ({ ...prev, [mod.id]: e.target.value }))}
                                    className="px-4 py-2.5 border border-slate-200 rounded-lg focus:ring-2 focus:ring-brand-500/50 outline-none flex-1 bg-white"
                                  />
                                  <button 
                                    onClick={() => handleUploadMaterial(mod.id)}
                                    className="px-6 py-2.5 bg-blue-600 hover:bg-blue-500 text-white font-medium rounded-lg transition-all shadow-sm shrink-0"
                                  >
                                    确认上传 (Upload)
                                  </button>
                                </div>
                              )}
                            </div>
                          </div>

                          <InstructorQuizSection moduleId={mod.id} />
                    </>
                  )}
                </li>
              );
            })}
          </ul>
        )}
          </section>
        </>
      )}
    </div>
  );
}
