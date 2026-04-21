import { Link, Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Home() {
  const { user, isAuthenticated } = useAuth();

  // If already logged in, redirect directly to the corresponding dashboard.
  if (isAuthenticated && user) {
    if (user.role === 'student') {
      return <Navigate to="/student" replace />;
    } else if (user.role === 'instructor') {
      return <Navigate to="/instructor" replace />;
    }
  }

  return (
    <div className="flex flex-col items-center justify-center pt-20 pb-32">
      <div className="text-center max-w-3xl mb-16">
        <h1 className="text-5xl font-extrabold tracking-tight text-slate-900 mb-6 bg-gradient-to-r from-brand-600 to-green-500 bg-clip-text text-transparent">
          Welcome to LearnMateAI
        </h1>
        <p className="text-xl text-slate-500">
          Please select your role to log in and start a brand new learning and teaching experience.
        </p>
      </div>

      <div className="flex flex-col sm:flex-row gap-6 w-full max-w-2xl px-4">
        <Link
          to="/instructor"
          className="flex-1 glass-panel flex flex-col items-center justify-center p-8 rounded-2xl hover:-translate-y-1 hover:shadow-xl hover:border-brand-500/30 transition-all duration-300 group"
        >
          <div className="w-16 h-16 bg-blue-50 text-blue-500 rounded-full flex items-center justify-center text-2xl mb-4 group-hover:scale-110 transition-transform">
            👨‍🏫
          </div>
          <strong className="text-xl text-slate-800 mb-1">Instructor Dashboard</strong>
          <span className="text-sm text-slate-500">(For Teachers)</span>
        </Link>

        <Link
          to="/student"
          className="flex-1 glass-panel flex flex-col items-center justify-center p-8 rounded-2xl hover:-translate-y-1 hover:shadow-xl hover:border-brand-500/30 transition-all duration-300 group"
        >
          <div className="w-16 h-16 bg-green-50 text-green-500 rounded-full flex items-center justify-center text-2xl mb-4 group-hover:scale-110 transition-transform">
            👨‍🎓
          </div>
          <strong className="text-xl text-slate-800 mb-1">Student Dashboard</strong>
          <span className="text-sm text-slate-500">(For Students)</span>
        </Link>
      </div>
    </div>
  );
}
