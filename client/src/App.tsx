import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import InstructorModuleDashboard from './pages/InstructorModuleDashboard';
import StudentModuleView from './pages/StudentModuleView';
import Login from './pages/Login';
import Register from './pages/Register';
import ProtectedRoute from './components/ProtectedRoute';
import { AuthProvider, useAuth } from './context/AuthContext';

function Navigation() {
  const { user, isAuthenticated, logout } = useAuth();
  
  const handleToggleDebug = () => {
    const isDebug = localStorage.getItem('DEBUG_STUDENT') === 'true';
    localStorage.setItem('DEBUG_STUDENT', (!isDebug).toString());
    window.location.reload();
  };

  return (
    <nav className="glass-panel sticky top-0 z-50 flex items-center justify-between px-6 py-4 mb-4">
      <div className="flex items-center gap-6">
        <Link to="/" className="text-lg font-bold bg-gradient-to-r from-brand-600 to-green-400 bg-clip-text text-transparent hover:opacity-80 transition-opacity">
          🏠 LearnMateAI
        </Link>
        {/* TODO(Phase 4): Remove this debug toggle when student enrollment logic is completed */}
        <button 
          onClick={handleToggleDebug}
          className={`px-3 py-1.5 text-xs font-medium text-white rounded-md transition-colors shadow-sm ${
            localStorage.getItem('DEBUG_STUDENT') === 'true' 
              ? 'bg-green-500 hover:bg-green-600 ring-2 ring-green-500 ring-offset-1' 
              : 'bg-red-500 hover:bg-red-600'
          }`}
          title="开启后，学生端可绕过权限查看所有模块进行测试"
        >
          🐞 调试: {localStorage.getItem('DEBUG_STUDENT') === 'true' ? 'ON' : 'OFF'}
        </button>
      </div>
      <div className="flex items-center gap-4">
        {isAuthenticated ? (
          <>
            <span className="text-sm font-medium text-slate-600 bg-slate-100 px-3 py-1.5 rounded-full">
              👤 {user?.email} ({user?.role})
            </span>
            <button onClick={logout} className="text-sm font-medium text-slate-500 hover:text-slate-900 transition-colors">
              登出
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="text-sm font-medium text-slate-500 hover:text-brand-600 transition-colors">登录 (Login)</Link>
            <Link to="/register" className="text-sm font-medium px-4 py-2 bg-brand-600 text-white rounded-lg hover:bg-brand-500 transition-colors shadow-sm">注册 (Register)</Link>
          </>
        )}
      </div>
    </nav>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen flex flex-col bg-slate-50">
          <Navigation />          
          <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              
              <Route path="/instructor" element={
                <ProtectedRoute allowedRoles={['instructor']}>
                  <InstructorModuleDashboard />
                </ProtectedRoute>
              } />
              
              <Route path="/student" element={
                <ProtectedRoute allowedRoles={['student']}>
                  <StudentModuleView />
                </ProtectedRoute>
              } />
            </Routes>
          </main>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
