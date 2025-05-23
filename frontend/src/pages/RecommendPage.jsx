import { useState } from "react";
import client from "../api/client";

export default function RecommendPage() {
    const [query, setQuery] = useState("");
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

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

    return (
        <div className="max-w-3xl mx-auto mt-10">
            <h2 className="text-2xl font-bold mb-4">Ask the AI for a book</h2>
            <form onSubmit={handleSubmit} className="flex gap-2 mb-4">
                <input
                    className="flex-1 border p-2 rounded"
                    placeholder="예: '10대 여학생에게 추천할 판타지 소설'"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />
                <button className="bg-blue-600 text-white px-4 py-2 rounded">
                    Ask
                </button>
            </form>

            {loading && <p className="text-gray-500">⏳ Thinking...</p>}
            {error && <p className="text-red-600">{error}</p>}

            {result && (
                <div className="bg-white shadow rounded p-4">
                    <h3 className="text-xl font-semibold mb-2">📖 {result.recommended_title}</h3>
                    {result.book_metadata ? (
                        <div className="mb-2">
                            <p><strong>Author:</strong> {result.book_metadata.author}</p>
                            <p><strong>Publisher:</strong> {result.book_metadata.publisher}</p>
                            <p><strong>ISBN:</strong> {result.book_metadata.isbn13}</p>
                        </div>
                    ) : (
                        <p className="text-gray-500">📚 No matching book found in the DB.</p>
                    )}

                    <p className="mt-2 text-sm text-gray-600 italic">💬 {result.ai_response}</p>

                    {result.image_path && (
                        <img
                            src={`http://localhost:8000/${result.image_path}`}
                            alt="Generated book cover"
                            className="mt-4 w-64 h-64 object-cover rounded"
                        />
                    )}

                    {result.availability?.length > 0 && (
                        <div className="mt-3">
                            <p className="font-semibold">📚 Availability (via Library):</p>
                            <ul className="list-disc ml-5 text-sm">
                                {result.availability.map((lib, i) => (
                                    <li key={i}>{lib}</li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
