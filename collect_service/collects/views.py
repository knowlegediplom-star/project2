from django.db.models import Prefetch
from rest_framework import viewsets, permissions

from .models import Collect, Payment
from .serializers import CollectSerializer, PaymentSerializer


# 🔹 API для сборов
class CollectViewSet(viewsets.ModelViewSet):
    serializer_class = CollectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return (
            Collect.objects
            .select_related("author")
            .prefetch_related(
                Prefetch(
                    "payments",
                    queryset=Payment.objects.select_related("user")
                )
            )
            .all()
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# 🔹 API для платежей
class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.select_related("user", "collect").all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        # 🔥 обновляем сумму сбора
        collect = payment.collect
        collect.current_amount += payment.amount
        collect.save(update_fields=["current_amount"])