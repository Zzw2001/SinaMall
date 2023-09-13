<!--
 * @Description: 商品详情页面组件
 * @Author: hai-27
 * @Date: 2020-02-16 20:20:26
 * @LastEditors: hai-27
 * @LastEditTime: 2020-03-07 21:59:26
 -->
<template>
  <div id="details">

    <!-- 详情的头部 -->
    <div class="page-header">
      <div class="title">
        <!-- 插值语法 -->
        <!-- 产品的sku_name -->
        <p>{{productDetails.sku_name}}</p>
        <div class="list">
          <ul>
            <li>
              <router-link to>概述</router-link>
            </li>
            <li>
              <router-link to>参数</router-link>
            </li>
            <li>
              <router-link to>用户评价</router-link>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <!-- 头部END -->


    <!-- 主要内容 -->
    <div class="main">
      <!-- 左侧商品轮播图 -->
      <div class="block">
        <!-- 多个图片 轮播图显示 -->
        <el-carousel height="560px" v-if="productPicture.length>1">
          <el-carousel-item v-for="item in productPicture" :key="item.id">
            <img style="height:560px;" :src="item.img" :alt="item.title" />
          </el-carousel-item>
        </el-carousel>
        <!--  一个图片 单独显示-->
        <div v-if="productPicture.length==1">
          <img
            style="height:560px;"
            :src="productPicture[0].img"
            :alt="productPicture[0].title"
          />
        </div>
      </div>
      <!-- 左侧商品轮播图END -->

      <!-- 右侧内容区 -->
      <div class="content">
        <h1 class="name">{{productDetails.sku_name}}</h1>
        <p class="intro">{{productDetails.instruction}}</p>
        <p class="store">小米自营</p>
        <div class="price">
          <span>{{productDetails.selling_price}}元</span>
          <span
            v-show="productDetails.price != productDetails.selling_price"
            class="del"
          >{{productDetails.price}}元</span>
        </div>
        <div class="pro-list">
          <span class="pro-name">{{productDetails.sku_name}}</span>
          <span class="pro-price">
            <span>{{productDetails.selling_price}}元</span>
            <span
              v-show="productDetails.price != productDetails.selling_price"
              class="pro-del"
            >{{productDetails.price}}元</span>
          </span>
          <p class="price-sum">总计 : {{productDetails.selling_price}}元</p>
        </div>


        <!-- 加入购物车 & 收藏   底部按钮 -->
        <div class="button">
          <el-button class="shop-cart" :disabled="dis" @click="addShoppingCart">加入购物车</el-button>
          <el-button class="like" @click="addCollect">喜欢</el-button>
        </div>
        <!-- 内容区底部按钮END -->
        <div class="pro-policy">
          <ul>
            <li>
              <i class="el-icon-circle-check"></i> 小米自营
            </li>
            <li>
              <i class="el-icon-circle-check"></i> 小米发货
            </li>
            <li>
              <i class="el-icon-circle-check"></i> 7天无理由退货
            </li>
            <li>
              <i class="el-icon-circle-check"></i> 7天价格保护
            </li>
          </ul>
        </div>
      </div>
      <!-- 右侧内容区END -->
    </div>
    <!-- 主要内容END -->
  </div>
</template>

<script>
import { mapActions } from "vuex";
export default {
  data() {
    return {
      dis: false, // 控制“加入购物车 按钮 是否可用”
      productID: "", // router-link 传入的商品id
      productDetails: "", // 商品详细信息
      productPicture: "" // 商品图片
    };
  },
  // 通过路由获取商品id
  activated() {//点击router-link 激活
    // $route 组件自己对应的路由信息{path:xxx, query:{productId:xxx}}
    if (this.$route.query.productID != undefined) {
      this.productID = this.$route.query.productID;
      // productID值由""==>路由传入的productID，触发监视属性
    }
  },
  watch: {
    // 监听商品id的变化，请求后端获取商品数据
    productID: function(val) {//val 为变化的新值
      // 
      this.getDetails(val);
      this.getDetailsPicture(val);
      this.addHistory(val)
    }
  },
  methods: {
    ...mapActions(["unshiftShoppingCart", "addShoppingCartNum"]),

    // 加入历史记录
    addHistory(productID){
      // 页面挂载完成，请求后端加入历史记录
      console.log('token的值是------->',localStorage.getItem('token'))
      this.$axios.post('/goods/onegood/history/', {
        productID: productID,
        token: localStorage.getItem('token')||''
      })
      .then(res => {
        console.log("加入历史记录的响应：", res)
      })
      .catch(err => {
        return Promise.reject(err)
      })
    },
    // 获取商品详细信息
    getDetails(val) {//val为商品id
      this.$axios
        .get("/goods/onegood/", {params:{
          gid: val
        }})
        .then(res => {
          console.log("@@一个商品>>>>>:", res.data)
          this.productDetails = res.data;
          // 然后模板就可以解析数据了
        })
        .catch(err => {
          return Promise.reject(err);
        });
    },
    // 获取商品图片
    getDetailsPicture(val) {//通过商品id获取其图片
      this.$axios
        .get("/goods/onegood/imgs/", {params:{
          gid: val
        }})
        .then(res => {
          console.log("@当前商品的图片>>>>>:",res.data)
          this.productPicture = res.data;
        })
        .catch(err => {
          return Promise.reject(err);
        });
    },

    // 加入购物车，点击一次增加一次，非幂等方式，中间可能某次数据包丢失
    // 导致 前后端  商品数量不一致
    addShoppingCart() { //
      // 判断是否登录,没有登录则显示登录组件
      if (!this.$store.getters.getUser) {
        this.$store.dispatch("setShowLogin", true);
        return;
      }

      // 已经登录，则请求后端将当前商品，加入自己的购物车
      console.log("@@getUser,已登录用户:",this.$store.getters.getUser)
      // {userName:'laufing',xxx...}
      this.$axios
        .post("/carts/addCarts/", {
          user: this.$store.getters.getUser.userName,
          productID: this.productID
        })
        .then(res => {
          console.log("@@添加购物车res:", res)
          // 
          // 处理购物车的响应
          switch (res.data.code) {
            case 200:
              // 新加入购物车成功
              this.unshiftShoppingCart(res.data.shoppingCartData);
              this.notifySucceed(res.data.msg);
              break;
            case 201:
              // 该商品已经在购物车，数量+1
              this.addShoppingCartNum(this.productID);
              this.notifySucceed(res.data.msg);
              break;
            case 202:
              // 商品数量达到限购数量(即库存量)
              this.dis = true; //购物车按钮不可点击
              this.notifyError(res.data.msg);
              break;
            case 203:
            default:
              this.notifyError(res.data.msg);
          }
        })
        .catch(err => {
          return Promise.reject(err);
        });
    },


    // 添加收藏
    addCollect() {
      // 判断是否登录,没有登录则显示登录组件
      if (!this.$store.getters.getUser) {
        this.$store.dispatch("setShowLogin", true);
        return;
      }
      this.$axios
        .post("/goods/collects/", {
          user: this.$store.getters.getUser,
          product_id: this.productID
        })
        .then(res => {
          console.log("@@添加收藏的响应--->：", res)
          if (res.data.code == 200) {
            // 添加收藏成功
            this.notifySucceed(res.data.msg);
          } else {
            // 添加收藏失败
            this.notifyError(res.data.msg);
          }
        })
        .catch(err => {
          return Promise.reject(err);
        });
    }
  }
};

