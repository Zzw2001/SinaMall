from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from users.models import User
from django.db.models import Q


class AuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """重写此方法"""
        # 1.用户输入的可能是用户名或手机号
        # 使用Q对象进行逻辑操作相当于或操作
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
        except Exception as e:
            print(e)
            return None

        # 密码校验
        is_correct = check_password(password, user.password)
        if is_correct:
            return user
        else:
            print("密码校验错误啦!!")
            return None