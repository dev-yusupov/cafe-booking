from django.contrib import admin
from django.utils.html import format_html
from .models import Order
from typing import Any


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table_number', 'status', 'total_price', 'created_at', 'view_items')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('id', 'table_number')
    readonly_fields = ('total_price', 'created_at', 'updated_at')
    list_per_page = 20
    ordering = ('-created_at',)  # naqo

    # Show items in a formatted way in the admin
    def view_items(self, obj: Any) -> str:
        items = obj.items
        if not items:
            return "No items"
        return format_html(
            """
            <table style="border: 1px solid #ddd; border-collapse: collapse; width: 100%;">
                <thead>
                    <tr>
                        <th style="border: 1px solid #ddd; padding: 8px;">Name</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">Quantity</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">Price</th>
                    </tr>
                </thead>
                <tbody>
                    {}
                </tbody>
            </table>
            """,
            format_html(
                "".join(
                    format_html(
                        "<tr><td style='border: 1px solid #ddd; padding: 8px;'>{}</td><td style='border: 1px solid #ddd; padding: 8px;'>{}</td><td style='border: 1px solid #ddd; padding: 8px;'>${}</td></tr>",
                        item['name'], item['quantity'], item['price']
                    ) for item in items
                )
            )
        )
    view_items.short_description = "Items Ordered"

    # Add a custom action to mark selected orders as paid
    actions = ['mark_as_paid']

    def mark_as_paid(self, request: Any, queryset: Any) -> None:
        updated_count = queryset.update(status=Order.STATUS_PAID)
        self.message_user(
            request,
            f"{updated_count} order(s) marked as paid."
        )
    mark_as_paid.short_description = "Mark selected orders as Paid"

    # Customize the form view
    fieldsets = (
        (None, {
            'fields': ('table_number', 'status', 'items', 'total_price')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


admin.site.register(Order, OrderAdmin)
