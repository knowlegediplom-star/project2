from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError

from collects.models import Collect, Payment


class CollectTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test", password="123")

        self.collect = Collect.objects.create(
            author=self.user,
            title="Сбор",
            reason="birthday",
            description="Описание",
            target_amount=1000,
            end_at=timezone.now() + timedelta(days=1),
        )

    def test_collect_created(self):
        self.assertEqual(self.collect.title, "Сбор")

    def test_invalid_date(self):
        collect = Collect(
            author=self.user,
            title="Ошибка",
            reason="birthday",
            description="",
            target_amount=100,
            end_at=timezone.now() - timedelta(days=1),
        )

        with self.assertRaises(ValidationError):
            collect.clean()


class PaymentTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user", password="123")

        self.collect = Collect.objects.create(
            author=self.user,
            title="Сбор",
            reason="birthday",
            description="",
            target_amount=1000,
            end_at=timezone.now() + timedelta(days=1),
        )

    def test_payment_create(self):
        payment = Payment.objects.create(
            collect=self.collect,
            user=self.user,
            amount=200
        )

        self.assertEqual(payment.amount, 200)

    def test_payment_validation(self):
        self.collect.current_amount = 900
        self.collect.save()

        payment = Payment(
            collect=self.collect,
            user=self.user,
            amount=200
        )

        with self.assertRaises(ValidationError):
            payment.clean()

    def test_update_collect_amount(self):
        payment = Payment.objects.create(
            collect=self.collect,
            user=self.user,
            amount=300
        )

        self.collect.current_amount += payment.amount
        self.collect.save()

        self.assertEqual(self.collect.current_amount, 300)