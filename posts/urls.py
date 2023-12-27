from django.urls import path

from .views import (
    CategoryCreateView,
    PostCreateView,
    PostListView,
    PostUpdateAPIView,
    PostDeleteAPIView,
    PostRetrieveAPIView,
    CommentCreateAPIView,
    CommentUpdateAPIView,
    CommentDeleteAPIView,
    GlobalSearchView,
    CategoryFilterView
)

urlpatterns = [
    path('search/', GlobalSearchView.as_view(), name='global-search'),
    path('category/<int:category_id>/', CategoryFilterView.as_view(), name='category-filter'),
    path('category/', CategoryCreateView.as_view(), name='create_category'),
    path('posts/', PostListView.as_view(), name='posts'),
    path('post-create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', PostRetrieveAPIView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', PostUpdateAPIView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteAPIView.as_view(), name='post_delete'),
    path('posts/<int:pk>/comments/', CommentCreateAPIView.as_view(), name='comment-create'),
    path('comments/<int:pk>/update/', CommentUpdateAPIView.as_view(), name='comment-update'),
    path('comments/<int:pk>/delete/', CommentDeleteAPIView.as_view(), name='comment-delete'),
]
