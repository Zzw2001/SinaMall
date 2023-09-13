<!--
 * @Description: 我的购物车页面组件
 * @Author: hai-27
 * @Date: 2020-02-20 01:55:47
 * @LastEditors: hai-27
 * @LastEditTime: 2020-02-27 13:36:42
 -->

<template>
  <div class="shoppingCart">

    <!-- 购物车头部 -->
    <div class="cart-header">
      <div class="cart-header-content">
        <p>
          <i class="el-icon-shopping-cart-full" style="color:#ff6700; font-weight: 600;"></i>
          我的购物车
        </p>
        <span>温馨提示：产品是否购买成功，以最终下单为准哦，请尽快结算</span>
      </div>
    </div>
    <!-- 购物车头部END -->


    <!-- xxxxxxxxxxx购物车主要内容区xxxxxxxxxxxx -->
    <div class="content" v-if="getShoppingCart.length>0">
      <ul>
        <!-- 购物车表头 -->
        <li class="header">
          <div class="pro-check">
            <!-- 全选 -->
            <el-checkbox v-model="isAllCheck">全选</el-checkbox>
          </div>
          <div class="pro-img"></div>
          <div class="pro-name">商品名称</div>
          <div class="pro-price">单价</div>
          <div class="pro-num">数量</div>
          <div class="pro-total">小计</div>
          <div class="pro-action">操作</div>
        </li>
        <!-- 购物车表头END -->

        <!-- 购物车列表 -->
        <li class="product-list" v-for="(item,index) in getShoppingCart" :key="item.productID">
          <div class="pro-check">
            <!-- 单选 -->
            <el-checkbox :value="item.check" @change="checkChange($event,index,item.id)"></el-checkbox>
          </div>
          <div class="pro-img">
            <router-link :to="{ path: '/goods/details', query: {productID:item.productID} }">
              <img :src="item.productImg" />
            </router-link>
          </div>
          <div class="pro-name">
            <router-link
              :to="{ path: '/goods/details', query: {productID:item.productID} }"
            >{{item.productName}}</router-link>
          </div>
          <div class="pro-price">{{item.price}}元</div>
          <div class="pro-num">
            <!-- 更新购物车 1.默认勾选 2. +/-数量     -->
            <!-- 更新购买的商品数量 -->
            <el-input-number
              size="small"
              :value="item.num"
              @change="handleChange($event,index,item.productID)"
              :min="1"
              :max="item.maxNum"
            ></el-input-number>
          </div>
          <!-- 当前商品总计价格 -->
          <div class="pro-total pro-total-in">{{item.price*item.num}}元</div>
          
          <!-- 是否删除该商品 -->
          <div class="pro-action">
            <el-popover placement="right">
              <p>确定删除吗？</p>
              <div style="text-align: right; margin: 10px 0 0">
                <el-button
                  type="primary"
                  size="mini"
                  @click="deleteItem($event, item.productID)"
                >确定</el-button>
              </div>
              <i class="el-icon-error" slot="reference" style="font-size: 18px;"></i>
            </el-popover>
          </div>
        </li>
        <!-- 购物车列表END -->

      </ul>
      <div style="height:20px;background-color: #f5f5f5"></div>
      
      
      <!-- 购物车底部导航条 -->
      <div class="cart-bar">
        <div class="cart-bar-left">
          <span>
            <router-link to="/goods">继续购物</router-link>
          </span>
          <span class="sep">|</span>
          <span class="cart-total">
            共
            <span class="cart-total-num">{{getNum}}</span> 件商品，已选择
            <span class="cart-total-num">{{getCheckNum}}</span> 件
          </span>
        </div>
        <div class="cart-bar-right">
          <span>
            <span class="total-price-title">合计：</span>
            <span class="total-price">{{getTotalPrice}}元</span>
          </span>

          <!-- 去结算 -->
          <router-link :to="getCheckNum > 0 ? '/confirmOrder' : ''">
            <div :class="getCheckNum > 0 ? 'btn-primary' : 'btn-primary-disabled'">去结算</div>
          </router-link>
        </div>
      </div>
      <!-- 购物车底部导航条END -->
    </div>
    <!-- 购物车主要内容区END -->

    <!-- 购物车为空的时候显示的内容 -->
    <div v-else class="cart-empty">
      <div class="empty">
        <h2>您的购物车还是空的！</h2>
        <p>快去购物吧！</p>
      </div>
    </div>
    <!-- 购物车为空的时候显示的内容END -->
  </div>
</template>


