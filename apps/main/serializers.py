from django.db.models import Sum
from rest_framework import serializers
from .models import *
from rest_framework.exceptions import NotFound
from django.utils.translation import gettext_lazy as _
from data_import.get_data import get_kurs_valyuta


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    # def to_representation(self, instance):
    #     # Get the original representation of the instance
    #     data = super(ProductSerializer, self).to_representation(instance)
    #     kurs = get_kurs_valyuta()
    #
    #     # Increase the price by 2 times
    #     data['price'] *= 2
    #
    #     return data


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'


class PromocodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'


class UserCashbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCashback
        fields = '__all__'


class UserSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSale
        fields = ['id', 'user', 'sale', 'order_quantity', 'created_date', 'is_full']


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'name', 'description', 'image', 'created_date']


class UserCashbackHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCashbackHistory
        fields = ['id', 'summa', 'user', 'created_date']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'card_code', 'card_name', 'phone', 'all_cashback']


class UserTotalStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cashback
        fields = "__all__"
    # monthly = serializers.DecimalField(max_digits=10, decimal_places=2)
    # seasonal = serializers.DecimalField(max_digits=10, decimal_places=2)
    # yearly = serializers.DecimalField(max_digits=10, decimal_places=2)
    #
    # def to_representation(self, instance):
    #     user_id = self.context['request'].user.id
    #     month = datetime.date.today().month
    #     year = datetime.date.today().year
    #
    #     # Monthly sum
    #     monthly = Order.objects.filter(
    #         user__telegram_id=user_id,
    #         created_date__month=month,
    #         created_date__year=year
    #     ).aggregate(monthly_sum=Sum('summa'))['monthly_sum'] or 0
    #
    #     # Yearly sum
    #     yearly = Order.objects.filter(
    #         user__telegram_id=user_id,
    #         created_date__year=year
    #     ).aggregate(yearly_sum=Sum('summa'))['yearly_sum'] or 0
    #
    #     # Seasonal sum
    #     start_month = ((month - 1) // 3) * 3
    #     end_month = start_month + 2 if start_month != 12 else 12
    #     season = Order.objects.filter(
    #         user__telegram_id=user_id,
    #         created_date__year=year,
    #         created_date__month__gte=start_month,
    #         created_date__month__lte=end_month
    #     ).aggregate(season_sum=Sum('summa'))['season_sum'] or 0
    #
    #     return {
    #         "monthly": monthly if monthly is not None else 0,
    #         "seasonal": season if season is not None else 0,
    #         "yearly": yearly if yearly is not None else 0
    #     }


class PromoCodeStatusSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=200)


class QrCodeSerializer(serializers.Serializer):
    card_code = serializers.CharField(max_length=100)
    cashback = serializers.IntegerField()
    doc_entry = serializers.CharField(max_length=100)
    doc_num = serializers.CharField(max_length=100)

    def validate(self, attrs):
        card_code = attrs.get('card_code')
        cashback = attrs.get('cashback')

        user = User.objects.filter(card_code=card_code).first()
        if not user:
            msg = _('Foydalanuvchi topilmadi')
            raise serializers.ValidationError(msg)
        elif user.all_cashback < int(cashback):
            msg = _('Foydalanuvchida keshbek miqdori yetarli emas')
            raise serializers.ValidationError(msg)

        return attrs


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'


class UserCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserComment
        fields = '__all__'


class AboutSerializer(serializers.ModelSerializer):

    class Meta:
        model = AboutUs
        fields = '__all__'


class StorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Story
        fields = '__all__'


class UserLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocations
        fields = "__all__"


class AddOrderSerializer(serializers.Serializer):
    pay_type = serializers.IntegerField()
    location = serializers.CharField(max_length=10000)


class PushTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushToken
        fields = '__all__'
