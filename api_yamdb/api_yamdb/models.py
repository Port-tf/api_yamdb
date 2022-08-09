
from django.contrib.auth import get_user_model
from django.db import models

# from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()



class Score(models.Model):
    score = models.IntegerField(default=0, null=True, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='scores'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    class Meta:
        unique_together = ('user', 'title')


class Review(models.Model):
    text = models.TextField(max_length=200,
                            verbose_name='Текст отзыва',
                            help_text='Введите текст отзыва'
                            )
    created = models.DateTimeField('Дата публикации', auto_now_add=True)
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    def __str__(self):
        return self.text[:15]


class Comments(models.Model):
    text = models.TextField(max_length=200,
                            verbose_name='Текст комментария',
                            help_text='Введите текст комментария'
                            )
    created = models.DateTimeField('Дата публикации', auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    def __str__(self):
        return self.text[:15]
