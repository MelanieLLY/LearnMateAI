import { Link } from 'react-router-dom';

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center pt-32 pb-32">
      <div className="relative text-center">
        {/* Decorative background element */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-brand-500/10 rounded-full blur-3xl pointer-events-none"></div>
        
        <h1 className="text-8xl font-black bg-gradient-to-br from-brand-400 to-brand-600 bg-clip-text text-transparent mb-4 drop-shadow-sm">
          404
        </h1>
        <h2 className="text-3xl font-bold text-slate-800 mb-6 relative z-10">
          Oops! 页面未找到
        </h2>
        <p className="text-lg text-slate-500 mb-10 max-w-md mx-auto relative z-10">
          您所访问的页面不存在，或者您没有足够的权限访问当前页面。如果你刚切换过身份，系统可能会需要重新认证。
        </p>
        
        <div className="relative z-10 space-y-4 sm:space-y-0 sm:space-x-4">
          <Link 
            to="/" 
            className="inline-block px-8 py-3.5 bg-brand-600 hover:bg-brand-500 text-white font-semibold rounded-xl transition-all shadow-lg hover:shadow-brand-500/30 transform hover:-translate-y-0.5 active:scale-95"
          >
            返回主页 (Go Home)
          </Link>
          <Link 
            to="/login" 
            className="inline-block px-8 py-3.5 bg-white text-slate-700 font-semibold rounded-xl border border-slate-200 hover:border-brand-300 hover:bg-brand-50 transition-all shadow-sm transform hover:-translate-y-0.5 active:scale-95"
          >
            重新登录 (Re-Login)
          </Link>
        </div>
      </div>
    </div>
  );
}
