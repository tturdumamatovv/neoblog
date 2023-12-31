from django.utils import timezone
from django.db import models
from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver

from user.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    description = models.CharField(max_length=255)
    text = models.TextField()
    photo = models.ImageField(upload_to='post_photos/', blank=True, null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    comments = models.ManyToManyField("Comment", related_name='post_comments')
    publication_date = models.DateTimeField(default=timezone.now)
    favorites = models.ManyToManyField(CustomUser, related_name='favorite_posts', blank=True)

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        self.total_comments = self.comments.count()
        super().save(*args, **kwargs)




class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} - {self.post}'


@receiver(post_save, sender=Comment)
def update_post_comments_count(sender, instance, **kwargs):
    post = instance.post
    post.total_comments = post.comments.count()
    post.save()
