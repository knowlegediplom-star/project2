from django.contrib import admin
from .models import Collect, Payment


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "current_amount", "target_amount", "end_at")
    search_fields = ("title", "author__username")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "collect", "amount", "created_at")