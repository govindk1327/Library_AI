// import { useState } from "react";
// import client from "../api/client";
// import { useUserPrefs } from "../context/UserContext";
// import { t } from "../utils/i18n";

// export default function RecommendPage() {
//     const [query, setQuery] = useState("");
//     const [result, setResult] = useState(null);
//     const [loading, setLoading] = useState(false);
//     const [error, setError] = useState("");
//     const { preferences } = useUserPrefs();
//     const lang = preferences?.preferred_language || "ko";

//     const handleSubmit = async (e) => {
//         e.preventDefault();
//         setError("");
//         setLoading(true);
//         setResult(null);

//         try {
//             const res = await client.post("/recommend/", { query });
//             setResult(res.data);
//         } catch (err) {
//             setError("❌ Failed to fetch recommendation.");
//         } finally {
//             setLoading(false);
//         }
//     };

//     const renderImage = () => {
//         if (!result.image_path || result.image_path === "NO_COVER") {
//             return (
//                 <div className="text-sm text-gray-400 italic mt-4">
//                     {t(lang, "no_image")}
//                     <img
//                         src="/static/images/no_cover.png"
//                         alt="No cover"
//                         className="mt-2 w-64 h-64 object-contain opacity-50"
//                     />
//                 </div>
//             );
//         }

//         const isExternal = result.image_path.startsWith("http");
//         return (
//             <img
//                 src={isExternal ? result.image_path : `http://localhost:8000/${result.image_path}`}
//                 alt="Book cover"
//                 className="mt-4 w-64 h-64 object-cover rounded"
//             />
//         );
//     };

//     return (
//         <div className="min-h-screen w-full bg-darker text-gray-100 flex items-center justify-center px-4">
//         <div className="w-full max-w-2xl bg-dark p-6 rounded-lg shadow-lg">
//                 <h2 className="text-3xl font-bold mb-6 text-accent">
//                     {t(lang, "ask_ai")}
//                 </h2>

//                 <form onSubmit={handleSubmit} className="flex gap-2 mb-6">
//                     <input
//                         className="flex-1 bg-gray-800 border border-gray-700 text-white p-3 rounded focus:outline-none focus:ring focus:ring-accent"
//                         placeholder={
//                             lang === "ko"
//                                 ? "예: '10대 여학생에게 추천할 판타지 소설'"
//                                 : "e.g., 'Recommend a fantasy novel for a teen girl'"
//                         }
//                         value={query}
//                         onChange={(e) => setQuery(e.target.value)}
//                     />
//                     <button className="bg-accent text-white px-5 py-2 rounded hover:bg-emerald-500 transition">
//                         Ask
//                     </button>
//                 </form>

//                 {loading && <p className="text-gray-400">⏳ {t(lang, "loading")}</p>}
//                 {error && <p className="text-red-500">{error}</p>}

//                 {result && (
//                     <div className="border-t border-gray-700 pt-4">
//                         <h3 className="text-xl font-semibold mb-2">📖 {result.recommended_title}</h3>

//                         {result.book_metadata ? (
//                             <div className="mb-2">
//                                 <p><strong>Author:</strong> {result.book_metadata.author}</p>
//                                 <p><strong>Publisher:</strong> {result.book_metadata.publisher}</p>
//                                 <p><strong>ISBN:</strong> {result.book_metadata.isbn13}</p>
//                             </div>
//                         ) : (
//                             <p className="text-gray-500">{t(lang, "no_book")}</p>
//                         )}

//                         <p className="mt-2 text-sm text-gray-400 italic">💬 {result.ai_response}</p>

//                         {renderImage()}

//                         {result.availability?.length > 0 && (
//                             <div className="mt-4">
//                                 <p className="font-semibold">{t(lang, "availability")}</p>
//                                 <ul className="list-disc ml-5 text-sm text-gray-300">
//                                     {result.availability.map((lib, i) => (
//                                         <li key={i}>{lib}</li>
//                                     ))}
//                                 </ul>
//                             </div>
//                         )}
//                     </div>
//                 )}
//             </div>
//         </div>
//     );
// }

