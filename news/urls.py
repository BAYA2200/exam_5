from django.urls import include, path

from news import views

urlpatterns = [
    path('api/news/', views.NewsListCreateAPIView.as_view()),
    path('api/news/<int:pk>/', views.NewsRetrieveUpdateDestroyAPIView.as_view()),
    path('api/news/<int:news_id>/comments/', views.CommentListCreateAPIView.as_view()),
    path('api/news/<int:news_id>/comments/<int:pk>/', views.CommentRetrieveUpdateDestroyAPIView.as_view()),
    path('api/statuses/', views.StatusListCreateAPIView.as_view()),
    path('api/statuses/<pk>/', views.StatusRetrieveUpdateDestroyAPIView.as_view()),
    path('api/news/<new_id>/<slug>/', views.NewsAddStatus.as_view()),

]


