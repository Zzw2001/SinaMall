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
    # 创建订单
    path('addorder/', views.CreateApp.as_view()),
    # 支付成功回调
    path('pay/result/', views.CheckPayResult.as_view()),
    # 获取订单信息
    path('orderInfo/', views.OrderInfo.as_view()),
    # 去支付
    path('payorder/', views.PayOrder.as_view()),
    # 修改订单状态
    path('changepaystatus/', views.ChangePayStatusView.as_view()),
    # 删除订单中的商品
    path('deleteOrderProduct/', views.DeleteOrderGoods.as_view())
]
