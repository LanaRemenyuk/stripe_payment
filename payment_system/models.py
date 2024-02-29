from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Item(models.Model):
    """Модель товара"""
    CURRENCY = (
        ('USD', 'USD'),
        ('INR', 'INR'),
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(
        max_length=10,
        default='INR',
        choices=CURRENCY)

    def __str__(self):
        return self.name


class Discount(models.Model):
    """Модель скидки"""
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return str(self.amount)


class Tax(models.Model):
    """Модель налога"""
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return str(self.amount)


class Order(models.Model):
    """Модель заказа"""
    items = models.ManyToManyField(Item)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    tax = models.ForeignKey(
        Tax,
        null=True,
        default=None,
        on_delete=models.SET_DEFAULT)
    discount = models.ForeignKey(
        Discount,
        null=True,
        default=None,
        on_delete=models.SET_DEFAULT)

    def calculate_total_price(self):
        item_prices = self.items.values_list('price', flat=True)
        total_price = sum(item_prices)
        if self.discount:
            total_price -= self.discount.amount
        if self.tax:
            total_price *= 1 + self.tax.amount / 100
        self.total_price = Decimal(total_price)

    def save(self, *args, **kwargs):
        self.calculate_total_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id}"
