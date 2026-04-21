import { useEffect,  useState } from 'react';
import type { FormEvent } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Login() {
  useEffect(() => {
    document.title = 'Login | LearnMateAI';
  }, []);

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const { checkAuth } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password }),
        credentials: 'include'
      });

      if (!response.ok) {
        if (response.status === 502 || response.status === 504 || response.status === 503) {
          throw new Error('☁️ The cloud server is waking up from hibernation (Cold Start). This is common on the free tier. Please wait about 50 seconds and try again!');
        }
        let errorMsg = 'Login failed';
        try {
          const errorData = await response.json();
          errorMsg = errorData.detail || errorMsg;
        } catch {
          errorMsg = `Server error: ${response.status} ${response.statusText}`;
        }
        throw new Error(errorMsg);
      }

      const userData = await response.json();
      await checkAuth(); // Re-fetch the session to set user in Context
      
      if (userData.role === 'student') {
        navigate('/student');
      } else if (userData.role === 'instructor') {
        navigate('/instructor');
      } else {
        navigate('/');
      }
    } catch (error) {
      if (error instanceof TypeError) {
        setError('🚨 Network request failed! If this happens on your first visit, it might be due to a Cold Start timeout on the free backend tier. Please give the server 50 seconds to wake up and try again!');
      } else {
        const err = error as Error;
        setError(err.message);
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-20 p-8 glass-panel rounded-2xl relative overflow-hidden">
      {/* Decorative gradient orb */}
      <div className="absolute -top-10 -right-10 w-32 h-32 bg-brand-500/20 rounded-full blur-3xl pointer-events-none"></div>
      
      <h2 className="text-3xl font-bold text-slate-800 text-center mb-8 relative z-10">
        Login
      </h2>
      
      {error && (
        <div className="bg-red-50 text-red-600 px-4 py-3 rounded-lg mb-6 text-sm flex items-center shadow-sm border border-red-100">
          <span className="mr-2">⚠️</span> {error}
        </div>
      )}
      
      <form onSubmit={handleLogin} className="flex flex-col gap-5 relative z-10">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1.5 ml-1">Email</label>
          <input 
            type="email" 
            value={email} 
            onChange={e => setEmail(e.target.value)} 
            required 
            className="w-full px-4 py-2.5 bg-white border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500/50 focus:border-brand-500 transition-all placeholder:text-slate-400"
            placeholder="you@example.com"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1.5 ml-1">Password</label>
          <input 
            type="password" 
            value={password} 
            onChange={e => setPassword(e.target.value)} 
            required 
            className="w-full px-4 py-2.5 bg-white border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500/50 focus:border-brand-500 transition-all placeholder:text-slate-400"
            placeholder="••••••••"
          />
        </div>
        
        <button 
          type="submit" 
          disabled={isLoading}
          className="mt-2 w-full py-2.5 bg-brand-600 hover:bg-brand-500 text-white font-medium rounded-xl transition-all shadow-md hover:shadow-lg disabled:opacity-70 disabled:cursor-not-allowed transform active:scale-[0.98]"
        >
          {isLoading ? 'Logging in...' : 'Login'}
        </button>
      </form>

      <p className="text-center mt-8 text-sm text-slate-500 relative z-10">
        Don't have an account? <Link to="/register" className="text-brand-600 font-medium hover:text-brand-700 transition-colors">Register</Link>
      </p>
    </div>
  );
}
