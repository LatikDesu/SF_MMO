from django.core.cache import cache
from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField

import accounts.models
from posts.resources import TYPE, no_class


class Category(models.Model):
    type = models.CharField("Класс", max_length=2, choices=TYPE, default=no_class)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return f'{dict(TYPE)[self.type]}'

    class Meta:
        verbose_name = "Класс"
        verbose_name_plural = "Классы"


class Post(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = HTMLField()
    poster = models.ImageField("Постер", upload_to="media/posts", null=True, blank=True)

    user = models.ForeignKey(accounts.models.User, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def get_comments(self):
        return self.comment_set.filter(parent__isnull=True)

    def __str__(self):
        return f'{self.title} : {self.time.strftime("%d.%m.%Y")}: {self.description[:20]}'

    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post.title}: {self.category.type}'


class Comment(models.Model):
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    rev_status = models.BooleanField(default=False)

    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )

    post = models.ForeignKey(Post, verbose_name="Статья", on_delete=models.CASCADE)
    user = models.ForeignKey(accounts.models.User, verbose_name="Пользователь", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post.title} - {self.user}'
