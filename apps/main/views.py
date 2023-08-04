from rest_framework import generics, status
from .serializers import *
from rest_framework.response import Response
from django.utils import timezone
from data_import.get_data import get_top_products, get_kurs_valyuta
from ..authentication.permission_classes import IsAuthenticatedCustom
from auth_models import viewlist
from django.http import HttpResponse
import random
import datetime


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
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return Sale.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            sales = Sale.objects.filter(active=True).all()
            response_data = []
            for sale in sales:
                user_order_quantity = 0
                user_sale = UserSale.objects.filter(user=request.user, sale=sale).first()
                if user_sale:
                    user_order_quantity = user_sale.order_quantity
                sale_data = {
                    "id": sale.id,
                    "name": sale.name,
                    "product_id": sale.product.id,
                    "expiration_date": sale.expiration_date,
                    "required_quantity": sale.required_quantity,
                    "gift_product_id": sale.gift_product.id,
                    "gift_quantity": sale.gift_quantity,
                    "user_order_quantity": user_order_quantity,
                }
                response_data.append(sale_data)
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


class UserSaleView(viewlist.ListCreateAPIView):
    serializer_class = UserSaleSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        check_expired_sales()
        user = self.request.user
        active_user_sales = UserSale.objects.filter(user=user, is_full=False)
        active_sales = Sale.objects.filter(active=True, id__in=active_user_sales.values_list('sale_id', flat=True))
        return active_sales


class UserSaleDetailView(viewlist.RetrieveAPIView):
    serializer_class = UserSaleSerializer
    # permission_classes = [IsAuthenticatedCustom]


class ProductView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all().order_by('id')

        category_id = self.request.GET.get('category_id')
        subcategory_id = self.request.GET.get('subcategory_id')
        brand_id = self.request.GET.get('brand_id')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        order_by = self.request.GET.get('order_by')  # 'asc' or 'desc'
        search = self.request.GET.get('search')

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if subcategory_id:
            queryset = queryset.filter(sub_category_id=subcategory_id)

        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)

        if search:
            queryset = queryset.filter(sub_category_id=subcategory_id)

        if min_price and max_price:
            queryset = queryset.filter(itemname__icontains=search)

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
            kurs = get_kurs_valyuta()
            for product in serializer.data:
                product['price'] *= kurs
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


