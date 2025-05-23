import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import RecommendPage from './pages/RecommendPage';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import BooksPage from './pages/BooksPage';
import PreferencesPage from './pages/PreferencesPage';
import LogsPages from './pages/LogsPages';
import Navbar from './components/Navbar';

export default function App() {
  return (
    <Router>
      <Navbar />
      <div className="p-4">
        <Routes>
          <Route path="/" element={<RecommendPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route path="/books" element={<BooksPage />} />
          <Route path="/preferences" element={<PreferencesPage />} />
          <Route path="/logs" element={<LogsPages />} />
        </Routes>
      </div>
    </Router>
  );
}
