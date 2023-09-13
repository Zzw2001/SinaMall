<!--
 * @Description: 我的订单页面组件
 * @Author: hai-27
 * @Date: 2020-02-20 17:21:54
 * @LastEditors: hai-27
 * @LastEditTime: 2020-02-27 13:36:27
 -->
<template>
  <div class="order">
    <!-- 我的订单头部 -->
    <div class="order-header">
      <div class="order-header-content">
        <p>
          <i class="el-icon-s-order" style="font-size: 30px;color: #ff6700;"></i>
          我的订单
        </p>
      </div>
    </div>
    <!-- 我的订单头部END -->

    <!-- 我的订单主要内容 -->
    <div class="order-content" v-if="orders.length>0">
      <div class="content" v-for="(item,index) in orders" :key="index">
        <!-- item===>[{},{},{}] -->
        <ul>
          <!-- 我的订单表头 -->
          <li class="order-info">
            <div class="order-id">订单编号: {{item[0].orderID}}</div>
            <div class="order-time">订单时间: {{item[0].createdTime | dateFormat}}</div>
          </li>
          <li class="header">
            <div class="pro-img"></div>
            <div class="pro-name">商品名称</div>
            <div class="pro-price">单价</div>
            <div class="pro-num">数量</div>
            <div class="pro-total">小计</div>
            <div class="pro-status">支付状态</div>
            <div class="pro-delete">删除订单</div>
          </li>
          <!-- 我的订单表头END -->

          <!-- 订单列表 -->
          <li class="product-list" v-for="product in item" :key="product.productID">
            <div class="pro-img">
              <router-link :to="{ path: '/goods/details', query: {productID:product.productID} }">
                <img :src="product.productImg" />
              </router-link>
            </div>
            <div class="pro-name">
              <router-link
                :to="{ path: '/goods/details', query: {productID:product.productID} }"
              >{{product.productName}}</router-link>
            </div>
            <div class="pro-price">{{product.productPrice}}元</div>
            <div class="pro-num">{{product.productNum}}</div>
            <div class="pro-total pro-total-in">{{product.productPrice*product.productNum}}元</div>
            <!-- 支付状态 -->
            <div class="pro-status">
              <div v-if="product.payStatus=='0'">
                <a href="javascript:;" @click="goToPay(product.orderID,total[index].totalPrice)">{{product.payStatus}}</a>
              </div>
              <div v-else-if="product.payStatus=='1'||product.payStatus=='4'">
                <span>{{product.payStatus}}</span>
              </div>
              <div v-else-if="product.payStatus=='2'">
                <a href="javascript:;" @click="confirmReceive(product.orderID)">{{ product.payStatus }}</a>
              </div>
              <div v-else-if="product.payStatus=='3'">
                <a href="javascript:;" @click="alertInfo(product.payStatus)">{{product.payStatus}}</a>
              </div>
            </div>
            <!-- 删除订单商品 -->
            <div class="pro-delete">
              <i class="el-icon-delete-solid" :style="{fontSize:'25px',}" @click="deleteProduct(product.orderID,product.productID)"></i>
            </div>
          </li>
        </ul>
        <div class="order-bar">
          <div class="order-bar-left">
            <span class="order-total">
              共
              <span class="order-total-num">{{total[index].totalNum}}</span> 件商品
            </span>
          </div>
          <div class="order-bar-right">
            <span>
              <span class="total-price-title">合计：</span>
              <span class="total-price">{{total[index].totalPrice}}元</span>
            </span>
          </div>
          <!-- 订单列表END -->
        </div>
      </div>
      <div style="margin-top:-40px;"></div>
    </div>
    <!-- 我的订单主要内容END -->

    <!-- 订单为空的时候显示的内容 -->
    <div v-else class="order-empty">
      <div class="empty">
        <h2>您的订单还是空的！</h2>
        <p>快去购物吧！</p>
      </div>
    </div>
    <!-- 订单为空的时候显示的内容END -->
  </div>
