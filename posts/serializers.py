from rest_framework import serializers

from user.models import CustomUser
from .models import (
    Category,
    Post,
    Comment
)
from .datetime import format_localized_datetime


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class CommentSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'created_at')

    def get_created_at(self, obj):
        return format_localized_datetime(obj.created_at)


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('post', 'text')


class PostSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer()
    category = CategorySerializer()
    publication_date = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'description', 'text', 'photo', 'author',
                  'category', 'publication_date', 'comments_count', 'is_favorite')

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_publication_date(self, obj):
        return format_localized_datetime(obj.publication_date)

    def get_is_favorite(self, obj):
        user = self.context['request'].user
        return user in obj.favorites.all()


class PostDetailSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer()
    category = CategorySerializer()
    comments = CommentSerializer(many=True)
    publication_date = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'description', 'text', 'photo', 'author', 'category', 'publication_date', 'comments')

    def get_publication_date(self, obj):
        return format_localized_datetime(obj.publication_date)


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    author = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    publication_date = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'description', 'text', 'photo', 'author', 'category', 'publication_date')

    def get_publication_date(self, obj):
        return format_localized_datetime(obj.publication_date)
