export const translations = {
    ko: {
        ask_ai: "AI에게 책 추천 받기",
        ask: "추천 요청",
        loading: "생각 중입니다...",
        no_book: "📚 일치하는 책이 데이터베이스에 없습니다.",
        no_image: "❌ 표지 이미지를 찾을 수 없습니다.",
        availability: "📦 도서관 대출 가능 여부",
        author: "저자",
        publisher: "출판사",
        isbn: "ISBN",
        history: "히스토리",
        preferences: "환경설정",
        books: "도서 목록",
        login: "로그인",
        signup: "회원가입",
        no_cover: "표지 없음"

    },
    en: {
        ask_ai: "Ask the AI for a Book Recommendation",
        ask: "Ask",
        loading: "Thinking...",
        no_book: "📚 No matching book found in the DB.",
        no_image: "❌ Front cover not available.",
        availability: "📦 Library Availability",
        author: "Author",
        publisher: "Publisher",
        isbn: "ISBN",
        history: "History",
        preferences: "Preferences",
        books: "Books",
        login: "Login",
        signup: "Signup",
        no_cover: "No cover"
    }
};

// ✅ Export a helper function `t`
export function t(lang, key) {
    return translations[lang]?.[key] || key;
}
