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
from .views import Addcart,CartInfo,Update,UpdateCarStatus,UpdateAllStatus,DeleateCart
urlpatterns = [
    #添加购物车
    path('addCarts/',Addcart.as_view()),
    #查看购物车
    path('cartsInfo/',CartInfo.as_view()),
    #更新购物车数量
    path('user/updateShoppingCart/',Update.as_view()),
    # 更新购车中勾选状态
    path("updateStatus/", UpdateCarStatus.as_view()),
    # 全选状态修改
    path('updateAllStatus/', UpdateAllStatus.as_view()),
    # 删除购物车种商品
    path('delcartgood/', DeleateCart.as_view())
]
