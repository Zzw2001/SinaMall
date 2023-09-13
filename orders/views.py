import datetime
import os
import random

import redis
from alipay import AliPay
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction

from users.models import User,Address
from goods.models import Goods
from zhang import settings
from .models import Order,OrderGoods


PUBLIC_URL = open(os.path.join(settings.BASE_DIR,"utils/alipay_secret/alipay_public_key.pem")).read()
PRIVATE_URL = open(os.path.join(settings.BASE_DIR,"utils/alipay_secret/app_private_key.pem")).read()

class MyAliPay(APIView):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.alipay = AliPay(
            appid='2021000119665007',  #你的支付宝沙箱应用的id
            app_private_key_string=PRIVATE_URL, # 每个人自己的私钥
            alipay_public_key_string=PUBLIC_URL, # 每个人支付宝的公钥
            app_notify_url=None,  # 回调地址
            sign_type='RSA2',  # 签名算法
            debug=True,  # 请求来到支付宝沙箱
        )

    def get_trade_url(self, order_id,total_price):
        """生成下单后支付的地址"""

        order_string = self.alipay.api_alipay_trade_page_pay(
            subject='商家收款',
            out_trade_no=order_id,
            total_amount=total_price,
            return_url='http://127.0.0.1:8000/orders/pay/result/',
            notify_url = 'http://127.0.0.1:8000/orders/pay/result/',
        )
        return 'https://openapi.alipaydev.com/gateway.do?' + order_string



#创建订单
class CreateApp(MyAliPay):
    def post(self, request):
        """创建订单"""
        # 1. 获取前端传来的数据
        name = request.data.get('user').get('userName')
        products = request.data.get('products') # [{"good_id":1,},{"good_id":2}]
        add = request.data.get('addr') # 获取的是地址的id
        payMethod = request.data.get('payMethod')

        # 2. 校验:
        #  1. 用户, 用户地址
        try:
            user = User.objects.get(username=name)
        except Exception as e:
            return Response({'msg':"用户未登录,请先登录","code":400})
        try:
            address = Address.objects.get(id=add)
        except Exception as e:
            return Response({'msg':"请确认收货地址","code":400})
        if payMethod != "1":
            return Response({'msg':"目前仅支持支付宝,其他后续完善","code":400})
        # 3.创建订单id: order_id 使用时间戳

        order_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+str(random.randint(00000000,99999999))+ str(user.id)
        # 总数量和总价格
        total_amount = 0 # 总价格
        total_count = 0 # 总数量
        #  开启事务
        with transaction.atomic():
            # 设置回滚点
            point = transaction.savepoint()
            try:
                # 4,创建订单:
                order = Order.objects.create(
                    order_id=order_id,
                    user_id = user.id,
                    address = address,
                    freight=10,
                    pay_method=payMethod,
                    total_amount=total_amount,
                    total_count = total_count,
                )
                #5.创建订单商品:
                for product in products:
                    print("商品>>>",product)
                    # product 是一个商品对象
                    # 判断库存和购买的商品数量\
                    print("商品id>>>>",product.get('productID'))
                    try:
                        gid = product.get('productID')
                        good= Goods.objects.get(id=int(gid))
                    except Exception as e:
                        return Response({'msg':'该商品已经下架',"code":400})
                    origin_stock = good.stock  # 商品库存
                    origin_count = good.count  # 销量

                    # 若库存不足,应该回滚,订单创建失败, 商品订单也创建失败
                    if product.get('num') > origin_stock:
                        # 商品存在,商品的库存 < 购买的数量, 不能下单
                        transaction.savepoint_rollback(point) # 回滚到订单创建之前
                        return Response({'msg':"该商品库存不足","code":400})
                    # 判断商品的数量 销量 库存是否一样,不一样,不能创建订单及订单商品,

                    result = Goods.objects.filter(
                        id=product.get('productID'),
                        stock=origin_stock,
                        count=origin_count
                    )
                    if not result:
                        # 此时商品已经卖完
                        transaction.savepoint_rollback(point)
                        raise ValueError("前后数据不一致，创建订单失败")
                    # 创建订单商品成功
                    OrderGoods.objects.create(
                        good_id = product.get('productID'),
                        count= product.get('num'),
                        price = product.get('price'),
                        order_id = order_id
                    )
                    # 3. 商品的库存-购买的商品数量
                    new_stock = origin_stock - product.get('num')
                    new_count = origin_count + product.get('num')
                    good.count = new_count
                    good.stock = new_stock
                    good.save() # 更新商品的库存和销量
                    # 商品的总价格和总数量
                    total_count += product.get('num')
                    total_amount += product.get('price') * product.get('num')
                # 更新订单表的总数量和总价格
                freight = 10
                order.total_amount = total_amount + freight
                order.total_count = total_count
                order.pay_status = 0
                order.save()
            except Exception as e:
                transaction.savepoint_rollback(point)
        # 6. 把redis中直径支付的商品从redis中删除
        rdb = redis.Redis()
        cart_key = "cart_%s" % user.id  # hash 中的key
        cart_selected = "cart_selected_%s" % user.id  # 集合中的key
        for i in products:
            # 删除已经支付的商品
            # 从hash中删除商品: key name  --> v
            rdb.hdel(cart_key,i.get('productID'))
            rdb.srem(cart_selected,i.get('productID'))
        rdb.close()

        # 调用生成的支付地址
        trade_url = self.get_trade_url(order_id,order.total_amount)
        return Response({'msg':"下单成功","code":200,"url":trade_url})



