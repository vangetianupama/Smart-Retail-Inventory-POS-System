from rest_framework import serializers
from core.models import Sale, SalesItem
from core.models import Product

class SalesReportSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = ['id', 'cashier_id', 'total', 'tax_total', 'discount_total', 'payment_mode', 'created_at', 'items']

    def get_items(self, obj):
        return [
            {
                "product": item.product.name,
                "quantity": item.quantity,
                "unit_price": str(item.unit_price),
                "total": str(item.total),
            }
            for item in obj.items.all()
        ]


class LowStockReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'quantity', 'reorder_level']
