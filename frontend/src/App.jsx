import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import RecommendPage from './pages/RecommendPage';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import BooksPage from './pages/BooksPage';
import PreferencesPage from './pages/PreferencesPage';
import HistoryPages from './pages/HistoryPages';
import Navbar from './components/Navbar';

export default function App() {
  return (
    <Router>
      <div className="min-h-screen w-full bg-[#0d0d0d] text-white font-sans">
        <Navbar />
        <Routes>
          <Route path="/" element={<RecommendPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route path="/books" element={<BooksPage />} />
          <Route path="/preferences" element={<PreferencesPage />} />
          <Route path="/history" element={<HistoryPages />} />

        </Routes>
      </div>
    </Router>
  );
}
