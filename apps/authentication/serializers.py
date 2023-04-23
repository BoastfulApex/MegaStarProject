from rest_framework import serializers
from .models import MegaUser


class PhoneVerifySerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate(self, attrs):
        phone = attrs['phone']
        data = MegaUser.objects.get(phone=phone)
        if not data:
            raise serializers.ValidationError({"Error": "Mijozlar bazasida bu telefon raqamga mos ma'lumotlartopilmadi!"})
        return attrs

