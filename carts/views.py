import redis
from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import User
from goods.models import Goods


#添加购物车
class Addcart(APIView):
    def post(self,request):
        user_name=request.data.get('user')
        pid=request.data.get('productID')
        #根据用户名获取用户对象,根据商品id获取商品对象
        try:
            user=User.objects.get(username=user_name)
        except Exception as e:
            return Response({"code":204, "msg":"用户不存在！"})
        try:
            good=Goods.objects.get(id=pid)
        except Exception as e:
            return Response({'msg':'此商品不存在','code':400})
        #链接redis, 写入数据库
        rdb=redis.Redis()
        #构建hash的key
        cart_key='cart_%s'%user.id  #哈希中的key
        cary_selected='cart_selected_%s'%user.id  #集合中的key
        #默认的商品数量
        count=1
        # 判断商品库存
        if good.stock>0:
            num=rdb.hget(cart_key,good.id)
            if num:
                #此时说明此商品在购物车中
                good_count=int(num.decode())
                good_count+=1 #新加的购物车后商品的总数量
                if good_count >good.stock:
                    return Response({'msg':'已超出限购数量','code':202})
                if good_count<=good.stock:
                    rdb.hset(cart_key,good.id,good_count)
                    rdb.sadd(cary_selected,good.id)
                    rdb.close()
                    return Response({'msg':"商品已存在,数量+1","code":201})
            else:
                #此商品没在购物车,可以直接添加到购物车中
                rdb.hset(cart_key,good.id,count)#写入哈希里
                rdb.sadd(cary_selected,good.id)
                rdb.close()
                #把添加到购物车中的商品返回
                shopping_cart_data = {
                    'id':cart_key,
                    'productID':good.id,
                    'productName':good.sku_name,
                    'productImg':good.img,
                    'price':good.selling_price,
                    "num": count,  # 该商品在购物车中的数量
                    "maxNum": good.stock,  # 限购数量
                    "check": True,  # 加购，默认是勾选状态
                }
                return Response({'msg': "添加购物车成功", "code": 200, "shoppingCart": shopping_cart_data})
        else:
            return Response({'code':203,'msg':'库存不足,无法购买'})


#查看购物车
class CartInfo(APIView):
    """
    根据当前登录的用户获取购物车中的商品
    """
    def post(self, request):
        # 1. 获取当前的用户信息,注意:此处是通过全局状态管理获取的username
        user_name = request.data.get('user').get('userName')
        try:
            user = User.objects.get(username=user_name)
        except Exception as e:
            return Response({'msg':'此用户不存在',"code":204})
        # 2. 根据用户信息构建key: hash的key  勾选状态的key
        cart_key = "cart_%s" % user.id  # hash 中的key
        cart_selected = "cart_selected_%s" % user.id  # 集合中的key
        # 3. 从redis中获取当前用户的: hash中存放的商品数量(gid, gcount) 以及集合中勾选或未勾选的商品
        rdb = redis.Redis()
        # 集合中勾选或未勾选的商品: [2,3,4,5]是勾选的商品的id, 取出的是byte字节要转码decode, 转码后是str, 要转换成int
        selected_gid = [ int(i.decode()) for i in rdb.smembers(cart_selected)]
        # 4. 通过判断勾选状态来展示不同的信息
        # 获取hash中存放的商品: gid gocunt   gid gcount eg: 1,10, 2,1, 3,5
        shopping_cart_data = []
        for gid, g_count in  rdb.hgetall(cart_key).items():
            # gid 是商品的id  g_count 是商品的数量
            gid = int(gid.decode())
            g_count = int(g_count.decode())
            # 判断gid 是否在勾选状态中
            if gid in selected_gid:
                one_good = get_one_good(cart_key,gid,g_count,check=True)
            else:
                one_good = get_one_good(cart_key, gid, g_count, check=False)
            shopping_cart_data.append(one_good)
        return Response({"msg":"获取用户的购物车数据成功","code":200,"shoppingCartData":shopping_cart_data})


