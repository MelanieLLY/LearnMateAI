import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import Home from './pages/Home';
import InstructorModuleDashboard from './pages/InstructorModuleDashboard';
import StudentModuleView from './pages/StudentModuleView';
import QuizTakingView from './pages/QuizTakingView';
import Login from './pages/Login';
import Register from './pages/Register';
import NotFound from './pages/NotFound';
import ProtectedRoute from './components/ProtectedRoute';
import { AuthProvider, useAuth } from './context/AuthContext';

function Navigation() {
  const { user, isAuthenticated, logout } = useAuth();

  return (
    <nav className="glass-panel sticky top-0 z-50 flex items-center justify-between px-6 py-4 mb-4">
      <div className="flex items-center gap-6">
        <Link to="/" className="text-lg font-bold text-black hover:opacity-80 transition-opacity">
          🏠 LearnMateAI
        </Link>
      </div>
      <div className="flex items-center gap-4">
        {isAuthenticated ? (
          <>
            <span className="text-sm font-medium text-slate-600 bg-slate-100 px-3 py-1.5 rounded-full">
              👤 {user?.email} ({user?.role})
            </span>
            <button onClick={logout} className="text-sm font-medium text-slate-500 hover:text-slate-900 transition-colors">
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="text-sm font-medium text-slate-500 hover:text-brand-600 transition-colors">Login</Link>
            <Link to="/register" className="text-sm font-medium px-4 py-2 bg-brand-600 text-white rounded-lg hover:bg-brand-500 transition-colors shadow-sm">Register</Link>
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

              <Route path="/student/quiz/:moduleId" element={
                <ProtectedRoute allowedRoles={['student']}>
                  <QuizTakingView />
                </ProtectedRoute>
              } />

              <Route path="/student/take-quiz/:quizId" element={
                <ProtectedRoute allowedRoles={['student']}>
                  <QuizTakingView />
                </ProtectedRoute>
              } />

              <Route path="/404" element={<NotFound />} />
              <Route path="*" element={<Navigate to="/404" replace />} />
            </Routes>
          </main>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
