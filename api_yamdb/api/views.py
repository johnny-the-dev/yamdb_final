from api.filters import TitleFilter
from api.permissions import IsAdmin, IsAuthorOrReadonly, ReadOnlyOrAdmin
from api.serializers import (CategorySerializer, CodeSerializer,
                             CommentSerializer, GenreSerializer,
                             ReviewSerializer, SignUpSerializer,
                             TitleSerializer, UserEditSerializer,
                             UserSerializer)
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Title
from users.models import User

from api_yamdb.settings import FROM_EMAIL


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Регистрация на Yamdb',
        message=f'Код подтверждения: {confirmation_code}',
        from_email=FROM_EMAIL,
        recipient_list=(user.email, ),
    )

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    serializer = CodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )

    if default_token_generator.check_token(
        user, serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )

    @action(
        methods=(
            'get',
            'patch',
        ),
        detail=False,
        url_path='me',
        permission_classes=(permissions.IsAuthenticated, ),
        serializer_class=UserEditSerializer,
    )
    def users_own_profile(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
        else:
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class BaseEntityViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin
):
    permission_classes = (ReadOnlyOrAdmin, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class CategoryViewSet(BaseEntityViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(BaseEntityViewSet):
    permission_classes = (ReadOnlyOrAdmin, )
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (ReadOnlyOrAdmin, )
    filter_backends = (DjangoFilterBackend, )
    filter_class = TitleFilter

    def get_genre(self):
        genres = []
        # При проверке автотестами срабатывает self.request.data.getlist
        # При ручном тестировании - self.request.data
        try:
            genres_slugs = self.request.data.getlist('genre')
        except AttributeError:
            genres_slugs = self.request.data['genre']

        for genre_slug in genres_slugs:
            genre = get_object_or_404(Genre, slug=genre_slug)
            genres.append(genre)
        return genres

    def get_category(self):
        return get_object_or_404(Category, slug=self.request.data['category'])

    def perform_create(self, serializer):
        genres = self.get_genre()
        category = self.get_category()
        return serializer.save(category=category, genre=genres)

    def perform_update(self, serializer):
        genres = self.get_genre()
        category = self.get_category()
        serializer.save(category=category, genre=genres)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadonly, )

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadonly, )

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        review = get_object_or_404(title.reviews, id=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        review = get_object_or_404(title.reviews, id=self.kwargs['review_id'])
        return serializer.save(review=review, author=self.request.user)
