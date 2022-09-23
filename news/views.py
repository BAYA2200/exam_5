from django.db import IntegrityError
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.generics import ListCreateAPIView, get_object_or_404, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import NewsStatus, CommentStatus
from news.models import News, Comment, Status
from news.permissions import IsAuthorPermission
from news.serializers import NewsSerializer, CommentSerializer, StatusSerializer


class NewsListCreateAPIView(ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthorPermission, ]

    def perform_create(self, serializers):
        serializers.save(author=self.request.user.author)


class NewsRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthorPermission, ]


class CommentListCreateAPIView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthorPermission, ]

    def get_queryset(self):
        return self.queryset.filter(news__id=self.kwargs['news_id'])

    def perform_create(self, serializers):
        serializers.save(
            author=self.request.user.author,
            news=get_object_or_404(News, id=self.kwargs['news_id'])
        )


class CommentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthorPermission, ]


class StatusListCreateAPIView(ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser, ]


class StatusRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser, ]


class NewsAddStatus(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, new_id, slug):
        news = get_object_or_404(News, id=new_id)
        news_status = get_object_or_404(Status, slug=slug)
        try:
            NewsStatus.objects.create(news=news, author=request.user.author, status=news_status)
        except IntegrityError:
            add_news_status = NewsStatus.objects.get(news=news, author=request.user.author)
            add_news_status.status = news_status
            add_news_status.save()
            data = {"error You already added status"}
            return Response(data, status.HTTP_403_FORBIDDEN)
        else:
            data = {"message Status added"}
            return Response(data, status=status.HTTP_201_CREATED)
