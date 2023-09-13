from functools import reduce

import redis
from django.http import JsonResponse
from django.shortcuts import render
from haystack.views import SearchView
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_decode_handler

from rest_framework.pagination import PageNumberPagination

from users.models import User
from .models import Carousel,Category,Goods,GoodsCollect
from .serializer import CarouselSer, GoodsSer, CateSer, GoodImgs, GoodCollectSer


# Create your views here.


class CarouselView(APIView):
    """轮播图"""
    def get(self, request):
        # 获取所有的轮播图
        cars = Carousel.objects.all()
        ser = CarouselSer(cars, many=True)
        return Response(ser.data)


class GoodsByCateName(APIView):
    def post(self, request):
        """
        根据类别名获取商品数据
        """
        name = request.data.get('categoryName')
        # 获取类别信息
        cate = Category.objects.get(cate_name=name)
        # 根据类别获取商品
        goods = cate.goods_set.all()
        # 使用序列化器输出
        good_ser = GoodsSer(goods, many=True)
        return Response(good_ser.data)

# 热门商品
class HotProductViews(APIView):
    def post(self, request):
        # 前端传来的类别信息
        cate_names = request.data.get('categoryName')
        # 根据类别名获取商品类别
        cates = [Category.objects.get(cate_name=name) for name in cate_names ]
        goods = [cate.goods_set.all() for cate in cates]

        # 根据商品销量对商品进行排序
        # map 和reduce 都是把可迭代对象的元素放在func中进行操作,但是返回的结果不一样
        # reduce:(func, iterable)---> 返回的是值
        # map:(func, iterable) ---> 返回的是新的迭代对象[]
        # reduce(lambda x,y: x | y, goods) 会拿到所有商品放在一起的一个列表
        # order_by()默认是升序排列, 我们要降序排列,前面加-
        res = reduce(lambda x, y: x | y, goods).order_by('-count')
        # 对返回的结果进行序列化输出
        ser = GoodsSer(res, many=True)
        return Response(ser.data)


# 1. 获取所有的商品类别
class CategoryView(APIView):
    def post(self, request):
        cates = Category.objects.all()
        ser = CateSer(cates, many=True)
        return Response(ser.data)


#  根据类别id获取此类别下所有的商品
class GoodsByCategoryId(APIView):
    def get(self, request):
        #查询字符串传参
        cate_id = request.query_params['categoryID']
        try:
            cate = Category.objects.get(id=cate_id)
        except Exception  as e:
            return Response({'msg':"没有此类别"})
        #根据类别查商品  反向查询
        goods = cate.goods_set.all()
        good_ser = GoodsSer(goods, many=True)
        return Response(good_ser.data)

#分页
class MyPagenations(PageNumberPagination):
    page_size_query_param = "pageSize"
    page_query_param = "page"
    page_size = 7


# 3. 获取所有的商品
class GoodsViews(ListAPIView):
    queryset = Goods.objects.all()
    serializer_class = GoodsSer

    pagination_class = MyPagenations



#详情
#根据商品id 获取商品图片
class GoodiList(APIView):
    def get(self,request):
        gid = request.query_params.get('gid')
        if gid:
            #根据商品id 获取商品图片
            try:
                good=Goods.objects.get(id=gid)
            except Exception as e:
                return Response({'mag':'没有此商品','code':400})
            #根据商品获取图片
            imgs=good.goodsimg_set.all()
            #进行序列化输出
            str=GoodImgs(imgs,many=True)
            return Response(str.data)
        else:
            #获取失败
            return Response({'mag':'商品图片不存在','code':400})



##根据商品id 获取商品
class GoodsAll(APIView):
    def get(self,request):
        gid = request.query_params.get('gid')
        if gid:
            #根据商品id 获取商品
            try:
                good=Goods.objects.get(id=gid)
            except Exception as e:
                return Response({'mag':'没有此商品','code':400})
            str=GoodsSer(good)
            return Response(str.data)
        else:
            #获取失败
            return Response({'mag':'商品不存在','code':400})