</template>
<script>
export default {
  data() {
    return {
      orders: [], // 订单列表
      total: [] // 每个订单的商品数量及总价列表
    };
  },
  activated() {
    // 获取所有订单数据
    this.$axios
      .post("/orders/orderInfo/", {
        user: this.$store.getters.getUser
      })
      .then(res => {
        console.log("@@查看订单的响应：", res.data.orders)
        if (res.data.code === 200) {
          this.orders = res.data.orders;
        } else {
          this.notifyError(res.data.msg);
        }
      })
      .catch(err => {
        return Promise.reject(err);
      });
  },
  methods:{
    alertInfo(val){
      this.notifySucceed(val)
    },
    // 去支付
    goToPay(orderID, totalPrice){
      this.$axios.post("/orders/payorder/", {
        orderID,
        totalPrice,
      }).then(res=>{
        console.log("@@支付的响应:", res)
        if(res.data.code==302){
          this.notifySucceed("正跳转支付页面...")
          // 2s后跳转，使用如下方式
          setTimeout(window.location.href=res.data.pay_url, 2000)
        }else{
          this.notifyError(res.data.msg)
        }
      }).catch(err=>{
        return Promise.reject(err)
      })
    },
    // 删除订单商品
    deleteProduct(orderID, productID){
      this.$axios.post("/orders/deleteOrderProduct/",{
        orderID,
        productID,
      }).then(res=>{
        console.log("@@删除订单的响应:", res)
        if(res.data.code==200){
          // 前端删除订单商品
          for(let i=0; i<this.orders.length; i++){
            // 获取一个订单数组
            const orderArr = this.orders[i]
            if(orderArr.length==1){
              let productObj = orderArr[0]
              if(productObj.productID==productID&&productObj.orderID==orderID){
                // console.log("xxxxxx删除一个订单")
                this.orders.splice(i, 1) //直接删除当前订单数组
              }
            }else{
              for(let j=0; j<orderArr.length; j++){
                const productObj = orderArr[j]
                if(productObj.productID == productID&&productObj.orderID==orderID){
                  // 因为一个商品id会出现在多个订单中，不能仅凭商品id判断
                  orderArr.splice(j, 1)//从当前位置删除一个商品对象
                } 
              }
            }
            
          }
        }else{
          this.notifyError(res.data.msg)
        }
      }).catch(err=>{
        return Promise.reject(err)
      })
    },
    // 模拟确认收货
    confirmReceive(orderID){
      // 确认是否收货
      let r = confirm("确认收货？请谨慎操作")
      if(r){
        // 用户已确认收货
        this.$axios.post('/orders/changepaystatus/', {
          orderID,
        }).then(res=>{
          console.log("@@确认收货的响应:", res)
          // 前端处理支付状态
          if(res.data.code==200){
            for(let i=0; i<this.orders.length; i++){
              const temp = this.orders[i]
              if(temp[0].orderID == orderID){
                // 找到确认收货的订单
                for(let j=0; j<temp.length; j++){
                  temp[j].payStatus = '待评价'
                }
              }
            }
          }
        }).catch(err=>{
          return Promise.reject(err)
        })

      }else{
        // 用户取消确认
        return
      }
    },

  },
  watch: {
    // 通过订单信息，计算出每个订单的商品数量及总价
    orders: function(val) {
      let total = [];
      for (let i = 0; i < val.length; i++) {
        const element = val[i];

        let totalNum = 0;
        let totalPrice = 0;
        for (let j = 0; j < element.length; j++) {
          const temp = element[j];
          totalNum += temp.productNum;
          totalPrice += temp.productPrice * temp.productNum;
        }
        total.push({ totalNum, totalPrice });
      }
      this.total = total;
    }
  }
};
</script>
<style scoped>
.order {
  background-color: #f5f5f5;
  padding-bottom: 20px;
}
/* 我的订单头部CSS */
.order .order-header {
  height: 64px;
  border-bottom: 2px solid #ff6700;
  background-color: #fff;
  margin-bottom: 20px;
}
.order .order-header .order-header-content {
  width: 1225px;
  margin: 0 auto;
}
.order .order-header p {
  font-size: 28px;
  line-height: 58px;
  float: left;
  font-weight: normal;
  color: #424242;
}
/* 我的订单头部CSS END */
.order .content {
  width: 1225px;
  margin: 0 auto;
  background-color: #fff;
  margin-bottom: 50px;
}

