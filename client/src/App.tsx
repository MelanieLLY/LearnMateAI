import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import InstructorModuleDashboard from './pages/InstructorModuleDashboard';
import StudentModuleView from './pages/StudentModuleView';

function App() {
  return (
    <Router>
      <div>
        <nav style={{ padding: '1rem', borderBottom: '1px solid #ccc', marginBottom: '1rem' }}>
          <Link to="/" style={{ marginRight: '1rem' }}>🏠 首页 (Home)</Link>
          <Link to="/instructor" style={{ marginRight: '1rem' }}>👨‍🏫 教师端</Link>
          <Link to="/student">🎓 学生端</Link>
        </nav>
        
        <main style={{ padding: '0 2rem' }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/instructor" element={<InstructorModuleDashboard />} />
            <Route path="/student" element={<StudentModuleView />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
