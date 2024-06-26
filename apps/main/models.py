from django.db import models
from apps.authentication.models import MegaUser as User
from apps.home.models import BaseModel
from datetime import datetime, timedelta
from urllib.parse import unquote

MONTH, SEASON, YEAR = (
    "month",
    "season",
    "year"
)


class Cashback(models.Model):
    PERIOD_TYPES = (
        (MONTH, MONTH),
        (SEASON, SEASON),
        (YEAR, YEAR)
    )

    name = models.CharField(max_length=500, null=True, blank=True)
    period = models.CharField(max_length=50, null=True, blank=True, choices=PERIOD_TYPES)
    summa = models.IntegerField(default=0)
    persent = models.IntegerField(default=1)


class UserCashback(BaseModel):
    PERIOD_TYPES = (
        (MONTH, MONTH),
        (SEASON, SEASON),
        (YEAR, YEAR)
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    cashback = models.ForeignKey(Cashback, on_delete=models.SET_NULL, null=True)
    expiration_date = models.DateTimeField(null=True)
    period = models.CharField(max_length=50, null=True, blank=True, choices=PERIOD_TYPES)
    summa = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.period == MONTH:
                self.expiration_date = self.created_date + timedelta(days=30)
            elif self.period == SEASON:
                self.expiration_date = self.created_date + timedelta(days=90)
            elif self.period == YEAR:
                self.expiration_date = self.created_date + timedelta(weeks=52)

        super(UserCashback, self).save(*args, **kwargs)


class Category(BaseModel):
    image = models.FileField(null=True)

    groupname = models.CharField(max_length=2000, null=True)
    number = models.CharField(max_length=2000, null=True)

    @property
    def PhotoURL(self):
        try:
            return self.image.url
        except:
            return ''

    def __str__(self):
        return self.groupname


class SubCategory(BaseModel):
    image = models.FileField(null=True)

    name = models.CharField(max_length=2000, null=True)
    code = models.CharField(max_length=2000, null=True)
    # u_group = models.CharField(max_length=2000, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    @property
    def PhotoURL(self):
        try:
            return self.image.url
        except:
            return ''

    def __str__(self):
        return self.name


class Manufacturer(BaseModel):
    image = models.FileField(null=True)

    manufacturer_name = models.CharField(max_length=2000, null=True)
    code = models.CharField(max_length=2000, null=True)

    def __str__(self):
        return self.manufacturer_name


class WareHouse(BaseModel):
    warehouse_code = models.CharField(max_length=1000, null=True, blank=True)
    warehouse_name = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.warehouse_name


class SalesEmployee(BaseModel):
    employee_code = models.IntegerField(null=True)
    employee_name = models.CharField(max_length=1000, null=True, blank=True)
    warehouse = models.ForeignKey(WareHouse, on_delete=models.CASCADE, null=True, blank=True)


class Product(BaseModel):
    itemcode = models.CharField(max_length=100, null=True, blank=True)
    itemname = models.CharField(max_length=2000, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, null=True, blank=True)

    image = models.FileField(null=True, blank=True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    price = models.FloatField()
    order_sale = models.IntegerField(default=0, null=True)
    top = models.BooleanField(null=True, blank=True, default=False)

    def __str__(self):
        return self.itemname


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    is_sale = models.BooleanField(default=False)
    summa = models.FloatField(default=0)
    u_sumuzs = models.FloatField(default=0, null=True)

    doc_entry = models.CharField(max_length=100, null=True, blank=True)
    doc_num = models.CharField(max_length=2000, null=True, blank=True)
    pay_type = models.IntegerField(null=True, blank=True)
    sales_employee = models.ForeignKey(SalesEmployee, on_delete=models.SET_NULL, null=True, blank=True)
    warehouse = models.ForeignKey(WareHouse, on_delete=models.SET_NULL, null=True, blank=True)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()
    total = models.FloatField(default=0, null=True)
    total_uzs = models.FloatField(default=0, null=True)
    location = models.CharField(max_length=1000, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.order.summa += self.product.price
            self.order.save()
        super(OrderDetail, self).save(*args, **kwargs)


class Sale(BaseModel):
    name = models.CharField(max_length=10000, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    expiration_date = models.DateField(null=True, blank=True)
    required_quantity = models.IntegerField()

    image = models.ImageField(null=True, blank=True)
    description = models.CharField(max_length=5000, null=True, blank=True)

    gift_product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="gift_product")
    gift_quantity = models.IntegerField()

    active = models.BooleanField(default=True)
    orders = models.IntegerField(default=0)

    @property
    def PhotoURL(self):
        try:
            return self.image.url
        except:
            return ''


class UserSale(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    order_quantity = models.IntegerField(default=0)
    is_full = models.BooleanField(default=False)


class News(BaseModel):
    name = models.CharField(max_length=10000, null=True, blank=True)
    description = models.TextField(max_length=10000, null=True, blank=True)
    image = models.FileField(null=True, blank=True)


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=4500)


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    summa = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.count <= 0:
            if self.pk:  # Check if the Card object already exists
                self.delete()
        else:
            self.summa = self.product.price * self.count
            super(Card, self).save(*args, **kwargs)


class PromoCode(models.Model):
    promocode = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)
    summa = models.IntegerField()


class Admin(models.Model):
    user_id = models.CharField(max_length=100)


class Notification(models.Model):
    name = models.CharField(max_length=1000, unique=True)
    message = models.TextField(max_length=10000, null=True, blank=True)


class UserCashbackHistory(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    summa = models.IntegerField(default=0)
    order = models.CharField(max_length=500, null=True, blank=True)
    doc_entry = models.CharField(max_length=500, null=True, blank=True)
    doc_num = models.CharField(max_length=500, null=True, blank=True)


class UserComment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=10000)


class AboutUs(models.Model):
    about = models.TextField(max_length=10000)


class StoryCategory(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True)
    index = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.name}'


class Story(models.Model):
    story_category = models.ForeignKey(StoryCategory, null=True, blank=True, on_delete=models.SET_NULL)
    file = models.FileField(null=True)
    title = models.CharField(max_length=1000, null=True)

    @property
    def PhotoURL(self):
        try:
            return self.file.url
        except:
            return ''


class UserLocations(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    longitude = models.CharField(max_length=1000, null=True, blank=True)
    latitude = models.CharField(max_length=1000, null=True, blank=True)
    location = models.CharField(max_length=1000, null=True, blank=True)


class PushToken(models.Model):
    push = models.CharField(max_length=5000, null=True, blank=True)

