import random
import string
import redis
from django.http.response import JsonResponse
from django.contrib.auth.hashers import check_password, make_password
from django.http.response import HttpResponse
from django.contrib.auth import authenticate
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_payload_handler,jwt_encode_handler

from .models import User,Address
from captcha.image import ImageCaptcha
from .serializer import UserSer,AddressSer

# 注册
# ApiView GenericApiView, CreateApiView  视图集

#"""生成图片验证码"""
class GenerateImageCode(APIView):
    def get(self,request,imagecodeid):
        """生成图片验证码"""
        #1.接收前端传来的uuid，图片id
        #2.使用随机模块生成: 字符+数字的随机数，长度6
        #3.使用capch模块生成图片
        #4.返回生成的图片

        #使用随机模块生成: 字符+数字的随机数，长度6
        salt=''.join(random.sample(string.ascii_letters + string.digits, 4))
        #生成一张图片
        img=ImageCaptcha()
        #把生成的数字添加图片上
        image=img.generate(salt)
        # 3. 连接redis
        redis_conn = redis.Redis(host='localhost', port=6379)
        imgId='img_{}'.format(imagecodeid)
        # # 4. 存储图片验证码，设置过期时间10分钟
        redis_conn.setex(imgId,300,salt)
        #返回图片
        return HttpResponse(image,content_type='image/jpg')

#判断图片验证码
class CheckImageCode(APIView):
    def get(self, request):
        """
        1. 接收前端发送的参数，imageCodeID & imageCode
        2. 取出redis中的 图片验证码
            如果取不到，说明过期，响应204
            如果取到验证码，进行对比，注意： 统一大小写
        3. 根据对比结果，返回响应
            对比成功，响应200
            对比失败，响应204
        """
        #1. 接收前端发送的参数，imageCodeID & imageCode
        image_id = request.query_params.get("imageCodeID")
        image_code = request.query_params.get("imageCode")

        # 2. 取出redis中的 图片验证码
        #     如果取不到，说明过期，响应204
        #     如果取到验证码，进行对比，注意： 统一大小写
        redis_cli=redis.Redis(host='localhost', port=6379)
        #查询redis
        resuit=redis_cli.get('img_{}'.format(image_id))
        if resuit:
           if resuit.decode().lower() != image_code.lower():
               return Response({'msg':'验证码输入错误'})
           else:
               return Response({'code':200})
        else:
            return Response({'msg':'验证码已过期'})

#判断用户名
class CheckUsername(APIView):
    def get(self, request, name):
        """
        判断用户名是否重复
        1.获取前端传来的用户名
        2. 校验, 数据中是否有此用户名
        3. 有的话说明已经存在
        """
        # 直接从数据库查询
        # 统计当前用户的数量
        rest = User.objects.filter(username=name).count()
        if rest > 0:
            # 说明用户名已经存在
            return Response({'msg':"用户名已经存在","code":400})
        # 不存在
        return Response({"code":200})

# """判断手机号号是否重复"""
class CheckMobile(APIView):
    def get(self, request, mobile):
        """判断手机号号是否重复"""
        rest = User.objects.filter(mobile=mobile).count()
        if rest > 0:
            # 说明用户名已经存在
            return Response({'msg': "手机号已经存在", "code": 400})
        # 不存在
        return Response({"code": 200})

#注册
class UserRegister(APIView):
    def post(self, request):
        """
        注册业务逻辑(实现思路):
        1.获取request.data.get()中的数据,拿过来和数据中的字段比较: userName, pwd, mobile, agree
        2.如果字段一样,注册成功, 写入数据库
        7. 是否勾选
        """
        user_name = request.data.get('userName')
        pwd = request.data.get('pwd')
        mobile = request.data.get('mobile')
        agree = request.data.get('agree')
        # 后端要校验前端传来的数据
        # 只要有一个为空就错误
        if not all([user_name, pwd, mobile, agree]):
            return Response({'msg':"请输入完善注册用户信息","code":400})

        if not agree:
            # 说明没有同意协议
            return Response({"msg":"请勾选协议"})
        # 写入数据库
        # create()写入数据库时,密码是明文存储, 这是不安全的, 我们要以密文存储密码
        # create_user会把密码进行加密存储
        User.objects.create_user(username=user_name, password=pwd,mobile=mobile, agree_rule=agree)
        return Response({'msg':"注册成功!","code":201})

