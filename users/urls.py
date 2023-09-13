"""zhang URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
urlpatterns = [
    # 校验用户名是否重复
    path('check/username/<str:name>/', views.CheckUsername.as_view()),
    # 校验手机号是否重复
    path('check/mobile/<str:mobile>/', views.CheckMobile.as_view()),
    # 注册
    path('register/', views.UserRegister.as_view()),
    #生成图片
    path('image_code/<str:imagecodeid>/',views.GenerateImageCode.as_view()),
    #校验
    path('check_image_code/', views.CheckImageCode.as_view()),
    #登录
    path('login/',views.Login.as_view()),
    #退出登录
    path('logout/',views.Logout.as_view()),
    # 获取用户信息
    path('userInfo/', views.UserInfo.as_view()),
    # 添加收货地址
    path('add_addrerss/', views.AddAddress.as_view()),
    # 修改用户信息
    path('updateUserInfo/', views.UpdateUserInfo.as_view()),
    #删除地址
    path('deladdress/',views.DelAddressInfo.as_view()),
    # 修改密码
    path('updatePassword/',views.UpdatePassword.as_view())
]