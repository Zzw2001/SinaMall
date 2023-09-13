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
from .views import *

urlpatterns = [
    # 所有的轮播图数据
    path('carouseles/', CarouselView.as_view()),
    # 根据类别名获取商品数据
    path('oneCategory/goods/', GoodsByCateName.as_view()),
    # 热门商品
    path('getHotProduct/', HotProductViews.as_view()),
    # 获取所有的类别
    path('cates/',CategoryView.as_view()),
    # 根据类别获取商品
    path('good/getProductByCategory/', GoodsByCategoryId.as_view()),
    # 获取所有的商品
    path('good/getAllProduct/',GoodsViews.as_view()),
    # 通过商品id 获取商品的图片信息"
    path('onegood/imgs/', GoodiList.as_view()),
    # 通过商品id 获取商品的详细信息"
    path('onegood/', GoodsAll.as_view()),
    #添加历史浏览记录
    path('onegood/history/',AddHostory.as_view()),
    # 添加收藏
    path('collects/', CollectViews.as_view()),
    # 查看收藏
    path('collects/all/', CollectInfoView.as_view()),
    # 删除收藏
    path('collects/del/', CollectDelView.as_view())
]

