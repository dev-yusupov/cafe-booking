from django.db import models
from django.core.validators import MinValueValidator


class Order(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_READY = 'ready'
    STATUS_PAID = 'paid'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'В ожидании'),
        (STATUS_READY, 'Готово'),
        (STATUS_PAID, 'Оплачено'),
    ]

    id = models.AutoField(primary_key=True, editable=False)
    table_number = models.IntegerField(validators=[MinValueValidator(1)], db_index=True)
    items = models.JSONField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    def save(self, *args, **kwargs):
        self._calculate_total_price()
        super().save(*args, **kwargs)

    def _calculate_total_price(self):
        self.total_price = sum(item['price'] * item['quantity'] for item in self.items)

    def __str__(self):
        return f"Order {self.id} at table {self.table_number}"