class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class TopProductAPIView(viewlist.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        top_products = get_top_products()
        item_codes = [item['ItemCode'] for item in top_products['value']]
        if item_codes:
            queryset = queryset.filter(itemcode__in=item_codes)
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = ProductSerializer(queryset, many=True)
            kurs = get_kurs_valyuta()
            for product in serializer.data:
                product['price'] *= kurs
            return Response(
                {"status": True,
                 "code": 200,
                 "data": serializer.data,
                 "message": []}
            )
        except Exception as exx:
            return Response(
                {"status": True,
                 "code": 500,
                 "data": [],
                 "message": [str(exx)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SimilarProductView(viewlist.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        product_id = self.request.GET.get('product_id')
        product = generics.get_object_or_404(Product, id=product_id)

        similar_products = Product.objects.filter(category=product.category).exclude(id=product_id)[:5]

        return similar_products

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = ProductSerializer(queryset, many=True)
            kurs = get_kurs_valyuta()
            for product in serializer.data:
                product['price'] *= kurs
            return Response(
                {"status": True,
                 "code": 200,
                 "data": serializer.data,
                 "message": []}
            )
        except Exception as exx:
            return Response(
                {"status": True,
                 "code": 500,
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
                 "code": 500,
                 "data": [],
                 "message": [str(exx)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticatedCustom]

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
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return []

    def list(self, request, *args, **kwargs):
        try:
            user_id = request.user.id
            month = datetime.date.today().month
            year = datetime.date.today().year

            # Monthly sum
            monthly = Order.objects.filter(
                user_id=user_id,
                created_date__month=month,
                created_date__year=year
            ).aggregate(monthly_sum=Sum('summa'))['monthly_sum'] or 0

            # Yearly sum
            yearly = Order.objects.filter(
                user_id=user_id,
                created_date__year=year
            ).aggregate(yearly_sum=Sum('summa'))['yearly_sum'] or 0

            # Seasonal sum
            start_month = ((month - 1) // 3) * 3
            end_month = start_month + 2 if start_month != 12 else 12
            season = Order.objects.filter(
                user_id=user_id,
                created_date__year=year,
                created_date__month__gte=start_month,
                created_date__month__lte=end_month
            ).aggregate(season_sum=Sum('summa'))['season_sum'] or 0
            month_cashback, created = Cashback.objects.get_or_create(
                period="month"
            )
            season_cashback, created = Cashback.objects.get_or_create(
                period="season"
            )

            year_cashback, created = Cashback.objects.get_or_create(
                period="year"
            )
            d_1 = {
                "name": month_cashback.name,
                "need": month_cashback.summa,
                "earn": monthly,
            }
            d_2 = {
                "name": season_cashback.name,
                "need": season_cashback.summa,
                "earn": season,
            }
            d_3 = {
                "name": year_cashback.name,
                "need": year_cashback.summa,
                "earn": yearly,
            }
            data = [d_1, d_2, d_3]
            return Response(
                {"status": True,
                 "code": 200,
                 "data": data,
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
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


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
    permissions = [IsAuthenticatedCustom]

    def get_queryset(self):
        queryset = Card.objects.filter(user=self.request.user).all()
        return queryset

    def create(self, request, *args, **kwargs):
        try:
            card = Card.objects.filter(user=request.data['user'], product=request.data['product']).first()
            if not card:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(
                    {"status": True,
                     "code": 200,
                     "data": serializer.data,
                     "message": []}, status=status.HTTP_200_OK, headers=headers
                )
            else:
                return Response(
                    {"status": True,
                     "code": 200,
                     "data": [],
                     "message": ['Maxsulot savatda bor']}
                )

        except Exception as exx:
            return Response(
                {"status": True,
                 "code": 200,
                 "data": [],
                 "message": [str(exx)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            cards_data = []
            summa = 0
            kurs = get_kurs_valyuta()
            for card in queryset:
                card.summa = card.product.price * card.count
                card.save()
                summa += card.summa
                cards = {
                    'id': card.id,
                    'count': card.count,
                    'summa': card.summa * kurs,
                    'product_id': card.product.id,
                    'product_name': card.product.itemname.encode('utf-8'),
                    'product_image': "http://185.65.202.40:3222/files/" + str(card.product.image) if card.product.image else None,
                }
                cards_data.append(cards)
            response_data = {
                'cards': cards_data,
                'all_summa': summa,
                'objects': len(queryset)
            }
            return Response(
                {"status": True,
                 "code": 200,
                 "data": response_data,
                 "message": []})
        except Exception as exx:
            return Response(
                {"status": True,
                 "code": 500,
                 "data": [],
                 "message": [str(exx)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CardObject(viewlist.RetrieveUpdateDestroyAPIView):
    serializer_class = CardSerializer
    permissions = [IsAuthenticatedCustom]

    def get_queryset(self):
        queryset = Card.objects.filter(user=self.request.user).all()
        return queryset


class AddOrderView(generics.ListCreateAPIView):
    serializer_class = AddOrderSerializer
    permissions = [IsAuthenticatedCustom]

    def get_queryset(self):
        return []

    def create(self, request, *args, **kwargs):
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
        if not request.user.is_superuser:
            return HttpResponse('<html><body></body></html>',
                                status=403)
        else:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data
                card_code = data['card_code']
                cashback = data['cashback']
                user = User.objects.filter(card_code=card_code).first()
                cashback_history = UserCashbackHistory.objects.create(
                    user=user,
                    summa=int(cashback)
                )
                cashback_history.save()
                user.all_cashback = user.all_cashback - int(cashback)
                user.save()
                return Response({'status': 'success'})
            else:
                errors = serializer.errors
                return Response(errors)


class NewsView(viewlist.ListAPIView):
    serializer_class = NewsSerializer
    queryset = News.objects.all()


class UserCashbackHistoryVew(viewlist.ListAPIView):
    serializer_class = UserCashbackHistorySerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return UserCashbackHistory.objects.filter(user=self.request.user)


class NotificationView(viewlist.ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.all()


class UserRecommendation(viewlist.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        user_orders = Order.objects.filter(user=self.request.user).all()
        product_ids = []
        for order in user_orders:
            order_details = OrderDetail.objects.filter(order=order)
            for order_detail in order_details:
                product_ids.append(order_detail.product.id)
        from collections import Counter
        product_frequency = Counter(product_ids)
        recommended_products = sorted(product_frequency, key=product_frequency.get, reverse=True)
        if not recommended_products:
            all_products = Product.objects.all()
            total_products = all_products.count()
            random_indices = random.sample(range(total_products), 10)
            recommended_products = [all_products[index] for index in random_indices]
        return recommended_products[:10]


class Recommendation(viewlist.ListAPIView):
    serializer_class = ProductSerializer
    # permission_classes = IsAuthenticatedCustom

    def get_queryset(self):
        all_products = Product.objects.all()
        total_products = all_products.count()
        random_indices = random.sample(range(total_products), 10)
        random_products = [all_products[index] for index in random_indices]
        return random_products


class CommentView(viewlist.CreateAPIView):
    serializer_class = UserCommentSerializer
    # permission_classes = [IsAuthenticatedCustom]


class AboutUsView(viewlist.ListCreateAPIView):
    serializer_class = AboutSerializer
    queryset = AboutUs.objects.all()


class StoryView(viewlist.ListCreateAPIView):
    serializer_class = StorySerializer
    queryset = Story.objects.all()


class LocationView(viewlist.ListCreateAPIView):
    serializer_class = UserLocationSerializer
    permissions = [IsAuthenticatedCustom]

    def get_queryset(self):
        queryset = UserLocations.objects.filter(user=self.request.user).all()
        return queryset
