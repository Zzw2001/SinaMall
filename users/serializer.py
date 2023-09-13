from rest_framework import serializers
from .models import Address,User


class UserSer(serializers.ModelSerializer):
    """用户序列化器"""

    class Meta:
        model = User
        fields = "__all__"


class AddressSer(serializers.ModelSerializer):
    """收货地址"""
    class Meta:
        model = Address
        fields = "__all__"