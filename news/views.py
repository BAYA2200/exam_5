from django.db import IntegrityError
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.generics import ListCreateAPIView, get_object_or_404, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from serializers import serializer
from .models import NewsStatus, CommentStatus
from news.models import News, Comment, Status
from news.permissions import IsAuthorPermission
from news.serializers import NewsSerializer, CommentSerializer, StatusSerializer


class NewsViewSet(ModelViewSet):
    serializer_class = NewsSerializer
    queryset = News.objects.all()
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = [IsAuthorPermission, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NewsListCreateAPIView(ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthorPermission, ]

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.query_params.get('user')
        if user:
            queryset = queryset.filter(user__username=user)
            search = self.request.query_params.get('search')
            if search:
                queryset = queryset.filter(text__icontains=search)
            return queryset

    def perform_create(self, serializers):
        serializers.save(user=self.request.user,
                         tweet=get_object_or_404(News, id=self.kwargs['news_id'])
                         )


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
        queryset = self.queryset
        user = self.request.query_params.get('user')
        if user:
            queryset = queryset.filter(user__username=user)
            search = self.request.query_params.get('search')
            if search:
                queryset = queryset.filter(text__icontains=search)
            return queryset

    def perform_create(self, serializers):
        serializers.save(user=self.request.user,
                         tweet=get_object_or_404('news', id=self.kwargs['news_id'])
                         )


class CommentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthorPermission, ]

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.query_params.get('user')
        if user:
            queryset = queryset.filter(user__username=user)
            search = self.request.query_params.get('search')
            if search:
                queryset = queryset.filter(text__icontains=search)
            return queryset

    def perform_create(self, serializers):
        serializers.save(user=self.request.user,
                         tweet=get_object_or_404('news', id=self.kwargs['news_id'])
                         )


class StatusListCreateAPIView(ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthorPermission, ]

    def perform_create(self, serializers):
        user = serializer.save()
        if user:
            Status.objects.create(user=user, is_staff=True)


class StatusRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthorPermission, ]

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.query_params.get('user')
        if user:
            queryset = queryset.filter(user__username=user)
            search = self.request.query_params.get('search')
            if search:
                queryset = queryset.filter(text__icontains=search)
            return queryset

    def perform_create(self, serializer):
        user = serializer.save()
        if user:
            Status.objects.create(user=user, is_staff=True)

class NewsAddStatus(APIView):
    def get(self, request, new_id, slug):
        news = get_object_or_404(News, id=new_id)
        news_status = get_object_or_404(Status, slug=slug)
        try:
            add_status = NewsStatus.objects.create(news=news, user=request.user)
        except IntegrityError:
            add_news_status = NewsStatus.objects.get(news=news, user=request.user)
            add_news_status.status = news_status
            add_news_status.save()
            data = {"error You already added status"}
            return Response(data, status.HTTP_403_FORBIDDEN)
        else:
            data = {"message Status added"}
            return Response(data, status=status.HTTP_201_CREATED)


