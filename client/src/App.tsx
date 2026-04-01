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
  
  return (
    <nav style={{ padding: '1rem', borderBottom: '1px solid #ccc', marginBottom: '1rem', display: 'flex', justifyContent: 'space-between' }}>
      <div>
        <Link to="/" style={{ marginRight: '1rem' }}>🏠 首页 (Home)</Link>
        {isAuthenticated && user?.role === 'instructor' && (
          <Link to="/instructor" style={{ marginRight: '1rem' }}>👨‍🏫 教师端</Link>
        )}
        {isAuthenticated && user?.role === 'student' && (
          <Link to="/student">🎓 学生端</Link>
        )}
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
