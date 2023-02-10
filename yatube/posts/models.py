from django.db import models

from core.models import CreatedModel
from yatube.settings import POST_STR_MULTIPLIER
from users.models import User


class Group(models.Model):
    title = models.CharField('имя', max_length=200)
    slug = models.SlugField('адрес', unique=True)
    description = models.TextField('описание')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self) -> str:
        return self.title


class Post(CreatedModel):
    text = models.TextField('текст поста', help_text='Текст нового поста')
    author = models.ForeignKey(User, verbose_name='автор',
                               on_delete=models.CASCADE,
                               related_name='posts', )
    group = models.ForeignKey(Group,
                              verbose_name='Группа',
                              null=True,
                              blank=True,
                              on_delete=models.SET_NULL,
                              related_name='posts',
                              help_text=('Группа, к которой '
                                         'будет относиться пост'),)
    likes = models.ManyToManyField(User, related_name='like_posts')
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self) -> str:
        return self.text[:POST_STR_MULTIPLIER]


class Comment(CreatedModel):
    post = models.ForeignKey(Post,
                             verbose_name='Пост',
                             on_delete=models.CASCADE,
                             related_name='comments',)
    author = models.ForeignKey(User, verbose_name='Автор комментария',
                               on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField('Добавить комментарий',
                            help_text='Введите текст нового комментария')
    likes = models.ManyToManyField(User, related_name='like_comments')

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return self.text[:POST_STR_MULTIPLIER]


class Follow(CreatedModel):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower',)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='following')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follower_following'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F("author")),
                name='check_not_self_follow'
            ),
        ]

    def __str__(self) -> str:
        return f'Подписка {self.user} на {self.author}'
