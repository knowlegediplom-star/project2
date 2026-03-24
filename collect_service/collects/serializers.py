from rest_framework import serializers
from .models import Collect, Payment


# 🔹 СЕРИАЛИЗАТОР ПЛАТЕЖА
class PaymentSerializer(serializers.ModelSerializer):
    user_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = [
            "id",
            "amount",
            "created_at",
            "user",
            "user_full_name",
        ]

    def get_user_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username


# 🔹 СЕРИАЛИЗАТОР СБОРА
class CollectSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)
    author_username = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Collect
        fields = [
            "id",
            "author",
            "author_username",
            "title",
            "reason",
            "description",
            "target_amount",
            "current_amount",
            "cover",
            "end_at",
            "created_at",
            "payments",
        ]

        read_only_fields = [
            "author",
            "current_amount",
            "created_at",
        ]