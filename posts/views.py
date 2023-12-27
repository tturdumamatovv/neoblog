from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db.models import Count, Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import (
    Category,
    Post,
    Comment
)
from .serializers import (
    CategorySerializer,
    PostSerializer,
    PostCreateUpdateSerializer,
    CommentCreateSerializer,
    CommentSerializer,
    PostDetailSerializer
)
from .permissions import (
    IsOwnerOrAdminPermission,
    IsCommentOwnerOrPostAuthorOrAdmin
)


class GlobalSearchView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60*5))  # Cache for 5 minutes
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        return Post.objects.filter(
            Q(description__icontains=query) | Q(text__icontains=query)
        ).annotate(comments_count=Count('post_comments')).order_by('-publication_date')


class CategoryFilterView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return Post.objects.filter(category__id=category_id).annotate(comments_count=Count('post_comments')).order_by('-publication_date')


class CategoryCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]


class PostListView(generics.ListAPIView):
    queryset = Post.objects.annotate(comments_count=Count('post_comments')).order_by('-publication_date')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


class PostRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        comments = Comment.objects.filter(post=instance)
        post_serializer = self.get_serializer(instance)
        comment_serializer = CommentSerializer(comments, many=True)
        data = post_serializer.data
        data['comments'] = comment_serializer.data
        return Response(data)


class PostUpdateAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsOwnerOrAdminPermission]


class PostDeleteAPIView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrAdminPermission]


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        post = comment.post
        post.comments_count = post.comments.count()
        post.save()


class CommentUpdateAPIView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdminPermission]


class CommentDeleteAPIView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdminPermission, IsCommentOwnerOrPostAuthorOrAdmin]
