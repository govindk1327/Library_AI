import React from "react";

export default function Layout({ children }) {
    return (
        <div className="min-h-screen flex flex-col bg-background text-white">
            <header className="bg-dark px-6 py-4 shadow-md">
                <h1 className="text-2xl font-bold text-accent">📚 AI Book Recommender</h1>
            </header>

            <main className="flex-grow flex justify-center items-start py-10 px-4">
                <div className="w-full max-w-3xl">{children}</div>
            </main>

            <footer className="bg-dark px-6 py-4 text-center text-sm text-gray-500">
                &copy; 2025 Book Recommender. All rights reserved.
            </footer>
        </div>
    );
}