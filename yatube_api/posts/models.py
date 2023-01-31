from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CheckConstraint, F, Q, UniqueConstraint


User = get_user_model()


class Group(models.Model):
    title = models.CharField('заголовок', max_length=200,)
    slug = models.SlugField(unique=True)
    description = models.TextField(verbose_name='описание')

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', blank=True)
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL, verbose_name='группа',
        related_name='posts', blank=True, null=True
    )

    class Meta:
        verbose_name = "текст"
        verbose_name_plural = "тексты"

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name="подписчик", related_name="follower")
    following = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name="автор поста", related_name="author")

    class Meta:
        verbose_name = "подписка"
        verbose_name_plural = "подписки"
        constraints = [
            UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_following'),
            CheckConstraint(
                check=~Q(user=F('following')),
                name='unique_following')
        ]
