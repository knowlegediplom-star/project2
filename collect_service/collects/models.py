from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


# 🔹 МОДЕЛЬ СБОРА
class Collect(models.Model):
    REASON_CHOICES = [
        ("birthday", "День рождения"),
        ("wedding", "Свадьба"),
        ("charity", "Благотворительность"),
        ("other", "Другое"),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="collects",
    )

    title = models.CharField(max_length=255)
    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    description = models.TextField()

    target_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )

    current_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )

    cover = models.ImageField(upload_to="covers/", null=True, blank=True)

    end_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    # 🔥 ВАЛИДАЦИЯ
    def clean(self):
        if self.end_at <= timezone.now():
            raise ValidationError("Дата окончания должна быть в будущем")

        if self.target_amount is not None and self.target_amount <= 0:
            raise ValidationError("Сумма должна быть больше 0")

    def __str__(self):
        return self.title


# 🔹 МОДЕЛЬ ПЛАТЕЖА
class Payment(models.Model):
    collect = models.ForeignKey(
        Collect,
        on_delete=models.CASCADE,
        related_name="payments",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments",
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    # 🔥 ВАЛИДАЦИЯ
    def clean(self):
        if self.amount <= 0:
            raise ValidationError("Сумма должна быть больше 0")

        if self.collect.target_amount:
            remaining = self.collect.target_amount - self.collect.current_amount
            if self.amount > remaining:
                raise ValidationError("Сумма превышает остаток сбора")

    def __str__(self):
        return f"{self.user} → {self.collect} ({self.amount})"