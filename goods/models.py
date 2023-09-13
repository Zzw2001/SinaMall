from django.db import models
from users.models import User
from rest_framework.viewsets import ModelViewSet

class Category(models.Model):
    """商品类别"""
    cate_name = models.CharField(max_length=20, verbose_name='类别名字')

    class Meta:
        db_table = 'category'
        verbose_name_plural = "商品类别"

    def __str__(self):
        return self.cate_name


class Goods(models.Model):
    # 商品名字
    sku_name = models.CharField(max_length=100, verbose_name='商品名字')
    price = models.DecimalField(max_digits=13, decimal_places=2, verbose_name="商品价格")
    selling_price = models.DecimalField(max_digits=13, decimal_places=2, verbose_name="商品销售价格")
    img = models.CharField(max_length=200, verbose_name="商品默认图片")
    title = models.CharField(max_length=30, verbose_name="商品标题", null=True)
    instruction = models.TextField(verbose_name="商品的描述信息")
    # 商品销售数量
    count = models.IntegerField(verbose_name="商品销售数量", default=0)
    # 商品的库存
    stock = models.IntegerField(verbose_name="商品库存数量", default=0)
    # 商品所属类别
    cate = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='商品类别')

    # 是否在售
    online = models.BooleanField("是否在售", default=True)

    class Meta:
        db_table = 'goods'
        verbose_name_plural = "商品信息"

    def __str__(self):
        return self.sku_name


class GoodsImg(models.Model):
    # 图片地址
    img = models.CharField(max_length=200, verbose_name='图片')
    # 图片描述
    title = models.CharField(max_length=20, verbose_name="图片的描述", null=True)
    # 图片展示的商品
    good = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品所属图片")

    class Meta:
        db_table = "goodimg"

    def __str__(self):
        return self.title


class Carousel(models.Model):
    imgPath = models.CharField("图片地址", max_length=400, null=False)
    describes = models.CharField("图片描述", max_length=100, null=False)
    def __str__(self):
        return '轮播图%d'%self.id

    class Meta:
        db_table = "carousel_t"
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name



class GoodsCollect(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='用户')
    goods = models.ForeignKey(to=Goods, on_delete=models.CASCADE, verbose_name='商品')

    class Meta:
        db_table = 'goods_collect'
        verbose_name = '商品收藏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s:%s' % (self.user.username, self.goods.sku_name)