from rest_framework import generics, status
from .serializers import *
from rest_framework import permissions
from rest_framework.response import Response
from django.utils import timezone
from data_import.get_data import get_top_products
from ..authentication.permission_classes import IsAuthenticatedCustom

def check_expired_sales():
    """
    Checks for expired sales and sets their 'active' flag to False.
    """
    today = timezone.now().date()
    expired_sales = Sale.objects.filter(expiration_date__lt=today, active=True)
    expired_sales.update(active=False)


class CategoryView(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            mans = self.get_queryset()
            ser = self.get_serializer(mans, many=True)
            return Response(
                {"status": True,
                 "code": 200,
                 "data": ser.data,
                 "message": []}, status=status.HTTP_200_OK
            )
        except Exception as exx:
            return Response(
                {"status": True,
                 "code": 200,
                 "data": [],
                 "message": [str(exx)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class SubCategoryView(generics.ListAPIView):
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        return SubCategory.objects.all()

    def list(self, request, *args, **kwargs):
        mans = self.get_queryset()
        ser = self.get_serializer(mans, many=True)
        return Response(
            {"status": True,
             "code": 200,
             "data": ser.data,
             "message": []}
        )


class ManufacturerView(generics.ListAPIView):
    serializer_class = ManufacturerSerializer

    def get_queryset(self):
        return Manufacturer.objects.all()

    def list(self, request, *args, **kwargs):
        mans = self.get_queryset()
        ser = self.get_serializer(mans, many=True)
        return Response(
            {"status": True,
             "code": 200,
             "data": ser.data,
             "message": []}
        )


class SaleView(generics.ListAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    def get_queryset(self):
        return Sale.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            mans = self.get_queryset()
            ser = self.get_serializer(mans, many=True)
            return Response(
                {"status": True,
                 "code": 200,
                 "data": ser.data,
                 "message": []}, status=status.HTTP_200_OK
            )
        except Exception as exx:
            return Response(
                {"status": True,
                 "code": 200,
                 "data": [],
                 "message": [str(exx)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserSaleView(generics.ListAPIView):
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        check_expired_sales()
        user = self.request.user
        active_user_sales = UserSale.objects.filter(user=user, is_full=False)
        active_sales = Sale.objects.filter(active=True, id__in=active_user_sales.values_list('sale_id', flat=True))
        return active_sales

    def list(self, request, *args, **kwargs):
        try:
            mans = self.get_queryset()
            ser = self.get_serializer(mans, many=True)
            return Response(
                {"status": True,
                 "code": 200,
                 "data": ser.data,
                 "message": []}, status=status.HTTP_200_OK,
            )
        except Exception as exx:
            return Response(
                {"status": True,
                 "code": 200,
                 "data": [],
                 "message": [str(exx)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProductView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        category_id = self.request.GET.get('category_id')
        subcategory_id = self.request.GET.get('subcategory_id')
        brand_id = self.request.GET.get('brand_id')

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if subcategory_id:
            queryset = queryset.filter(subcategory_id=subcategory_id)

        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)

        return queryset

    def list(self, request, *args, **kwargs):
        try:
            page = request.query_params.get('page')
            page_size = request.query_params.get('page_size')

            queryset = self.get_queryset()

            page = int(page) if page else 1
            page_size = int(page_size) if page_size else 10

            if page < 1:
                page = 1
            if page_size < 1 or page_size > 100:
                page_size = 10

            start_index = (page - 1) * page_size
            end_index = start_index + page_size
            paginated_queryset = queryset[start_index:end_index]

            serializer = ProductSerializer(paginated_queryset, many=True)

            return Response(
                {"status": True,
                 "code": 200,
                 "data": serializer.data,
                 "message": []}
            )
        except Exception as exx:
            return Response(
                {"status": True,
                 "code": 200,
                 "data": [],
                 "message": [str(exx)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TopProductAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        top_products = get_top_products()
        item_codes = [item['ItemCode'] for item in top_products['value']]
        if item_codes:
            queryset = queryset.filter(itemcode__in=item_codes)
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            mans = self.get_queryset()
            ser = self.get_serializer(mans, many=True)
            return Response(
                {"status": True,
                 "code": 200,
                 "data": ser.data,
                 "message": []}
            )
        except Exception as exx:
            return Response(
                {"status": True,
                 "code": 200,
                 "data": [],
                 "message": [str(exx)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OrderView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        user = self.request.user
        orders = Order.objects.filter(user=user)
        return orders

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            response_data = []
            for order in queryset:
                order_details = OrderDetail.objects.filter(order=order)
                order_detail_serializer = OrderDetailSerializer(order_details, many=True)
                order_data = serializer.data[queryset.index(order)]
                order_data['order_details'] = order_detail_serializer.data
                response_data.append(order_data)
            return Response(
                {"status": True,
                 "code": 200,
                 "data": response_data,
                 "message": []}
            )
        except Exception as exx:
            return Response(
                {"status": True,
                 "code": 200,
                 "data": [],
                 "message": [str(exx)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        orders = Order.objects.filter(user=user)
        return orders

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)

            order_details = OrderDetail.objects.filter(order=instance)
            order_detail_serializer = OrderDetailSerializer(order_details, many=True)
            response_data = serializer.data
            response_data['order_details'] = order_detail_serializer.data

            return Response(
                {"status": True,
                 "code": 200,
                 "data": response_data,
                 "message": []}
            )
        except Exception as exx:
            return Response(
                {"status": True,
                 "code": 200,
                 "data": [],
                 "message": [str(exx)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserTotalStatusView(generics.ListAPIView):
    serializer_class = UserTotalStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return []

    def list(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(context={'request': request})
            return Response(
                {"status": True,
                 "code": 200,
                 "data": serializer.data,
                 "message": []}, status=status.HTTP_200_OK
            )
        except Exception as exx:
            return Response(
                {"status": True,
                 "code": 200,
                 "data": [],
                 "message": [str(exx)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id).first()

    def list(self, request, *args, **kwargs):
        try:
            mans = self.get_queryset()
            ser = self.get_serializer(mans, many=True)
            return Response(
                {"status": True,
                 "code": 200,
                 "data": ser.data,
                 "message": []}, status=status.HTTP_200_OK
            )
        except Exception as exx:
            return Response(
                {"status": True,
                 "code": 200,
                 "data": [],
                 "message": [str(exx)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DashboardListView(generics.ListAPIView):

    def get_queryset(self):
        queryset = Product.objects.all()
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = Product.objects.all()
            top_products = get_top_products()
            item_codes = [item['ItemCode'] for item in top_products['value']]
            top_queryset = queryset.filter(itemcode__in=item_codes)


        except Exception as exx:
            return Response(
                {"status": True,
                 "code": 200,
                 "data": [],
                 "message": [str(exx)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

