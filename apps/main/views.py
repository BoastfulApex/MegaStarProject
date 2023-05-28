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
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryView(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class ManufacturerView(generics.ListAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer


class SaleView(generics.ListAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer


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
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # pagination_class = MyPagination

    def list(self, request, *args, **kwargs):
        page = request.query_params.get('page')
        page_size = request.query_params.get('page_size')

        # Get the queryset
        queryset = Product.objects.all()

        # If page and page_size are not provided, return full queryset
        if not page and not page_size:
            serializer = ProductSerializer(queryset, many=True)
            return Response(serializer.data)

        # Convert page and page_size to integers and set default values
        page = int(page) if page else 1
        page_size = int(page_size) if page_size else 10

        # Validate page and page_size values
        if page < 1:
            page = 1
        if page_size < 1 or page_size > 100:
            page_size = 10

        # Perform slicing to get paginated queryset
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paginated_queryset = queryset[start_index:end_index]

        # Serialize paginated queryset
        serializer = ProductSerializer(paginated_queryset, many=True)

        # Return response with serialized data
        return Response(serializer.data)


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
        return Response(response_data)


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

        return Response(response_data)


class UserTotalStatusView(generics.ListAPIView):
    serializer_class = UserTotalStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return []

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserPost(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer()
