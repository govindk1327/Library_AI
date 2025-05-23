from django.urls import path
from api.views import RecommendView, book_list, prompt_logs, signup, login, user_preferences

urlpatterns = [
    path('recommend/', RecommendView.as_view()),
    path('books/', book_list),
    path("logs/", prompt_logs),
    path("signup/", signup),
    path("login/", login),
    path("preferences/", user_preferences),
]

