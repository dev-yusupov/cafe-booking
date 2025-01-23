from typing import List
from django.db import models
from django.core.validators import MinValueValidator


class Order(models.Model):
    STATUS_PENDING: str = 'pending'
    STATUS_READY: str = 'ready'
    STATUS_PAID: str = 'paid'

    STATUS_CHOICES: List = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_READY, 'Ready'),
        (STATUS_PAID, 'Paid'),
    ]

    id = models.AutoField(primary_key=True, editable=False)
    table_number = models.IntegerField(validators=[MinValueValidator(1)], db_index=True)
    items = models.JSONField(db_index=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    def save(self, *args, **kwargs) -> None:
        self._calculate_total_price()
        super().save(*args, **kwargs)

    def _calculate_total_price(self) -> float:
        self.total_price = sum(item['price'] * item['quantity'] for item in self.items)

    def __str__(self) -> str:
        return f"Order {self.id} at table {self.table_number}"
