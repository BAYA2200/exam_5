from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('user_author', views.UserAuthorViewSet, basename='user_author')
urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('', include('rest_framework.urls')),
    path('token/', obtain_auth_token),
]