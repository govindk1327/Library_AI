from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from books.models import Book
from api.serializers import BookSerializer
from recommendations.pipeline import run_recommendation_pipeline
from rest_framework.decorators import api_view, permission_classes
from asgiref.sync import async_to_sync
from recommendations.models import PromptLog
from api.serializers import PromptLogSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserSignupSerializer, UserPreferenceSerializer
from rest_framework.permissions import IsAuthenticated
from .models import UserPreference
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt

from django.db.models import Q

@api_view(["GET"])
def book_list(request):
    query = request.GET.get("q", "")
    page = int(request.GET.get("page", 1))
    per_page = int(request.GET.get("limit", 20))
    offset = (page - 1) * per_page

    queryset = Book.objects.all()
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )

    total = queryset.count()
    books = queryset[offset : offset + per_page]
    serializer = BookSerializer(books, many=True)

    return Response({
        "total": total,
        "page": page,
        "limit": per_page,
        "results": serializer.data
    })



# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def prompt_logs(request):
#     logs = PromptLog.objects.filter(user=request.user).order_by("-created_at")[:50]
#     data = [
#         {
#             "id": log.id,
#             "user_query": log.user_query,
#             "response_text": log.response_text,
#             "book_isbns": log.book_isbns,
#             "created_at": log.created_at,
#         }
#         for log in logs
#     ]
#     return Response(data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def prompt_logs(request):
    logs = PromptLog.objects.filter(user=request.user).order_by("-created_at")[:50]
    serializer = PromptLogSerializer(logs, many=True)
    return Response(serializer.data)




# @method_decorator(csrf_exempt, name='dispatch')
class RecommendView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        query = request.data.get('query')
        if not query:
            return Response({'error': "Missing 'query' parameter"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            
            result = async_to_sync(run_recommendation_pipeline)(query, user=request.user)
            return Response(result)
        except Exception as e:
            return Response({'error': 'Internal Server Error', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query')
        if not query:
            return Response({'error': "Missing 'query' parameter"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = async_to_sync(run_recommendation_pipeline)(query, user=request.user)
            return Response(result)
        except Exception as e:
            return Response({'error': 'Internal Server Error', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def signup(request):
    serializer = UserSignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # 🧠 Create default preferences
        UserPreference.objects.create(
            user=user,
            preferred_genres=["Fiction", "Fantasy"],
            preferred_language="ko",
            prefers_ai_images=True
        )

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=201)
    return Response(serializer.errors, status=400)

@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)

    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
    return Response({"error": "Invalid credentials"}, status=401)

@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def user_preferences(request):
    user = request.user
    prefs, _ = UserPreference.objects.get_or_create(user=user)

    if request.method == "GET":
        serializer = UserPreferenceSerializer(prefs)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = UserPreferenceSerializer(prefs, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def user_profile(request):
#     user = request.user
#     prefs = getattr(user, "preferences", None)

#     return Response({
#         "id": user.id,
#         "username": user.username,
#         "email": user.email,
#         "preferences": {
#             "favoriteGenres": prefs.preferred_genres if prefs else [],
#             "language": prefs.language if prefs else "en",
#             "preferAICovers": prefs.prefers_ai_images if prefs else False
#         }
#     })
    