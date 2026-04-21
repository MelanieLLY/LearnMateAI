import { useState } from 'react';
import type { FormEvent } from 'react';
import { useNavigate, Link } from 'react-router-dom';

export default function Register() {
  const [email, setEmail] = useState('');
  const [fullName, setFullName] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState<'student' | 'instructor'>('student');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const navigate = useNavigate();

  const handleRegister = async (e: FormEvent) => {
    e.preventDefault();
    if (password.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }

    setError('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/v1/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, full_name: fullName, password, role }),
        // Registration does not require credentials for session but good practice
        credentials: 'omit' 
      });

      if (!response.ok) {
        if (response.status === 502 || response.status === 504 || response.status === 503) {
          throw new Error('☁️ The cloud server is waking up from hibernation (Cold Start). This is common on the free tier. Please wait about 50 seconds and try again!');
        }
        let errorMsg = 'Registration failed';
        try {
          const errorData = await response.json();
          errorMsg = errorData.detail || errorMsg;
        } catch {
          errorMsg = `Server error: ${response.status} ${response.statusText}`;
        }
        throw new Error(errorMsg);
      }

      // Automatically redirect to login page upon success
      navigate('/login');
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
      <div className="absolute -top-10 -right-10 w-32 h-32 bg-green-500/20 rounded-full blur-3xl pointer-events-none"></div>

      <h2 className="text-3xl font-bold text-slate-800 text-center mb-8 relative z-10">
        Register Account
      </h2>
      
      {error && (
        <div className="bg-red-50 text-red-600 px-4 py-3 rounded-lg mb-6 text-sm flex items-center shadow-sm border border-red-100">
          <span className="mr-2">⚠️</span> {error}
        </div>
      )}
      
      <form onSubmit={handleRegister} className="flex flex-col gap-5 relative z-10">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1.5 ml-1">Full Name</label>
          <input 
            type="text" 
            value={fullName} 
            onChange={e => setFullName(e.target.value)} 
            required 
            className="w-full px-4 py-2.5 bg-white border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500/50 focus:border-green-500 transition-all placeholder:text-slate-400"
            placeholder="John Doe"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1.5 ml-1">Email</label>
          <input 
            type="email" 
            value={email} 
            onChange={e => setEmail(e.target.value)} 
            required 
            className="w-full px-4 py-2.5 bg-white border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500/50 focus:border-green-500 transition-all placeholder:text-slate-400"
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
            className="w-full px-4 py-2.5 bg-white border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500/50 focus:border-green-500 transition-all placeholder:text-slate-400"
            placeholder="At least 6 characters"
          />
        </div>
        
        <div className="flex flex-col sm:flex-row gap-4 mt-2">
          <label className={`flex-1 border rounded-xl p-3 cursor-pointer transition-all flex items-center justify-center gap-2 ${role === 'student' ? 'border-brand-500 bg-brand-50/50 ring-1 ring-brand-500' : 'border-slate-200 hover:bg-slate-50'}`}>
            <input 
              type="radio" 
              name="role" 
              value="student" 
              checked={role === 'student'} 
              onChange={() => setRole('student')} 
              className="hidden"
            /> 
            <span className="text-xl">🎓</span>
            <span className="font-medium text-slate-800 text-sm">I am a student</span>
          </label>
          <label className={`flex-1 border rounded-xl p-3 cursor-pointer transition-all flex items-center justify-center gap-2 ${role === 'instructor' ? 'border-blue-500 bg-blue-50/50 ring-1 ring-blue-500' : 'border-slate-200 hover:bg-slate-50'}`}>
            <input 
              type="radio" 
              name="role" 
              value="instructor" 
              checked={role === 'instructor'} 
              onChange={() => setRole('instructor')} 
              className="hidden"
            /> 
            <span className="text-xl">👨‍🏫</span>
            <span className="font-medium text-slate-800 text-sm">I am an instructor</span>
          </label>
        </div>
        
        <button 
          type="submit" 
          disabled={isLoading}
          className="mt-4 w-full py-2.5 bg-brand-600 hover:bg-brand-500 text-white font-medium rounded-xl transition-all shadow-md hover:shadow-lg disabled:opacity-70 disabled:cursor-not-allowed transform active:scale-[0.98]"
        >
          {isLoading ? 'Registering...' : 'Register'}
        </button>
      </form>

      <p className="text-center mt-8 text-sm text-slate-500 relative z-10">
        Already have an account? <Link to="/login" className="text-brand-600 font-medium hover:text-brand-700 transition-colors">Login</Link>
      </p>
    </div>
  );
}
