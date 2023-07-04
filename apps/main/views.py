from rest_framework import generics, status
from .serializers import *
from rest_framework import permissions
from rest_framework.response import Response
from django.utils import timezone
from data_import.get_data import get_top_products
from ..authentication.permission_classes import IsAuthenticatedCustom
from django.db.models import Q
from auth_models import viewlist
from django.http import HttpResponse


def check_expired_sales():
    """
    Checks for expired sales and sets their 'active' flag to False.
    """
    today = timezone.now().date()
    expired_sales = Sale.objects.filter(expiration_date__lt=today, active=True)
    expired_sales.update(active=False)


class CategoryView(viewlist.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()


class SubCategoryView(viewlist.ListAPIView):
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        queryset = SubCategory.objects.all()
        category_id = self.request.GET.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset


class ManufacturerView(viewlist.ListAPIView):
    serializer_class = ManufacturerSerializer

    def get_queryset(self):
        return Manufacturer.objects.all()


class SaleView(viewlist.ListAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    def get_queryset(self):
        return Sale.objects.all()


class UserSaleView(viewlist.ListAPIView):
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        check_expired_sales()
        user = self.request.user
        active_user_sales = UserSale.objects.filter(user=user, is_full=False)
        active_sales = Sale.objects.filter(active=True, id__in=active_user_sales.values_list('sale_id', flat=True))
        return active_sales


class ProductView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()

        category_id = self.request.GET.get('category_id')
        subcategory_id = self.request.GET.get('subcategory_id')
        brand_id = self.request.GET.get('brand_id')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        order_by = self.request.GET.get('order_by')  # 'asc' or 'desc'

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if subcategory_id:
            queryset = queryset.filter(sub_category_id=subcategory_id)

        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)

        if min_price and max_price:
            queryset = queryset.filter(
                Q(price__gte=min_price) & Q(price__lte=max_price)
            )
        elif min_price:
            queryset = queryset.filter(price__gte=min_price)
        elif max_price:
            queryset = queryset.filter(price__lte=max_price)

        if order_by == 'asc':
            queryset = queryset.order_by('price')
        elif order_by == 'desc':
            queryset = queryset.order_by('-price')

        return queryset

    def list(self, request, *args, **kwargs):
        try:
            page = request.query_params.get('page')
            page_size = request.query_params.get('page_size')

            queryset = self.get_queryset()

            page = int(page) if page else 1
            page_size = int(page_size) if page_size else 10

            if page <= 1:
                page = 1
            if page_size < 1 or page_size > 100:
                page_size = 10
            max_page = len(queryset) // 10 + 1
            next_page = ""
            previous_page = ""
            if page > 1:
                previous_page = f"http://185.65.202.40:3222/api/products/?page={page-1}"
            if page < max_page:
                next_page = f"http://185.65.202.40:3222/api/products/?page={page+1}"

            start_index = (page - 1) * page_size
            end_index = start_index + page_size
            paginated_queryset = queryset[start_index:end_index]
            serializer = ProductSerializer(paginated_queryset, many=True)
            data = {
                'page': page,
                'max_page': max_page,
                'previous_page': previous_page,
                'next_page': next_page,
                'results': serializer.data
            }
            return Response(
                {"status": True,
                 "code": 200,
                 "data": data,
                 "message": []}
            )
        except Exception as exx:
            return Response(
                {"status": True,
                 "code": 500,
                 "data": [],
                 "message": [str(exx)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TopProductAPIView(viewlist.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        top_products = get_top_products()
        item_codes = [item['ItemCode'] for item in top_products['value']]
        if item_codes:
            queryset = queryset.filter(itemcode__in=item_codes)
        return queryset


class SimilarProductView(viewlist.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        product_id = self.request.GET.get('product_id')
        product = generics.get_object_or_404(Product, id=product_id)

        similar_products = Product.objects.filter(category=product.category).exclude(id=product_id)[:5]

        return similar_products


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
                 "code": 500,
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
                 "code": 500,
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
                 "code": 500,
                 "data": [],
                 "message": [str(exx)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserListView(viewlist.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id).first()


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
                 "code": 500,
                 "data": [],
                 "message": [str(exx)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CardView(viewlist.ListCreateAPIView):
    serializer_class = CardSerializer
    permissions = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Card.objects.filter(user=self.request.user).all()
        return queryset


class CardObject(viewlist.RetrieveUpdateAPIView):
    serializer_class = CardSerializer
    permissions = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Card.objects.filter(user=self.request.user).all()
        return queryset


class AddOrderView(generics.ListAPIView):
    serializer_class = UserSerializer
    permissions = [permissions.IsAuthenticated]

    def get_queryset(self):
        return []

    def list(self, request, *args, **kwargs):
        try:
            cards = Card.objects.filter(user=request.user)
            for card in cards:
                card.delete()
            return Response(
                {"status": True,
                 "code": 200,
                 "data": 'Xarid amalga oshirildi',
                 "message": []}
            )
        except Exception as exx:
            return Response(
                {"status": True,
                 "code": 500,
                 "data": [],
                 "message": [str(exx)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SaleProducts(viewlist.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(sale__gt=0).all()


class CheckPromoCode(generics.CreateAPIView):
    serializer_class = PromoCodeStatusSerializer

    def create(self, request, *args, **kwargs):
        code = request.data['code']
        promo_code = PromoCode.objects.get(promocode=code)
        if not promo_code:
            return Response(
                {"status": True,
                 "code": 404,
                 "data": [],
                 "message": "Not found"}, status=status.HTTP_404_NOT_FOUND
            )
        else:
            return Response(
                {"status": True,
                 "code": 200,
                 "data": promo_code.values(),
                 "message": []}, status=status.HTTP_200_OK
            )


class QrCodeView(generics.CreateAPIView):
    serializer_class = QrCodeSerializer

    def get_queryset(self):
        return []

    def create(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return HttpResponse('<html><body></body></html>',
                                status=403)
        else:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data
                card_code = data['card_code']
                cashback = data['cashback']
                user = User.objects.filter(card_code=card_code)
                user.all_cashback = user.all_cashback - int(cashback)
                user.save()

            return Response({'status': 'success'})
