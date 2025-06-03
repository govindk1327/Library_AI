// import { Link, useNavigate } from "react-router-dom";

// export default function Navbar() {
//     const token = localStorage.getItem("token");
//     const navigate = useNavigate();

//     const logout = () => {
//         localStorage.removeItem("token");
//         navigate("/login");
//     };

//     return (
//         <nav className="flex items-center justify-between bg-gray-800 text-white p-4">
//             <h1 className="text-xl font-bold"><Link to="/">📚 AI Library</Link></h1>
//             <div className="space-x-4">
//                 <Link to="/books">Books</Link>
//                 <Link to="/preferences">Preferences</Link>
//                 <Link to="/logs">Logs</Link>
//                 {token ? (
//                     <button onClick={logout} className="ml-4 underline">Logout</button>
//                 ) : (
//                     <>
//                         <Link to="/login">Login</Link>
//                         <Link to="/signup">Signup</Link>
//                     </>
//                 )}
//             </div>
//         </nav>
//     );
// }

import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useUserPrefs } from "../context/UserContext";
import { t } from "../utils/i18n";
import { Menu, X } from "lucide-react";

export default function Navbar() {
    const [open, setOpen] = useState(false);
    const { user, logout } = useUserPrefs();
    const navigate = useNavigate();

    const [lang, setLang] = useState(localStorage.getItem("lang") || "ko");

    useEffect(() => {
        localStorage.setItem("lang", lang);
    }, [lang]);

    const toggleLang = () => {
        const newLang = lang === "ko" ? "en" : "ko";
        setLang(newLang);
        localStorage.setItem("lang", newLang);
        window.location.reload();
    };

    const handleLogout = () => {
        logout();
        navigate("/login");
    };

    return (
        <nav className="bg-gray-950 text-white px-4 py-3 shadow-md fixed w-full top-0 z-50">
            <div className="max-w-6xl mx-auto flex items-center justify-between">
                <Link to="/" className="text-lg font-bold text-indigo-400 flex items-center gap-1">
                    <span role="img" aria-label="logo">📚</span> AI Library
                </Link>

                <div className="md:hidden flex items-center gap-4">
                    <button onClick={toggleLang} className="text-sm bg-gray-800 px-2 py-1 rounded">
                        {lang === "ko" ? "🇺🇸 ENG" : "🇰🇷 한국어"}
                    </button>
                    <button onClick={() => setOpen(!open)} className="focus:outline-none">
                        {open ? <X size={24} /> : <Menu size={24} />}
                    </button>
                </div>

                {/* Desktop menu */}
                <div className="hidden md:flex items-center gap-6">
                    <Link to="/books" className="hover:text-emerald-400">{t(lang, "books")}</Link>
                    <Link to="/preferences" className="hover:text-emerald-400">{t(lang, "preferences")}</Link>
                    <Link to="/history" className="hover:text-emerald-400">{t(lang, "history")}</Link>
                    <button onClick={toggleLang} className="text-sm bg-gray-800 px-2 py-1 rounded">
                        {lang === "ko" ? "🇺🇸 ENG" : "🇰🇷 한국어"}
                    </button>
                    {user ? (
                        <button
                            onClick={handleLogout}
                            className="bg-gray-800 hover:bg-gray-700 text-white px-3 py-1 rounded"
                        >
                            {t(lang, "logout")}
                        </button>
                    ) : (
                        <div className="flex gap-2">
                            <Link to="/login" className="hover:text-blue-400">{t(lang, "login")}</Link>
                            <Link to="/signup" className="hover:text-blue-400">{t(lang, "signup")}</Link>
                        </div>
                    )}
                </div>
            </div>

            {/* Mobile menu */}
            {open && (
                <div className="md:hidden mt-3 space-y-2">
                    <Link to="/books" onClick={() => setOpen(false)} className="block px-4 py-2 hover:bg-gray-800">{t(lang, "books")}</Link>
                    <Link to="/preferences" onClick={() => setOpen(false)} className="block px-4 py-2 hover:bg-gray-800">{t(lang, "preferences")}</Link>
                    <Link to="/logs" onClick={() => setOpen(false)} className="block px-4 py-2 hover:bg-gray-800">{t(lang, "history")}</Link>
                    <button onClick={toggleLang} className="block w-full text-left px-4 py-2 text-sm text-gray-300 hover:bg-gray-800">
                        {lang === "ko" ? "🇺🇸 ENG" : "🇰🇷 한국어"}
                    </button>
                    {user ? (
                        <button
                            onClick={() => { handleLogout(); setOpen(false); }}
                            className="block w-full text-left px-4 py-2 text-red-400 hover:bg-gray-800"
                        >
                            {t(lang, "logout")}
                        </button>
                    ) : (
                        <>
                            <Link to="/login" onClick={() => setOpen(false)} className="block px-4 py-2 hover:bg-gray-800">{t(lang, "login")}</Link>
                            <Link to="/signup" onClick={() => setOpen(false)} className="block px-4 py-2 hover:bg-gray-800">{t(lang, "signup")}</Link>
                        </>
                    )}
                </div>
            )}
        </nav>
    );
}