.order .content ul {
  background-color: #fff;
  color: #424242;
  line-height: 85px;
}
/* 我的订单表头CSS */
.order .content ul .order-info {
  height: 60px;
  line-height: 60px;
  padding: 0 26px;
  color: #424242;
  border-bottom: 1px solid #ff6700;
}
.order .content ul .order-info .order-id {
  float: left;
  color: #ff6700;
}
.order .content ul .order-info .order-time {
  float: right;
}

.order .content ul .header {
  height: 85px;
  padding-right: 26px;
  color: #424242;
  /* background-color: lightblue; */
}
/* 我的订单表头CSS END */

/* 订单列表CSS */
.order .content ul .product-list {
  height: 85px;
  padding: 15px 26px 15px 0;
  border-top: 1px solid #e0e0e0;
  /* background-color: pink; */
}
.order .content ul .pro-img {
  float: left;
  height: 85px;
  width: 85px;
  padding-left: 80px;/*原来80px*/
  /* background-color: red; */
}
.order .content ul .pro-img img {
  height: 80px;
  width: 80px;
}
.order .content ul .pro-name {
  float: left;
  width: 280px; /*原380px*/
  /* background-color: purple; */
  text-align: center;
}
.order .content ul .pro-name a {
  color: #424242;
}
.order .content ul .pro-name a:hover {
  color: #ff6700;
}
.order .content ul .pro-price {
  float: left;
  width: 150px;
  padding-right: 18px;
  text-align: center;
  /* background-color: green; */
}
.order .content ul .pro-num {
  float: left;
  width: 150px;
  text-align: center;
}
.order .content ul .pro-total {
  float: left;
  width: 150px;
  padding-right: 0px;
  text-align: center;
  /* background-color: yellow; */
}
.order .content ul .pro-status {
  float: left;
  width: 150px;
  padding-right: 0px;
  text-align: center;
  /* background-color: pink; */
}
.order .content ul .pro-delete {
  float: left;
  width: 100px;
  padding-right: 0px;
  text-align: center;
  /* background-color: lightgreen; */
}
.order .content ul .pro-total-in {
  color: #ff6700;
}

.order .order-bar {
  width: 1185px;
  padding: 0 20px;
  border-top: 1px solid #ff6700;
  height: 50px;
  line-height: 50px;
  background-color: #fff;
}
.order .order-bar .order-bar-left {
  float: left;
}
.order .order-bar .order-bar-left .order-total {
  color: #757575;
}
.order .order-bar .order-bar-left .order-total-num {
  color: #ff6700;
}
.order .order-bar .order-bar-right {
  float: right;
}
.order .order-bar .order-bar-right .total-price-title {
  color: #ff6700;
  font-size: 14px;
}
.order .order-bar .order-bar-right .total-price {
  color: #ff6700;
  font-size: 30px;
}
/* 订单列表CSS END */

/* 订单为空的时候显示的内容CSS */
.order .order-empty {
  width: 1225px;
  margin: 0 auto;
}
.order .order-empty .empty {
  height: 300px;
  padding: 0 0 130px 558px;
  margin: 65px 0 0;
  background: url(../assets/imgs/cart-empty.png) no-repeat 124px 0;
  color: #b0b0b0;
  overflow: hidden;
}
.order .order-empty .empty h2 {
  margin: 70px 0 15px;
  font-size: 36px;
}
.order .order-empty .empty p {
  margin: 0 0 20px;
  font-size: 20px;
}
/* 订单为空的时候显示的内容CSS END */
</style>