from rest_framework import generics, status
from .serializers import *
from rest_framework import permissions
from rest_framework.response import Response
from django.utils import timezone


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
        mans = self.get_queryset()
        ser = self.get_serializer(mans, many=True)
        return Response(
            {"status": True,
             "code": 200,
             "data": ser.data,
             "message": []}
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
        mans = self.get_queryset()
        ser = self.get_serializer(mans, many=True)
        return Response(
            {"status": True,
             "code": 200,
             "data": ser.data,
             "message": []}
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
        mans = self.get_queryset()
        ser = self.get_serializer(mans, many=True)
        return Response(
            {"status": True,
             "code": 200,
             "data": ser.data,
             "message": []}
        )


class ProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # pagination_class = MyPagination

    def list(self, request, *args, **kwargs):
        page = request.query_params.get('page')
        page_size = request.query_params.get('page_size')

        # Get the queryset
        queryset = Product.objects.all()

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


class TopProductAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        itemcodes = self.request.GET.getlist('itemcodes')
        if itemcodes:
            queryset = queryset.filter(itemcode__in=itemcodes)
        return queryset


class OrderView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        orders = Order.objects.filter(user=user)
        return orders

    def list(self, request, *args, **kwargs):
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


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        orders = Order.objects.filter(user=user)
        return orders

    def retrieve(self, request, *args, **kwargs):
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


class UserTotalStatusView(generics.ListAPIView):
    serializer_class = UserTotalStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return []

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(context={'request': request})
        return Response(
            {"status": True,
             "code": 200,
             "data": serializer.data,
             "message": []}
        )


class UserPost(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
