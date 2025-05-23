import { useEffect, useState } from "react";
import client from "../api/client";

export default function PreferencesPage() {
    const [form, setForm] = useState({
        preferred_genres: [],
        preferred_language: "ko",
        prefers_ai_images: true,
    });
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState("");
    const [saved, setSaved] = useState(false);

    const GENRE_OPTIONS = [
        "Fiction", "Fantasy", "Mystery", "History", "Science", "Biography", "Children", "Romance",
    ];

    useEffect(() => {
        const fetchPreferences = async () => {
            try {
                const res = await client.get("/preferences/");
                setForm(res.data);
            } catch (err) {
                setError("Failed to load preferences.");
            } finally {
                setLoading(false);
            }
        };
        fetchPreferences();
    }, []);

    const toggleGenre = (genre) => {
        const genres = form.preferred_genres.includes(genre)
            ? form.preferred_genres.filter((g) => g !== genre)
            : [...form.preferred_genres, genre];
        setForm({ ...form, preferred_genres: genres });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSaving(true);
        setSaved(false);
        try {
            await client.put("/preferences/", form);
            setSaved(true);
        } catch {
            setError("Failed to save preferences.");
        } finally {
            setSaving(false);
        }
    };

    return (
        <div className="max-w-3xl mx-auto mt-10">
            <h2 className="text-2xl font-bold mb-4">⚙️ User Preferences</h2>

            {loading ? (
                <p>⏳ Loading...</p>
            ) : (
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="block font-semibold mb-1">Preferred Genres</label>
                        <div className="flex flex-wrap gap-2">
                            {GENRE_OPTIONS.map((genre) => (
                                <button
                                    key={genre}
                                    type="button"
                                    onClick={() => toggleGenre(genre)}
                                    className={`px-3 py-1 rounded border ${form.preferred_genres.includes(genre)
                                            ? "bg-blue-600 text-white"
                                            : "bg-gray-100 text-gray-700"
                                        }`}
                                >
                                    {genre}
                                </button>
                            ))}
                        </div>
                    </div>

                    <div>
                        <label className="block font-semibold mb-1">Preferred Language</label>
                        <select
                            className="border p-2 rounded"
                            value={form.preferred_language}
                            onChange={(e) =>
                                setForm({ ...form, preferred_language: e.target.value })
                            }
                        >
                            <option value="ko">Korean</option>
                            <option value="en">English</option>
                        </select>
                    </div>

                    <div>
                        <label className="flex items-center gap-2">
                            <input
                                type="checkbox"
                                checked={form.prefers_ai_images}
                                onChange={(e) =>
                                    setForm({ ...form, prefers_ai_images: e.target.checked })
                                }
                            />
                            Use AI-generated book covers
                        </label>
                    </div>

                    {error && <p className="text-red-500">{error}</p>}
                    {saved && <p className="text-green-600">✅ Preferences saved.</p>}

                    <button
                        type="submit"
                        className="bg-green-600 text-white px-4 py-2 rounded"
                        disabled={saving}
                    >
                        {saving ? "Saving..." : "Save Preferences"}
                    </button>
                </form>
            )}
        </div>
    );
}
