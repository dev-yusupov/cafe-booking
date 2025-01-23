from rest_framework import serializers
from cafe.models import Order

class OrderSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()
    items = serializers.JSONField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_status_display(self, obj):
        return obj.get_status_display()

    def validate_items(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Items must be a list.")
        for item in value:
            if not isinstance(item, dict):
                raise serializers.ValidationError("Each item must be a dictionary.")
            if 'name' not in item or 'price' not in item or 'quantity' not in item:
                raise serializers.ValidationError("Each item must contain 'name', 'price', and 'quantity'.")
        return value