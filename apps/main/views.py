from rest_framework import generics, status
from .serializers import *
from rest_framework import permissions
from rest_framework.response import Response


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
    queryset = UserSale.objects.all()
    serializer_class = UserSaleSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderDetailView(generics.ListAPIView):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

#
# class UserTotalStatusView(generics.ListAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def list(self, request, *args, **kwargs):
#         user_id = request.user.id
#         month = datetime.date.today().month
#         year = datetime.date.today().year
#
#         # Monthly sum
#         monthly = Order.objects.filter(
#             user__telegram_id=user_id,
#             created_date__month=month,
#             created_date__year=year
#         ).aggregate(monthly_sum=Sum('summa'))['monthly_sum'] or 0
#
#         # Yearly sum
#         yearly = Order.objects.filter(
#             user__telegram_id=user_id,
#             created_date__year=year
#         ).aggregate(yearly_sum=Sum('summa'))['yearly_sum'] or 0
#
#         # Seasonal sum
#         start_month = ((month - 1) // 3) * 3
#         end_month = start_month + 2 if start_month != 12 else 12
#         season = Order.objects.filter(
#             user__telegram_id=user_id,
#             created_date__year=year,
#             created_date__month__gte=start_month,
#             created_date__month__lte=end_month
#         ).aggregate(season_sum=Sum('summa'))['season_sum'] or 0
#
#         data = {
#             "monthly": monthly,
#             "season": season,
#             "yearly": yearly
#         }
#         return Response(data, status=status.HTTP_200_OK)
#


class UserTotalStatusView(generics.ListAPIView):
    serializer_class = UserTotalStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return []

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
