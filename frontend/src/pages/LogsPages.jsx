import { useEffect, useState } from "react";
import client from "../api/client";

export default function LogsPage() {
    const [logs, setLogs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchLogs = async () => {
            try {
                const res = await client.get("/logs/");
                setLogs(res.data);
            } catch {
                setError("❌ Failed to load logs.");
            } finally {
                setLoading(false);
            }
        };
        fetchLogs();
    }, []);

    return (
        <div className="max-w-4xl mx-auto mt-10">
            <h2 className="text-2xl font-bold mb-4">🧾 Your Prompt Logs</h2>

            {loading && <p>⏳ Loading...</p>}
            {error && <p className="text-red-600">{error}</p>}
            {!loading && logs.length === 0 && (
                <p className="text-gray-500">No logs found yet.</p>
            )}

            <ul className="space-y-4">
                {logs.map((log) => (
                    <li
                        key={log.id}
                        className="border p-4 bg-white rounded shadow text-sm space-y-1"
                    >
                        <p>
                            <span className="font-semibold">📥 Query:</span>{" "}
                            {log.user_query}
                        </p>
                        <p>
                            <span className="font-semibold">📤 Clova Response:</span>{" "}
                            {log.response_text.slice(0, 200)}...
                        </p>
                        <p>
                            <span className="font-semibold">📕 Book ID:</span>{" "}
                            {log.book_isbns || "N/A"}
                        </p>
                        <p className="text-gray-500 text-xs">
                            🕒 {new Date(log.created_at).toLocaleString()}
                        </p>
                    </li>
                ))}
            </ul>
        </div>
    );
}