// import { useState } from "react";
// import client from "../api/client";
// import { useUserPrefs } from "../context/UserContext";
// import { t } from "../utils/i18n";

// export default function RecommendPage() {
//     const [query, setQuery] = useState("");
//     const [result, setResult] = useState(null);
//     const [loading, setLoading] = useState(false);
//     const [error, setError] = useState("");
//     const { preferences } = useUserPrefs();
//     const lang = preferences?.preferred_language || "ko";

//     const handleSubmit = async (e) => {
//         e.preventDefault();
//         setError("");
//         setLoading(true);
//         setResult(null);

//         try {
//             const res = await client.post("/recommend/", { query });
//             setResult(res.data);
//         } catch (err) {
//             setError("❌ Failed to fetch recommendation.");
//         } finally {
//             setLoading(false);
//         }
//     };

//     const renderImage = () => {
//         if (!result.image_path || result.image_path === "NO_COVER") {
//             return (
//                 <div className="text-sm text-gray-500 italic mt-4 flex flex-col items-center">
//                     {t(lang, "no_image")}
//                     <img
//                         src="/static/images/no_cover.png"
//                         alt="No cover"
//                         className="mt-2 w-48 h-64 object-contain opacity-50 rounded-xl"
//                     />
//                 </div>
//             );
//         }

//         const isExternal = result.image_path.startsWith("http");
//         return (
//             <img
//                 src={isExternal ? result.image_path : `http://localhost:8000/${result.image_path}`}
//                 alt="Book cover"
//                 className="mt-4 w-48 h-64 object-cover rounded-xl shadow-md"
//             />
//         );
//     };

//     return (
//         <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white flex items-center justify-center px-4 py-10">
//             <div className="w-full max-w-3xl bg-gray-950 p-8 rounded-2xl shadow-2xl">
//                 <h2 className="text-4xl font-bold mb-6 text-emerald-400 text-center">
//                     {t(lang, "ask_ai")}
//                 </h2>

//                 <form onSubmit={handleSubmit} className="flex flex-col md:flex-row gap-4 mb-8">
//                     <input
//                         className="flex-1 bg-gray-800 border border-gray-700 text-white p-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-400"
//                         placeholder={
//                             lang === "ko"
//                                 ? "예: '10대 여학생에게 추천할 판타지 소설'"
//                                 : "e.g., 'Recommend a fantasy novel for a teen girl'"
//                         }
//                         value={query}
//                         onChange={(e) => setQuery(e.target.value)}
//                     />
//                     <button
//                         type="submit"
//                         className="bg-emerald-500 hover:bg-emerald-600 text-white px-6 py-3 rounded-lg font-semibold transition"
//                     >
//                         {t(lang, "ask") || "Ask"}
//                     </button>
//                 </form>

//                 {loading && <p className="text-gray-400 text-center">⏳ {t(lang, "loading")}</p>}
//                 {error && <p className="text-red-400 text-center">{error}</p>}

//                 {result && (
//                     <div className="border-t border-gray-700 pt-6 mt-6 space-y-4">
//                         <h3 className="text-2xl font-bold text-emerald-300">
//                             📖 {result.recommended_title}
//                         </h3>

//                         {result.book_metadata ? (
//                             <div className="text-sm text-gray-300 space-y-1">
//                                 <p><span className="font-semibold">Author:</span> {result.book_metadata.author}</p>
//                                 <p><span className="font-semibold">Publisher:</span> {result.book_metadata.publisher}</p>
//                                 <p><span className="font-semibold">ISBN:</span> {result.book_metadata.isbn13}</p>
//                             </div>
//                         ) : (
//                             <p className="text-gray-500">{t(lang, "no_book")}</p>
//                         )}

//                         <p className="italic text-gray-400">💬 {result.ai_response}</p>

//                         <div className="flex justify-center">
//                             {renderImage()}
//                         </div>

