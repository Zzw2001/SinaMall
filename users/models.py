from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    # 需要的字段: username, pwd, mobile,
    mobile = models.CharField(max_length=11, verbose_name="手机号")
    agree_rule = models.BooleanField(default=True,verbose_name="同意协议")

    class Meta:
        # 指定数据库表名
        db_table = 'stu'

    def __str__(self):
        return self.username



class Address(models.Model):
    """收货地址"""
    receiver = models.CharField("收件人", max_length=30)
    receive_mobile = models.CharField("手机号", max_length=11)
    receive_addr = models.CharField("收货地址", max_length=100)
    is_default = models.BooleanField("是否默认", default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")

    def __str__(self):
        return self.receiver + " " + self.receive_mobile + " " + self.receive_addr