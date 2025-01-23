from rest_framework import serializers
from cafe.models import Order

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.
    """

    status_display = serializers.SerializerMethodField()
    items = serializers.JSONField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_status_display(self, obj):
        """
        Get the display value for the order status.

        Args:
            obj (Order): The order instance.

        Returns:
            str: The display value for the status.
        """
        return obj.get_status_display()

    def validate_items(self, value):
        """
        Validate the items field.

        Args:
            value (list): The items value.

        Returns:
            list: The validated items value.

        Raises:
            serializers.ValidationError: If the items value is invalid.
        """
        if not isinstance(value, list):
            raise serializers.ValidationError("Items must be a list.")
        for item in value:
            if not isinstance(item, dict):
                raise serializers.ValidationError("Each item must be a dictionary.")
            if "name" not in item or "price" not in item or "quantity" not in item:
                raise serializers.ValidationError(
                    "Each item must contain 'name', 'price', and 'quantity'."
                )
        return value