</script>


<style>
/* 头部CSS */
#details .page-header {
  height: 64px;
  margin-top: -20px;
  z-index: 4;
  background: #fff;
  border-bottom: 1px solid #e0e0e0;
  -webkit-box-shadow: 0px 5px 5px rgba(0, 0, 0, 0.07);
  box-shadow: 0px 5px 5px rgba(0, 0, 0, 0.07);
}
#details .page-header .title {
  width: 1225px;
  height: 64px;
  line-height: 64px;
  font-size: 18px;
  font-weight: 400;
  color: #212121;
  margin: 0 auto;
}
#details .page-header .title p {
  float: left;
}
#details .page-header .title .list {
  height: 64px;
  float: right;
}
#details .page-header .title .list li {
  float: left;
  margin-left: 20px;
}
#details .page-header .title .list li a {
  font-size: 14px;
  color: #616161;
}
#details .page-header .title .list li a:hover {
  font-size: 14px;
  color: #ff6700;
}
/* 头部CSS END */

/* 主要内容CSS */
#details .main {
  width: 1225px;
  height: 560px;
  padding-top: 30px;
  margin: 0 auto;
}
#details .main .block {
  float: left;
  width: 560px;
  height: 560px;
}
#details .el-carousel .el-carousel__indicator .el-carousel__button {
  background-color: rgba(163, 163, 163, 0.8);
}
#details .main .content {
  float: left;
  margin-left: 25px;
  width: 640px;
}
#details .main .content .name {
  height: 30px;
  line-height: 30px;
  font-size: 24px;
  font-weight: normal;
  color: #212121;
}
#details .main .content .intro {
  color: #b0b0b0;
  padding-top: 10px;
}
#details .main .content .store {
  color: #ff6700;
  padding-top: 10px;
}
#details .main .content .price {
  display: block;
  font-size: 18px;
  color: #ff6700;
  border-bottom: 1px solid #e0e0e0;
  padding: 25px 0 25px;
}
#details .main .content .price .del {
  font-size: 14px;
  margin-left: 10px;
  color: #b0b0b0;
  text-decoration: line-through;
}
#details .main .content .pro-list {
  background: #f9f9fa;
  padding: 30px 60px;
  margin: 50px 0 50px;
}
#details .main .content .pro-list span {
  line-height: 30px;
  color: #616161;
}
#details .main .content .pro-list .pro-price {
  float: right;
}
#details .main .content .pro-list .pro-price .pro-del {
  margin-left: 10px;
  text-decoration: line-through;
}
#details .main .content .pro-list .price-sum {
  color: #ff6700;
  font-size: 24px;
  padding-top: 20px;
}
#details .main .content .button {
  height: 55px;
  margin: 10px 0 20px 0;
}
#details .main .content .button .el-button {
  float: left;
  height: 55px;
  font-size: 16px;
  color: #fff;
  border: none;
  text-align: center;
}
#details .main .content .button .shop-cart {
  width: 340px;
  background-color: #ff6700;
}
#details .main .content .button .shop-cart:hover {
  background-color: #f25807;
}

#details .main .content .button .like {
  width: 260px;
  margin-left: 40px;
  background-color: #b0b0b0;
}
#details .main .content .button .like:hover {
  background-color: #757575;
}
#details .main .content .pro-policy li {
  float: left;
  margin-right: 20px;
  color: #b0b0b0;
}
/* 主要内容CSS END */
</style>