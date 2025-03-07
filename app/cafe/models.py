from typing import List
from django.db import models
from django.core.validators import MinValueValidator

class Order(models.Model):
    """
    Model representing an order in the cafe.
    """

    STATUS_PENDING: str = "pending"
    STATUS_READY: str = "ready"
    STATUS_PAID: str = "paid"

    STATUS_CHOICES: List = [
        (STATUS_PENDING, "Pending"),
        (STATUS_READY, "Ready"),
        (STATUS_PAID, "Paid"),
    ]

    id = models.AutoField(primary_key=True, editable=False)
    table_number = models.IntegerField(validators=[MinValueValidator(1)], db_index=True)
    items = models.JSONField()
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False, default=0
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING, db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    def save(self, *args, **kwargs) -> None:
        """
        Save the order instance, calculating the total price.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        self._calculate_total_price()
        super().save(*args, **kwargs)

    def _calculate_total_price(self) -> float:
        """
        Calculate the total price of the order.

        Returns:
            float: The total price of the order.
        """
        self.total_price = sum(
            item["price"] * item["quantity"] for item in self.items if "price" in item
        )

    def get_status_display(self) -> str:
        """
        Get the display value for the order status.

        Returns:
            str: The display value for the status.
        """
        return dict(self.STATUS_CHOICES).get(self.status, "Unknown")

    def __str__(self) -> str:
        """
        Get the string representation of the order.

        Returns:
            str: The string representation of the order.
        """
        return f"Order {self.id} at table {self.table_number}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"
