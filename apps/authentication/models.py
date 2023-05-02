from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from .managers import UserManager
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
import random


class MegaUser(AbstractUser):
    _validate_phone = RegexValidator(
        regex="(0|91)?[7-9][0-9]{9}",
        message="Telefon raqam Xalqaro Formatda 998YYXXXXXXX ko'rinishida kiritilishi kerak!"
    )
    username = None
    first_name = models.CharField(_("first name"), max_length=150, blank=True, null=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True, null=True)
    email = models.EmailField(_("email address"), blank=True, null=True)

    phone = models.CharField(max_length=15, null=True, unique=True, validators=[_validate_phone])
    telegram_id = models.CharField(max_length=100, null=True, blank=True)

    card_code = models.CharField(max_length=50, null=True, blank=True)
    card_name = models.CharField(max_length=500, null=True, blank=True)

    otp = models.CharField(max_length=10, null=True, blank=True)

    all_cashback = models.IntegerField(default=0)

    is_sale = models.BooleanField(default=False)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return "{}".format(self.phone)

    def generate_otp(self):
        otp = random.randint(111111, 999999)
        self.set_password(str(otp))
        self.otp = otp
        self.save()
        return otp