#登录
class Login(APIView):
    def post(self,request):
        user_name=request.data.get('user')
        pwd=request.data.get('pwd')
        try:
            user=User.objects.get(Q(username=user_name) | Q(mobile=user_name))
        except User.DoesNotExist as e:
            return Response({'msg':'用户不存在','code':400})
        is_correct=check_password(pwd,user.password)
        if is_correct:
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            resp=Response({'msg':'登陆成功','code':200,'user':{'userName':user.username},'token':token})
            resp.set_cookie('token',token)
            return resp
        else:
            return Response({'msg':'用户名或密码不正确！',"code":400})

# """退出登录"""
class Logout(APIView):
    def post(self,request):
        """退出登录"""
        token=request.COOKIES.get('token')
        if token:
            del token
        return Response({'msg':'退出成功!','code':200})

# 用户信息展示
class UserInfo(APIView):
    def post(self,request):
        """用户信息展示"""
        name = request.data.get('user').get('userName')
        # 查询用户信息和用户的收货地址信息
        try:
            user = User.objects.get(username=name)
        except Exception as e:
            return Response({'msg':"请先登录","code":400})
        # 返回用户信息

        addresses = user.address_set.all()
        # add_ser = AddressSer(addresses, many=True)
        user_addr = []
        for addr in addresses:
            user_addr.append(AddressSer(addr).data)

        data = {
            "username":user.username,
            "mobile":user.mobile,
            "addresses":user_addr
        }

        return JsonResponse({"msg":"获取用户信息成功","code":200,"userInfo":data})


#添加收获地址
class AddAddress(APIView):
    def post(self, request):
        """添加收货地址"""
        name = request.data.get('user').get('userName')
        # 查询用户信息和用户的收货地址信息
        try:
            user = User.objects.get(username=name)
        except Exception as e:
            return Response({'msg': "请先登录", "code": 400})
        receiver = request.data.get('receiver')
        receive_mobile = request.data.get('receive_mobile')
        receive_addr = request.data.get('receive_addr')
        is_default = request.data.get('is_default')
        if not all([receive_addr,receiver,receive_mobile,is_default]):
            # 此时数据不全
            return Response({'msg':"请完善地址信息","code":400})
        add = Address.objects.create(user_id=user.id, is_default=is_default,receiver=receiver,
                               receive_addr=receive_addr,receive_mobile=receive_mobile)
        ser = AddressSer(add)
        return Response({"msg":"添加收货地址成功","code":200, "addr":ser.data})


#修改用户信息
class UpdateUserInfo(APIView):
    def post(self,request):
        """修改用户信息"""
        name = request.data.get('user').get('userName')
        # 查询用户信息和用户的收货地址信息
        try:
            user = User.objects.get(username=name)
        except Exception as e:
            return Response({'msg': "请先登录", "code": 400})
        phone = request.data.get('phone')
        # 前端传来的用户地址信息
        addr_list = request.data.get('addr')
        user.mobile = phone
        user.save()
        for new_addr in addr_list:
            print(">>>>", new_addr)
            # 判断是否有更新, 若没有返回对象,要更新, 若返回的有对象,不用更新
            addr = Address.objects.filter(id=new_addr.get('id'),
                                          receiver=new_addr.get("receiver"),
                                          receive_mobile=new_addr.get("receive_mobile"),
                                          receive_addr=new_addr.get("receive_addr"),
                                         )
            print(addr)
            if not addr:
                addrs = Address.objects.get(id=new_addr.get('id'))
                addrs.receiver = new_addr.get("receiver")
                addrs.receive_mobile = new_addr.get("receive_mobile")
                addrs.receive_addr = new_addr.get("receive_addr")
                addrs.save()

        return Response({'msg':"更新信息成功","code":200})


#删除地址
class DelAddressInfo(APIView):
    def post(self,request):
        add_id = request.data.get('addr_id')
        try:
            address = Address.objects.get(id=add_id)
        except Exception as e:
            return Response({'msg':'获取地址信息失败',"code":400})
        address.delete()
        return Response({"msg":"删除成功!","code":200})


#更新密码
class UpdatePassword(APIView):
    def post(self, request):
        """更新密码"""
        name = request.data.get('user')
        old_pwd = request.data.get('originPw')
        new_pwd = request.data.get('newPw')
        confirm_pwd = request.data.get('confirmNewPw')
        if new_pwd != confirm_pwd:
            return Response({"msg":'输入的两次密码不一致,请重新输入',"code":400})
        if old_pwd == new_pwd:
            return Response({"msg": '新密码和旧密码一样,请重新输入', "code": 400})

        # 更新新密码
        try:
            user = User.objects.get(username=name)
        except Exception  as e:
            return Response({"msg":"获取用户失败", "code":400})
        # 对密码进行hasH加密
        user.password = make_password(new_pwd)
        user.save()
        return Response({'msg':"修改密码成功","code":200})