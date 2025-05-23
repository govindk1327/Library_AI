import { useState } from "react";
import { useNavigate } from "react-router-dom";
import client from "../api/client";

export default function LoginPage() {
    const [form, setForm] = useState({ username: "", password: "" });
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await client.post("/login/", form);
            localStorage.setItem("token", res.data.token);
            navigate("/");
        } catch {
            setError("Invalid credentials");
        }
    };

    return (
        <div className="max-w-md mx-auto mt-10 p-4 bg-white shadow rounded">
            <h2 className="text-2xl font-bold mb-4">Login</h2>
            <form onSubmit={handleSubmit} className="space-y-3">
                <input
                    className="w-full border p-2"
                    placeholder="Username"
                    value={form.username}
                    onChange={(e) => setForm({ ...form, username: e.target.value })}
                />
                <input
                    className="w-full border p-2"
                    placeholder="Password"
                    type="password"
                    value={form.password}
                    onChange={(e) => setForm({ ...form, password: e.target.value })}
                />
                {error && <div className="text-red-500">{error}</div>}
                <button className="w-full bg-blue-600 text-white p-2 rounded">Log In</button>
            </form>
        </div>
    );
}