class CheckPayResult(MyAliPay):
    def get(self,request):
        """告知买家支付成功"""
        #  获取支付结果的参数
        # 使用query_params 获取支付的结果
        print(request.query_params)
        # 获取订单流水号
        order_id = request.query_params.get('out_trade_no')
        # 根据订单号查询订单的支付结果
        result = self.alipay.api_alipay_trade_query(order_id)
        print(result)
        if result.get('trade_status') == "TRADE_SUCCESS":
            # 此时说明支付成功
            # 修改订单的支付状态
            order = Order.objects.get(order_id=order_id)
            # 支付转台是pay_status
            order.pay_status = 1
            order.save()
            # 此时说明支付成功
            return Response({'msg':"支付成功"})
        else:
            return Response({'msg':"支付失败,重新支付"})
    def post(self,request):
        """
        告知卖家支付的结果
        支付宝沙箱没有这功能,只能等项目上线后才能使用,这里仅做说明
        """
        # 把返回的参数形成字典
        data_dict = {k: v for k, v in request.POST.items()}
        # 获取sign
        sign = data_dict.pop('sign')
        # 对sign进行校验,防止伪造
        result = self.alipay.verify(data_dict,sign)
        if result:
            # 此时说明支付成功
            if data_dict.get("trade_status") == "TRADE_SUCCESS":
                # 支付成功
                # 给支付宝的响应
                return Response({"msg":'支付成功',"code":200})
            else:
                return Response({"msg": '支付失败', "code": 400})
        else:
            return Response({"msg":"您已经被网警关注","code":"200"})


#获取订单详情
class OrderInfo(APIView):
    def post(self,request):
        # 获取前端传来的user
        user = request.data.get('user').get('userName')
        # 判断用户是否存在
        try:
            user =User.objects.get(username=user)
        except Exception as e:
            return Response({'msg':"请先登录","code":204})
        # 获取所有的订单: 根据订单表中的related_name反向查询
        orders = user.order.all()
        order_list = []
        # 根据订单获取商品
        for order in orders:
            # 根据订单获取订单下的商品
            order_goods = order.orderGood.all()
            temp = []
            # 把每个订单的商品存放到dict中
            for order_good in order_goods:
                temp.append({
                    "productID": order_good.good.id,
                    "productName": order_good.good.sku_name,
                    "productImg": order_good.good.img,
                    "productPrice": order_good.good.price,
                    "productNum": order_good.good.count,
                    "orderID": order.order_id,
                    "createdTime": order.created_time,
                    # "payStatus":'待收货',
                    "payStatus": order.get_pay_status_display()
                })
            order_list.append(temp)
        return Response({"msg":"获取订单数据成功！","code":200,"orders":order_list})



class PayOrder(MyAliPay):
    def post(self, request):
        """支付"""
        order_id = request.data.get('orderID')
        total_price = request.data.get('totalPrice')
        # 支付
        url = self.get_trade_url(order_id,total_price)
        return Response({'msg':'去支付',"code":302, 'pay_url':url})




class ChangePayStatusView(APIView):
    def post(self, request):
        """接收前端传来的订单id"""
        order_id = request.data.get('orderID')
        print("订单id>>", order_id)
        # 根据订单id ,查询订单,然后修改订单状态
        try:
            order = Order.objects.get(order_id=order_id)
            order.pay_status = int(order.pay_status) + 1
            order.save()
            return Response({'msg':"修改状态成功","code":200})
        except Exception as e:
            return Response({'msg':"订单不存在","code":400})


class DeleteOrderGoods(APIView):
    def post(self, request):
        """删除订单中的商品"""
        order_id = request.data.get('orderID')
        pid = request.data.get('productID')
        try:
            order = Order.objects.get(order_id=order_id)
        except Exception as e:
            return Response({'msg':"订单不存在","code":400})
        # 订单存在, 判断订单中商品的数量
        goods = order.orderGood.all()
        if len(goods) > 1:
            # 订单商品长度大于1, 说明订单中只要一个商品
            for good in goods:
                if pid == good.id:
                    good.delete()
        else:
            # 订单中只有一个商品
            order.delete()
        return Response({'msg':"删除成功","code":200})