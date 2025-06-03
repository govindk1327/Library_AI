from django.urls import path
from api.views import RecommendView, book_list, prompt_logs, signup, login, user_preferences

urlpatterns = [
    path('recommend/', RecommendView.as_view()),
    path('books/', book_list),
    path("history/", prompt_logs, name="history"),
    path("signup/", signup),
    path("login/", login),
    path("preferences/", user_preferences),
    # path("me/", user_profile, name="user-profile"),
]

