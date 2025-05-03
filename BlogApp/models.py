from django.db import models
from django.contrib.auth.models import User
import re

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    tagged_users = models.ManyToManyField(User, related_name='tagged_in_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def extract_user_tags(self):
        usernames = re.findall(r'@(\w+)', self.content)
        return User.objects.filter(username__in=usernames)

    def extract_tags(self):
        tag_names = re.findall(r'#(\w+)', self.content)
        tag_objects = []
        for name in tag_names:
            tag_obj, created = Tag.objects.get_or_create(name=name.lower())
            tag_objects.append(tag_obj)
        return tag_objects

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.tagged_users.set(self.extract_user_tags())
        self.tags.set(self.extract_tags())

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ('follower', 'following')

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
