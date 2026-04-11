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
    <nav style={{ padding: '1rem', borderBottom: '1px solid #ccc', marginBottom: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <Link to="/">🏠 首页 (Home)</Link>
        {/* TODO(Phase 4): Remove this debug toggle when student enrollment logic is completed */}
        <button 
          onClick={handleToggleDebug}
          style={{ 
            padding: '4px 8px', 
            background: localStorage.getItem('DEBUG_STUDENT') === 'true' ? '#4CAF50' : '#f44336', 
            color: 'white', 
            border: 'none', 
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '0.8rem'
          }}
          title="开启后，学生端可绕过权限查看所有模块进行测试"
        >
          🐞 调试：强制查看所有模块 ({localStorage.getItem('DEBUG_STUDENT') === 'true' ? 'ON' : 'OFF'})
        </button>
      </div>
      <div>
        {isAuthenticated ? (
          <>
            <span style={{ marginRight: '10px' }}>👤 {user?.email} ({user?.role})</span>
            <button onClick={logout} style={{ padding: '4px 8px', cursor: 'pointer' }}>登出 Logout</button>
          </>
        ) : (
          <>
            <Link to="/login" style={{ marginRight: '10px' }}>Login</Link>
            <Link to="/register">Register</Link>
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
        <div>
          <Navigation />          
          <main style={{ padding: '0 2rem' }}>
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
