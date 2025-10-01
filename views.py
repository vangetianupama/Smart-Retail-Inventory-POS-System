from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_date
from core.models import Sale
from core.models import Product
from reports.serializers import SalesReportSerializer, LowStockReportSerializer


class SalesReportView(APIView):
    def get(self, request):
        from_date = request.GET.get("from")
        to_date = request.GET.get("to")

        if not from_date or not to_date:
            return Response({"error": "from and to dates are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from_date = parse_date(from_date)
            to_date = parse_date(to_date)
        except Exception:
            return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)

        sales = Sale.objects.filter(created_at__date__gte=from_date, created_at__date__lte=to_date)
        serializer = SalesReportSerializer(sales, many=True)
        return Response(serializer.data)


class LowStockReportView(APIView):
    def get(self, request):
        low_stock_products = Product.objects.filter(quantity__lte=models.F('reorder_level'))
        serializer = LowStockReportSerializer(low_stock_products, many=True)
        return Response(serializer.data)
