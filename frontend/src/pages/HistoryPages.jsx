// import { useEffect, useState } from "react";
// import client from "../api/client";

// export default function LogsPage() {
//     const [logs, setLogs] = useState([]);
//     const [loading, setLoading] = useState(true);
//     const [error, setError] = useState("");

//     useEffect(() => {
//         const fetchLogs = async () => {
//             try {
//                 const res = await client.get("/logs/");
//                 setLogs(res.data);
//             } catch {
//                 setError("❌ Failed to load logs.");
//             } finally {
//                 setLoading(false);
//             }
//         };
//         fetchLogs();
//     }, []);

//     return (
//         <div className="max-w-4xl mx-auto mt-10">
//             <h2 className="text-2xl font-bold mb-4">🧾 Your Prompt Logs</h2>

//             {loading && <p>⏳ Loading...</p>}
//             {error && <p className="text-red-600">{error}</p>}
//             {!loading && logs.length === 0 && (
//                 <p className="text-gray-500">No logs found yet.</p>
//             )}

//             <ul className="space-y-4">
//                 {logs.map((log) => (
//                     <li
//                         key={log.id}
//                         className="bg-[#1e1e1e] text-gray-100 rounded-lg shadow-md p-4 mb-4"
//                     >
//                         <p>
//                             <span className="font-semibold">📥 Query:</span>{" "}
//                             {log.user_query}
//                         </p>
//                         <p>
//                             <span className="font-semibold">📤 Clova Response:</span>{" "}
//                             {log.response_text.slice(0, 200)}...
//                         </p>
//                         <p>
//                             <span className="font-semibold">📕 Book ID:</span>{" "}
//                             {log.book_isbns || "N/A"}
//                         </p>
//                         <p className="text-gray-500 text-xs">
//                             🕒 {new Date(log.created_at).toLocaleString()}
//                         </p>
//                     </li>
//                 ))}
//             </ul>
//         </div>
//     );
// }

import { useEffect, useState } from "react";
import client from "../api/client";
import { t } from "../utils/i18n";

export default function HistoryPage() {
    const [logs, setLogs] = useState([]);
    const lang = localStorage.getItem("lang") || "ko";

    useEffect(() => {
        const fetchLogs = async () => {
            try {
                const res = await client.get("/history/");
                setLogs(res.data);
            } catch (err) {
                console.error("❌ Failed to load history", err);
            }
        };
        fetchLogs();
    }, []);

    return (
        <div className="min-h-screen bg-gray-900 text-white p-6">
            <h1 className="text-3xl font-bold text-emerald-400 mb-6 text-center">
                {t(lang, "history")}
            </h1>

            {logs.length === 0 ? (
                <p className="text-gray-500 text-center">⏳ {t(lang, "loading")}</p>
            ) : (
                <div className="space-y-4 max-w-4xl mx-auto">
                    {logs.map((log) => (
                        <div
                            key={log.id}
                            className="bg-gray-800 p-4 rounded-xl shadow hover:shadow-xl transition"
                        >
                            <p className="text-sm text-gray-400 mb-1">
                                {new Date(log.created_at).toLocaleString()}
                            </p>
                            <p className="font-semibold text-emerald-300">
                                💬 {log.user_query}
                            </p>
                            <p className="text-gray-300 mt-1 truncate">
                                {log.response_text.slice(0, 200)}...
                            </p>
                            {log.book_isbns && (
                                <p className="text-sm text-gray-400 mt-2">
                                    📚 Book ID: {log.book_isbns}
                                </p>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
