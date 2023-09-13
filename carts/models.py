from django.db import models
from users.models import User
from goods.models import Goods
# Create your models here.
class Carts(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='用户')
    good = models.ForeignKey(Goods,on_delete=models.CASCADE,verbose_name='商品')
    selected=models.BooleanField(default=True,verbose_name='勾选状态')
    good_count = models.IntegerField(verbose_name='商品数量')

    class Meta:
        db_table='tb_cart'
        verbose_name_plural='商品信息'
