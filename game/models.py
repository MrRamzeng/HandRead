from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class AccuracyGame(models.Model):
    TIMERS = (
        (30, "0:30"),
        (60, "1:00"),
        (120, "2:00")
    )
    MODES = (
        ('W', 'Только слова'),
        ('D', 'Только числа'),
        ('S', 'Только знаки'),
        ('ALL', 'Все')
    )
    user = models.ForeignKey('user.User', models.CASCADE)
    timer = models.CharField(
        'Таймер', choices=TIMERS, default=30, max_length=10
    )
    mode = models.CharField('Режим', choices=MODES, default='W', max_length=20)
    score = models.PositiveSmallIntegerField(default=0)
    speed = models.PositiveSmallIntegerField('Количество символов', default=0)
    accuracy = models.DecimalField(
        validators=(MinValueValidator(0), MaxValueValidator(100)), max_digits=5,
        decimal_places=2, default=0
    )
    max_score = models.PositiveSmallIntegerField('Лучший счёт', default=0)
    max_speed = models.PositiveSmallIntegerField(default=0)
    best_accuracy = models.DecimalField(
        'лучшая аккуратность', max_digits=5, decimal_places=2,
        validators=(MinValueValidator(0), MaxValueValidator(100)), default=0
    )
    best_score_time = models.DateTimeField(blank=True, null=True)
    is_win = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.timer} {self.mode} - {self.user.username}'

    class Meta:
        ordering = (
            '-best_accuracy', '-max_score', '-max_speed'
        )