<script>
import { mapActions } from "vuex";
import { mapGetters } from "vuex";

export default {
  data() {
    return {};
  },
  
  methods: {
    ...mapActions(["updateShoppingCart", "deleteShoppingCart", "checkAll"]),
    
    // 修改商品数量时，触发
    handleChange(currentValue, key, productID) {
      console.log("@@修改商品数量了......")
      // currentValue，当前商品的新数量
      // key，商品{} 在shoppingChart数组中 的索引
      // productID 当前商品的id

      // 1.修改数量时，设置为 勾选状态
      this.updateShoppingCart({ key: key, prop: "check", val: true });
      
      // 2.请求后端 --更新redis购物车--指定商品的数量
      this.$axios
        .post("/carts/user/updateShoppingCart/", {
          user: this.$store.getters.getUser,//{userName:'laufing'}
          productID: productID,
          num: currentValue,//改后的值
        })
        .then(res => {
          console.log("@@更新购物车的后端响应：", res)
          switch (res.data.code) {
            case 200:
              // 200代表更新成功
              // 更新vuex状态
              this.updateShoppingCart({
                key: key,
                prop: "num",
                val: currentValue
              });
              // 提示更新成功信息
              this.notifySucceed(res.data.msg);
              break;
            default:
              // 提示更新失败信息
              this.notifyError(res.data.msg);
          }
        })
        .catch(err => {
          return Promise.reject(err);
        });
    },
    // 单选
    checkChange(val, key, cartID) {
      console.log("单选的勾选状态:", val, key, cartID)
      // 更新后端购物车中该商品的勾选状态
      const productID = this.getShoppingCart[key].productID
      this.$axios.get("/carts/updateStatus/", {
        params:{
          productID,
          cartID,
          val,
          }
        })
      .then(res=>{
        if(res.data.code == 200){
          // 更新前端vuex中购物车商品勾选状态
          this.updateShoppingCart({ key: key, prop: "check", val: val});
          this.notifySucceed(res.data.msg)
        }else{
          this.notifyError(res.data.msg)
        }
      })
      .catch(err=>{
        return Promise.reject(err)
      })
      
    },


    // 向后端请求删除购物车的 商品信息
    deleteItem(e, productID) {
      // console.log(e,id,productID)
      this.$axios
        .post("/carts/delcartgood/", {
          user: this.$store.getters.getUser,
          productID: productID
        })
        .then(res => {
          console.log("@@删除购物车商品res", res)
          switch (res.data.code) {
            case 200:
              // 200 删除成功
              // 更新vuex状态
              this.deleteShoppingCart(productID);
              // 提示删除成功信息
              this.notifySucceed(res.data.msg);
              break;
            default:
              // 提示删除失败信息
              this.notifyError(res.data.msg);
          }
        })
        .catch(err => {
          return Promise.reject(err);
        });
    }
  },


  computed: {
    ...mapGetters([
      "getShoppingCart", //获取vuex中的购物车数组
      "getCheckNum", //获取购物车中勾选的商品数量
      "getTotalPrice",
      "getNum", //计算属性，获取购物车中的商品总数
    ]),

    isAllCheck: {
      // 读的时候执行getter
      get() {
        return this.$store.getters.getIsAllCheck;
      },
      // 写的时候，执行setter
      set(val) {
        // 向后端发送请求，设置全选状态
        const cartID = this.getShoppingCart[0].id
        this.$axios.post("/carts/updateAllStatus/", {
          cartID,
          val,
        })
        .then(res=>{
          console.log("全选的响应：", res)
          if(res.data.code == 200){
            // 更新前端购物车
            this.checkAll(val);
          }else{
            this.notifyError(res.data.msg)
          }
        })
        .catch(err=>{
          return Promise.reject(err)
        })
        
      }
    }
  }
};
</script>


<style scoped>
.shoppingCart {
  background-color: #f5f5f5;
  padding-bottom: 20px;
}
/* 购物车头部CSS */
.shoppingCart .cart-header {
  height: 64px;
  border-bottom: 2px solid #ff6700;
  background-color: #fff;
  margin-bottom: 20px;
}
.shoppingCart .cart-header .cart-header-content {
  width: 1225px;
  margin: 0 auto;
}
.shoppingCart .cart-header p {
  font-size: 28px;
  line-height: 58px;
  float: left;
  font-weight: normal;
  color: #424242;
}
.shoppingCart .cart-header span {
  color: #757575;
  font-size: 12px;
  float: left;
  height: 20px;
  line-height: 20px;
  margin-top: 30px;
  margin-left: 15px;
}
/* 购物车头部CSS END */

