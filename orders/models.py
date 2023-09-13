import datetime

from django.db import models
from users.models import User,Address
from goods.models import Goods


class Order(models.Model):
    order_id = models.CharField(max_length=100, primary_key=True, verbose_name='订单号')
    user = models.ForeignKey(User, related_name='order', on_delete=models.CASCADE,
                             verbose_name='用户')  # related_name用于反向查询 user.order.all()
    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name='收货地址')
    total_amount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='总价')
    freight = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='运费')
    total_count = models.IntegerField(verbose_name='商品总数', default=1)
    pay_method = models.CharField(max_length=10, choices=((1, '支付宝'), (2, '银联')), verbose_name='支付方式')
    pay_status = models.CharField(max_length=10,
                                  default= 0,
                                  choices=((0, '待支付'), (1, '待发货'), (2, '待收货'), (3, '待评价'), (4, '已完成')),
                                  verbose_name='支付状态')
    # 日期可以使用datetime 或time 模块
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')

    def __str__(self):
        return "订单:%s" % self.order_id

    class Meta:
        db_table = 'tb_order'
        verbose_name = '订单表'
        verbose_name_plural = verbose_name


# 订单商品表: id、商品id(外键)、数量、单价、评价、评分、订单id(外键)、是否匿名评价、是否评价
class OrderGoods(models.Model):
    """订单商品"""
    SCORE_CHOICES = (
        (0, '0分'),
        (1, '20分'),
        (2, '40分'),
        (3, '60分'),
        (4, '80分'),
        (5, '100分'),
    )

    good = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="订单商品")
    count = models.IntegerField(default=1, verbose_name="数量")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="单价")
    comment = models.TextField(default="", verbose_name="评价信息")
    score = models.SmallIntegerField(choices=SCORE_CHOICES, default=5, verbose_name='满意度评分')
    order = models.ForeignKey(Order, related_name='orderGood', on_delete=models.CASCADE, verbose_name="订单")
    is_anonymous = models.BooleanField(default=False, verbose_name='是否匿名评价')
    is_commented = models.BooleanField(default=False, verbose_name='是否评价')

    class Meta:
        db_table = "order_goods_table"
        verbose_name = '订单商品表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "订单%s中的商品%s" % (self.order.order_id, self.good.sku_name)