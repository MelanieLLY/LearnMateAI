import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <div style={{ marginTop: '20px' }}>
      <h1>欢迎使用 LearnMateAI</h1>
      <p>请选择您的身份登入：</p>

      <div style={{ display: 'flex', gap: '2rem', marginTop: '2rem' }}>
        <Link
          to="/instructor"
          style={{ padding: '1rem 2rem', border: '1px solid #333', borderRadius: '8px', textDecoration: 'none', color: '#333' }}
        >
          <strong>老师Dashboard</strong> <br />
          (Instructor Dashboard)
        </Link>

        <Link
          to="/student"
          style={{ padding: '1rem 2rem', border: '1px solid #333', borderRadius: '8px', textDecoration: 'none', color: '#333' }}
        >
          <strong>学生Dashboard</strong> <br />
          (Student View)
        </Link>
      </div>
    </div>
  );
}
