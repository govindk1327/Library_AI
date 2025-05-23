import { useState, useEffect } from "react";
import client from "../api/client";

export default function BooksPage() {
    const [books, setBooks] = useState([]);
    const [q, setQ] = useState("");
    const [page, setPage] = useState(1);
    const [total, setTotal] = useState(0);
    const [loading, setLoading] = useState(true);

    const fetchBooks = async () => {
        setLoading(true);
        try {
            const res = await client.get(`/books/?q=${q}&page=${page}&limit=10`);
            setBooks(res.data.results);
            setTotal(res.data.total);
        } catch (err) {
            console.error("❌ Failed to fetch books", err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchBooks();
    }, [q, page]);

    const totalPages = Math.ceil(total / 10);

    return (
        <div className="max-w-4xl mx-auto mt-10">
            <h2 className="text-2xl font-bold mb-4">📚 Browse Books</h2>

            <input
                className="border p-2 w-full mb-4 rounded"
                placeholder="Search by title or author..."
                value={q}
                onChange={(e) => {
                    setPage(1);
                    setQ(e.target.value);
                }}
            />

            {loading ? (
                <p>⏳ Loading...</p>
            ) : books.length === 0 ? (
                <p className="text-gray-500">No books found.</p>
            ) : (
                <>
                    <ul className="space-y-4">
                        {books.map((book) => (
                            <li
                                key={book.id}
                                className="bg-white shadow rounded p-4 border border-gray-100"
                            >
                                <h3 className="text-lg font-semibold">{book.title}</h3>
                                <p className="text-sm text-gray-700">
                                    {book.author} &middot; {book.publisher} &middot; {book.pub_date}
                                </p>
                            </li>
                        ))}
                    </ul>

                    <div className="mt-6 flex justify-between items-center text-sm">
                        <button
                            className="px-3 py-1 bg-gray-200 rounded"
                            disabled={page <= 1}
                            onClick={() => setPage((p) => p - 1)}
                        >
                            ← Previous
                        </button>
                        <span>
                            Page {page} of {totalPages}
                        </span>
                        <button
                            className="px-3 py-1 bg-gray-200 rounded"
                            disabled={page >= totalPages}
                            onClick={() => setPage((p) => p + 1)}
                        >
                            Next →
                        </button>
                    </div>
                </>
            )}
        </div>
    );
}
