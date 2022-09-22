from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from account.models import Author, User
from account.serializers import RegisterSerializer, UserAuthorSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        if user:
            Author.objects.create(user=user)


class UserAuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = UserAuthorSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser, ]