def get_one_good(cart_key, gid, count, check=False):
    try:
        good = Goods.objects.get(id=gid)
    except Exception as e:
        return {}
    return {
                    "id": cart_key,
                    "productID": good.id,
                    "productName": good.sku_name,
                    "productImg": good.img,
                    "price": good.selling_price,
                    "num": count,  # 该商品在购物车中的数量
                    "maxNum": good.stock,  # 限购数量
                    "check": check,  # 加购，默认是勾选状态
                }


#更新购物车数量
class Update(APIView):
    def post(self, request):
        """更新购物车商品数量"""
        # 1. 获取前端传来的数据
        user_name = request.data.get('user').get('userName')
        pid = request.data.get('productID')
        good_num = request.data.get('num')
        # 用户判断
        try:
            user = User.objects.get(username=user_name)
        except Exception as e:
            return Response({'msg': '此用户不存在', "code": 204})
        # 2. 根据用户信息构建key: hash的key  勾选状态的key
        cart_key = "cart_%s" % user.id  # hash 中的key
        cart_selected = "cart_selected_%s" % user.id  # 集合中的key
        rdb = redis.Redis()
        # 更新商品的数量
        # 被更新的商品的状态设置为勾选
        try:
            rdb.sadd(cart_selected,pid)
            # 更新数量
            rdb.hset(cart_key,pid, good_num)
            rdb.close()
            return Response({'msg': "更新商品数量成功", "code": 200})
        except:
            return Response({'msg': "更新商品数量失败", "code": 400})

#"""更新购物车商品状态"""
class UpdateCarStatus(APIView):
    def get(self, request):
        # 获取查询字符串中的参数
        pid = request.query_params.get('productID')
        # 此处获取的是购物车id, 是hash中的key
        cart_key = request.query_params.get('cartID')
        status = request.query_params.get('val')
        # 要修改的是集合中的商品状态, key 是cart_selected_uid  v 是 pid
        # 通过购物车id,获取uid 从而获取cart_selected_uid
        print('cart_Key----->', cart_key)
        # 把购物车中cart_key中的用户id,获取
        cart_selected = "cart_selected_%s" % cart_key.split('_')[-1]
        # 连接数据库
        rdb = redis.Redis()
        # 修改状态,接收的是修改后的状态
        # set
        if status == 'true':
            rdb.sadd(cart_selected,pid)
        else:
            rdb.srem(cart_selected,pid)
        rdb.close()
        return Response({"msg":"修改状态成功","code":200})

# """修改全选与否"""
class UpdateAllStatus(APIView):
    def post(self,request):

        cart_key = request.data.get('cartID')
        status = request.data.get('val') # 是修改一后的值
        print(status)
        # 把购物车中cart_key中的用户id,获取
        cart_selected = "cart_selected_%s" % cart_key.split('_')[-1]
        # 连接redis 修改redis集合中的商品
        rdb = redis.Redis()
        # 若status 是true, 说明之前没有勾选,要加到set
        if status == "true":
            # 获取所有的商品id
            goods = rdb.hkeys(cart_key) # [2,,3]
            rdb.sadd(cart_selected, *goods)
        # 若status 是false, 说明之前勾选,要从set中删除
        else:
            rdb.delete(cart_selected) # 删除redis的key
        return Response({"msg": "修改状态成功", "code": 200})


# """删除购物车中商品"""
class DeleateCart(APIView):
    def post(self,request):
        name=request.data.get('user').get('userName')
        gid=request.data.get('productID')
        try:
            user=User.objects.get(username=name)
        except Exception as e:
            return Response({'msg':'此用户不存在',"code":204})
        # 2. 根据用户信息构建key: hash的key  勾选状态的key
        cart_key = "cart_%s" % user.id  # hash 中的key
        cart_selected = "cart_selected_%s" % user.id  # 集合中的key
        # 链接redsi
        rdb = redis.Redis()
        # 删除时: 删除的商品要冲hash 和 集合中全部删除
        try:
            rdb.hdel(cart_key, gid)
            rdb.srem(cart_selected,gid)
            rdb.close()
        except Exception as e:
            return Response({'msg':"删除购物车失败","code":400})
        return Response({'msg':"删除购物车成功","code":200})