//                         {result.availability?.length > 0 && (
//                             <div>
//                                 <p className="font-semibold text-emerald-400 mt-4">{t(lang, "availability")}</p>
//                                 <ul className="list-disc ml-5 text-sm text-gray-300 space-y-1 mt-2">
//                                     {result.availability.map((lib, i) => (
//                                         <li key={i}>{lib}</li>
//                                     ))}
//                                 </ul>
//                             </div>
//                         )}
//                     </div>
//                 )}
//             </div>
//         </div>
//     );
// }

import { useState } from "react";
import client from "../api/client";
import { useUserPrefs } from "../context/UserContext";
import { t } from "../utils/i18n";

export default function RecommendPage() {
    const [query, setQuery] = useState("");
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const { preferences } = useUserPrefs();
    const lang = preferences?.preferred_language || "ko";

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        setLoading(true);
        setResult(null);

        try {
            const res = await client.post("/recommend/", { query });
            setResult(res.data);
        } catch (err) {
            setError("❌ Failed to fetch recommendation.");
        } finally {
            setLoading(false);
        }
    };

    const renderImage = () => {
        if (!result.image_path || result.image_path === "NO_COVER") {
            return (
                <div className="text-sm text-gray-500 italic mt-4 flex flex-col items-center">
                    {t(lang, "no_image")}
                    <img
                        src="/static/images/no_cover.png"
                        alt="No cover"
                        className="mt-2 w-48 h-64 object-contain opacity-50 rounded-xl"
                    />
                </div>
            );
        }

        const isExternal = result.image_path.startsWith("http");
        return (
            <img
                src={isExternal ? result.image_path : `http://localhost:8000/${result.image_path}`}
                alt="Book cover"
                className="mt-4 w-48 h-64 object-cover rounded-xl shadow-md"
            />
        );
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white flex items-center justify-center px-4 py-10">
            <div className="w-full max-w-3xl bg-gray-950 p-8 rounded-2xl shadow-2xl">
                <h2 className="text-4xl font-bold mb-6 text-emerald-400 text-center">
                    {t(lang, "ask_ai")}
                </h2>

                <form onSubmit={handleSubmit} className="flex flex-col md:flex-row gap-4 mb-8">
                    <input
                        className="flex-1 bg-gray-800 border border-gray-700 text-white p-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-400"
                        placeholder={
                            lang === "ko"
                                ? "예: '10대 여학생에게 추천할 판타지 소설'"
                                : "e.g., 'Recommend a fantasy novel for a teen girl'"
                        }
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                    />
                    <button
                        type="submit"
                        className="bg-emerald-500 hover:bg-emerald-600 text-white px-6 py-3 rounded-lg font-semibold transition"
                    >
                        {t(lang, "ask") || "Ask"}
                    </button>
                </form>

                {loading && <p className="text-gray-400 text-center">⏳ {t(lang, "loading")}</p>}
                {error && <p className="text-red-400 text-center">{error}</p>}

                {result && (
                    <div className="border-t border-gray-700 pt-6 mt-6 space-y-4">
                        <h3 className="text-2xl font-bold text-emerald-300">
                            📖 {result.recommended_title}
                        </h3>

                        {result.book_metadata ? (
                            <div className="text-sm text-gray-300 space-y-1">
                                <p><span className="font-semibold">Author:</span> {result.book_metadata.author}</p>
                                <p><span className="font-semibold">Publisher:</span> {result.book_metadata.publisher}</p>
                                <p><span className="font-semibold">ISBN:</span> {result.book_metadata.isbn13}</p>
                            </div>
                        ) : (
                            <p className="text-gray-500">{t(lang, "no_book")}</p>
                        )}

                        <p className="italic text-gray-400">💬 {result.ai_response}</p>

                        <div className="flex justify-center">
                            {renderImage()}
                        </div>

                        {result.availability?.length > 0 && (
                            <div>
                                <p className="font-semibold text-emerald-400 mt-4">{t(lang, "availability")}</p>
                                <ul className="list-disc ml-5 text-sm text-gray-300 space-y-1 mt-2">
                                    {result.availability.map((lib, i) => (
                                        <li key={i}>{lib}</li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}