#添加历史浏览记录
class AddHostory(APIView):
    def post(self,request):
        # 获取前端传来的gid 和 token
        gid = request.data.get('productID')
        token = request.data.get('token')
        print("token>>", token)
        # 判断
        if not token:
            # 此时没有token,shuoming 没有登录
            return Response({'msg':"请先登录!","code":400})
        else:
            # 登录过的,需要校验token
            # decode:解码,
            payload = jwt_decode_handler(token)
            # 在payload 中获取登录的用户信息
            print("payload>>>", payload)
            user_id = payload.get('user_id')
            # 把用户信息和商品id写入redis
            redis_cli = redis.Redis()
            # 写入redis: list   history_userid: gid
            history = "history_%s"%user_id
            # 直接添加
            # 若存在此商品直接删除
            redis_cli.lrem(history,0, gid)
            # 删除后添加
            redis_cli.lpush(history,gid)
            redis_cli.close()

            return Response({'msg':"添加历史浏览记录成功","code":200})



#添加收藏
class CollectViews(APIView):
    def post(self,request):
        user=request.data.get('user')
        gid=request.data.get('product_id')
        #判断商品是否存在
        if not user:
            return Response({'msg':"获取用户信息错误","code":400})
        if not gid:
            return Response({"msg": "商品错误", "code": 400})
        try:
            user = User.objects.get(username=user['userName'])
        except Exception as e:
            return Response({'msg':"没有此用户","code":400})
        try:
            good = Goods.objects.get(id=gid)
        except Exception as e:
            return Response({'msg':"没有此商品","code":400})
        good=GoodsCollect.objects.create(user=user,goods=good)
        ser = GoodCollectSer(good)
        return Response({"code": 200, "data": ser.data, "msg": "添加收藏成功"})



#获取收藏的商品
class CollectInfoView(APIView):
    """获取收藏的商品"""
    def post(self,request):
        dict_user = request.data.get("user")
        token = request.data.get('token')
        # print("user>>>",dict_user)
        # 做判断, 判断当前的用户是否在登录的表中
        # 只要有一个为空说明前端传来的数据没有获取到, 此时让用户登录
        if not all([dict_user, token]):
            return Response({"msg":"请先登录","code":400})
        # 判断传来的用户信息和token 中的用户信息是否一致,若一致,才能获取收藏的商品
        try:
            user = User.objects.get(username=dict_user['userName'])
        except Exception as e:
            return Response({'msg':"没有此用户","code":400})
        # 校验token
        payload = jwt_decode_handler(token)
        print("payload>>>", payload)
        user_id = payload.get('user_id')
        # 校验传来的用户user和token中的user是一个,不一个说明用户信息被盗取(篡改),不让登录
        if user_id == user.id:
            # 此时说明登录的用户和传递来的用户一致,才能获取收藏的商品
            products = user.goodscollect_set.all()
            print("product---->", products)
            collect_goods = []
            for product in products:
                collect_goods.append({
                    "id":product.goods.id,
                    'sku_name':product.goods.sku_name,
                    "price":product.goods.price,
                    "selling_price":product.goods.selling_price,
                    "img":product.goods.img,
                    "title":product.goods.title,
                    "instruction":product.goods.instruction
                })
            return Response({'msg':"ok","data":collect_goods, "code":200})
        else:
            return Response({'msg':"用户信息错误, 请先登录","code":400})


#删除收藏
class CollectDelView(APIView):
        def delete(self, request):
            # 1. 获取商品id、登录用户
            pid = request.data.get('product_id')
            dict_user = request.data.get('user')
            try:
                user = User.objects.get(username=dict_user['userName'])
            except Exception as e:
                return Response({'msg': "没有此用户", "code": 400})

            GoodsCollect.objects.filter(user=user, goods_id=pid).delete()

            return Response({"code": 200, 'msg': '删除成功'})




#商品搜索
class MySearchView(SearchView):
    """自定义返回json"""
    def create_response(self):
        # 重载create_response来实现接口编写
        # 返回上下文的数据
        #{' query': '电视', 'form': <ModelSearchForm bound=True, valid=True, fields=(q;models)>,
        # 'page': <Page 1 of 1>, 'paginator': <django.core.paginator.Paginator object at 0x7f7d69a0d0>,
        # 'suggestion': None
        # }
        context = super().get_context()
        # print(">>>context", context)
        # 获取当前的分页
        current_page = context.get("page")
        # 查询结果的分页
        paginator = context.get("paginator")
        goods_list = []
        # print('商品列表>>',current_page.object_list )
        for i in current_page.object_list:
            # 将每一个商品对象放入列表
            goods_list.append(i.object)
        # 对商品列表序列化
        goods_ser = GoodsSer(goods_list, many=True)

        # 返回响应
        return JsonResponse({
            "code": 200,
            "msg": "查询商品成功！",
            "product": goods_ser.data,
            "total": len(goods_list)
        })

