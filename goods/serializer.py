from rest_framework_jwt.serializers import *
from goods.models import *


class  CarouselSer(serializers.ModelSerializer):
    class Meta:
        model = Carousel
        fields = "__all__"


class GoodsSer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = "__all__"


class GoodImgs(serializers.ModelSerializer):
    class Meta:
        model = GoodsImg
        fields = "__all__"


class CateSer(serializers.ModelSerializer):
    """类别序列化器"""
    class Meta:
        model = Category
        fields = '__all__'

class GoodCollectSer(serializers.ModelSerializer):
    """类别序列化器"""
    class Meta:
        model = GoodsCollect
        fields = '__all__'