/* 购物车主要内容区CSS */
.shoppingCart .content {
  width: 1225px;
  margin: 0 auto;
  background-color: #fff;
}

.shoppingCart .content ul {
  background-color: #fff;
  color: #424242;
  line-height: 85px;
}
/* 购物车表头及CSS */
.shoppingCart .content ul .header {
  height: 85px;
  padding-right: 26px;
  color: #424242;
}
.shoppingCart .content ul .product-list {
  height: 85px;
  padding: 15px 26px 15px 0;
  border-top: 1px solid #e0e0e0;
}
.shoppingCart .content ul .pro-check {
  float: left;
  height: 85px;
  width: 110px;
}
.shoppingCart .content ul .pro-check .el-checkbox {
  font-size: 16px;
  margin-left: 24px;
}
.shoppingCart .content ul .pro-img {
  float: left;
  height: 85px;
  width: 120px;
}
.shoppingCart .content ul .pro-img img {
  height: 80px;
  width: 80px;
}
.shoppingCart .content ul .pro-name {
  float: left;
  width: 380px;
}
.shoppingCart .content ul .pro-name a {
  color: #424242;
}
.shoppingCart .content ul .pro-name a:hover {
  color: #ff6700;
}
.shoppingCart .content ul .pro-price {
  float: left;
  width: 140px;
  padding-right: 18px;
  text-align: center;
}
.shoppingCart .content ul .pro-num {
  float: left;
  width: 150px;
  text-align: center;
}
.shoppingCart .content ul .pro-total {
  float: left;
  width: 120px;
  padding-right: 81px;
  text-align: right;
}
.shoppingCart .content ul .pro-total-in {
  color: #ff6700;
}
.shoppingCart .content ul .pro-action {
  float: left;
  width: 80px;
  text-align: center;
}
.shoppingCart .content ul .pro-action i:hover {
  color: #ff6700;
}
/* 购物车表头及CSS END */

/* 购物车底部导航条CSS */
.shoppingCart .cart-bar {
  width: 1225px;
  height: 50px;
  line-height: 50px;
  background-color: #fff;
}
.shoppingCart .cart-bar .cart-bar-left {
  float: left;
}
.shoppingCart .cart-bar .cart-bar-left a {
  line-height: 50px;
  margin-left: 32px;
  color: #757575;
}
.shoppingCart .cart-bar .cart-bar-left a:hover {
  color: #ff6700;
}
.shoppingCart .cart-bar .cart-bar-left .sep {
  color: #eee;
  margin: 0 20px;
}
.shoppingCart .cart-bar .cart-bar-left .cart-total {
  color: #757575;
}
.shoppingCart .cart-bar .cart-bar-left .cart-total-num {
  color: #ff6700;
}
.shoppingCart .cart-bar .cart-bar-right {
  float: right;
}
.shoppingCart .cart-bar .cart-bar-right .total-price-title {
  color: #ff6700;
  font-size: 14px;
}
.shoppingCart .cart-bar .cart-bar-right .total-price {
  color: #ff6700;
  font-size: 30px;
}
.shoppingCart .cart-bar .cart-bar-right .btn-primary {
  float: right;
  width: 200px;
  text-align: center;
  font-size: 18px;
  margin-left: 50px;
  background: #ff6700;
  color: #fff;
}
.shoppingCart .cart-bar .cart-bar-right .btn-primary-disabled {
  float: right;
  width: 200px;
  text-align: center;
  font-size: 18px;
  margin-left: 50px;
  background: #e0e0e0;
  color: #b0b0b0;
}
.shoppingCart .cart-bar .cart-bar-right .btn-primary:hover {
  background-color: #f25807;
}
/* 购物车底部导航条CSS END */
/* 购物车主要内容区CSS END */

/* 购物车为空的时候显示的内容CSS */
.shoppingCart .cart-empty {
  width: 1225px;
  margin: 0 auto;
}
.shoppingCart .cart-empty .empty {
  height: 300px;
  padding: 0 0 130px 558px;
  margin: 65px 0 0;
  background: url(../assets/imgs/cart-empty.png) no-repeat 124px 0;
  color: #b0b0b0;
  overflow: hidden;
}
.shoppingCart .cart-empty .empty h2 {
  margin: 70px 0 15px;
  font-size: 36px;
}
.shoppingCart .cart-empty .empty p {
  margin: 0 0 20px;
  font-size: 20px;
}
/* 购物车为空的时候显示的内容CSS END */
</style>