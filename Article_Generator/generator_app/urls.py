from django.urls import path
from .views import UserRegisterAPIView, UserLoginAPIView, UserLogoutAPIView, GenerateArticleAPI

urlpatterns = [
  path('api/signup/', UserRegisterAPIView.as_view(), name='signup'),
  path('api/signin/', UserLoginAPIView.as_view(), name='signin'),
  path('api/logout/', UserLogoutAPIView.as_view(), name='logout'),
  path('api/generate_article/', GenerateArticleAPI.as_view(), name="qna")
]