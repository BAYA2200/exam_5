from django.urls import include, path
from rest_framework.routers import DefaultRouter

from news import views

router = DefaultRouter()
router.register('news', views.NewsViewSet, basename='news')
urlpatterns = [
    path('', include(router.urls)),
    path('api/news/', views.NewsListCreateAPIView.as_view()),
    path('api/news/<news_id>', views.NewsRetrieveUpdateDestroyAPIView.as_view()),
    path('api/news/<news_id>/comments/', views.CommentListCreateAPIView.as_view()),
    path('api/news/<news_id>/comments/<int:pk>/', views.CommentRetrieveUpdateDestroyAPIView.as_view()),
    path('api/statuses/', views.StatusListCreateAPIView.as_view()),
    path('api/statuses/<pk>', views.StatusRetrieveUpdateDestroyAPIView.as_view()),
    path('api/news/<new_id>/<slug>/', views.NewsAddStatus.as_view()),

]


