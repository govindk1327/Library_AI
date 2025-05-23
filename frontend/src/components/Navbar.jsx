import { Link, useNavigate } from "react-router-dom";

export default function Navbar() {
    const token = localStorage.getItem("token");
    const navigate = useNavigate();

    const logout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };

    return (
        <nav className="flex items-center justify-between bg-gray-800 text-white p-4">
            <h1 className="text-xl font-bold"><Link to="/">📚 AI Library</Link></h1>
            <div className="space-x-4">
                <Link to="/books">Books</Link>
                <Link to="/preferences">Preferences</Link>
                <Link to="/logs">Logs</Link>
                {token ? (
                    <button onClick={logout} className="ml-4 underline">Logout</button>
                ) : (
                    <>
                        <Link to="/login">Login</Link>
                        <Link to="/signup">Signup</Link>
                    </>
                )}
            </div>
        </nav>
    );
}
