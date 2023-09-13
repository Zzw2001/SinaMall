<template>
  <div>
    <!-- v2-template快捷指令
            自定义组件，配置路由router>index.js /user
            组件显示在 <router-view></router-view>
         -->
    <div class="user">
      <div class="user-header">
        <div class="user-title">
          <i class="el-icon-s-custom" style="color: #ff6700"></i>
          用户中心
        </div>
      </div>
    </div>

    <!-- 展示用户信息 -->
    <ul class="user-content">
      <li>
        <span>用户名:</span>
        <el-input type="text" v-model="userInfo.username" disabled></el-input>
      </li>
      <li>
        <span>手机号:</span>
        <el-input type="text" v-model="userInfo.mobile"></el-input>
      </li>

      <!-- 展示收货地址 -->
      <li v-for="(item, index) in userInfo.addresses" :key="item.id">
        <span>地址{{ index + 1 }}:</span>&nbsp;
        <!-- 删除按钮 -->
        <el-popover placement="right">
          <p>确定删除吗？</p>
          <div style="text-align: right; margin: 10px 0 0">
            <el-button
              type="primary"
              size="mini"
              @click="deleteAddr($event, item.id)"
              >确定</el-button
            >
          </div>
          <i class="el-icon-error" slot="reference" style="font-size: 18px"></i>
        </el-popover>
        <!-- 地址数据 -->
        <el-input type="text" v-model="item.receiver"></el-input>
        <el-input type="text" v-model="item.receive_mobile"></el-input>
        <el-input type="text" v-model="item.receive_addr"></el-input>
      </li>

      <li ref="controls">
        <el-button type="primary" plain @click="updateUserInfo"
          >修改信息</el-button
        >
        <el-button type="primary" round @click="updatePassword"
          >修改密码</el-button
        >
        <!-- 更新密码组件，控制显示隐藏 -->
        <UpdatePw></UpdatePw>

        <!-- 添加收货地址 -->
        <span>添加收货地址：</span>
        <el-input placeholder="收货人" v-model="receiver"></el-input>
        <el-input placeholder="手机号" v-model="receive_mobile"></el-input>
        <el-input placeholder="添加地址" v-model="receive_addr"></el-input>
        <el-checkbox v-model="is_default">是否默认</el-checkbox>
        <el-button class="addAddr" type="primary" round @click="addAddr"
          >添加地址</el-button
        >
      </li>
      <li style="{display:block, margin:20px,}" class="bottom-line"></li>
    </ul>
  </div>
</template>

<script>
import UpdatePw from "../components/UpdatePw.vue";
export default {
  name: "User",
  components: { UpdatePw, },
  data() {
    return {
      userInfo: {
        username: "",
        phone: "",
        addresses: [
          //   { id: 1, receiver:"", receive_mobile:"", receive_addr: "北京", is_default:true},
          //   { id: 2, receiver:"", receive_mobile:"", receive_addr: "上海", is_default:false},
        ],
      },
      receiver: "",//收货人
      receive_mobile: "", //收货手机号
      receive_addr: "", //收货地址
      is_default: false, //是否为默认地址
    };
  },
  props: {},

  //router-link被点击时，判断用户是否登录
  // 登录后向后端发送异步请求，获取用户信息
  activated() {
    //   未登录时，弹出登录组件
    if (!this.$store.getters.getUser.userName) {
      this.$store.dispatch("setShowLogin", true);
    }
    // 已登录，发送ajax请求，获取用户信息
    this.$axios
      .post("/users/userInfo/", {
        user: this.$store.getters.getUser,
      })
      .then((res) => {
        console.log("@@获取用户的信息：", res);
        if (res.data.code == 200) {
          this.userInfo = res.data.userInfo;
        } else {
          this.notifyError(res.data.msg);
        }
      })
      .catch((err) => {
        return Promise.reject(err);
      });
  },

  methods: {
    // 修改个人信息
    updateUserInfo() {
      console.log("修改个人信息...");
      this.$axios.post("/users/updateUserInfo/", {
        user: this.$store.getters.getUser,
        phone: this.userInfo.mobile,
        addr: this.userInfo.addresses,
      }).then(res=>{
        if(res.data.code == 200){
          this.notifySucceed(res.data.msg)
        }else{
          this.notifyError(res.data.msg)
        }
      })
    },

    // 更改个人密码
    updatePassword() {
      console.log("修改个人密码...");
      this.$store.dispatch("setUpdatePw", true);
    },

    deleteAddr(e, addr_id){
      // 删除该地址
      this.$axios.post("/users/deladdress/", {
        addr_id: addr_id,
      }).then(res=>{
        if(res.data.code == 200){
          // 删除vuex中的对应地址
          for(let i=0; i<this.userInfo.addresses.length; i++){
            let temp = this.userInfo.addresses[i]
            if(temp.id == addr_id){
              this.userInfo.addresses.splice(i, 1)
            }
          }
          this.notifySucceed(res.data.msg)
        }else{
          this.notifyError
        }
      })
    },
    // 添加地址
    addAddr() {
      console.log("增加地址...");
      this.$axios
        .post("/users/add_addrerss/", {
          user: this.$store.getters.getUser,
          receiver: this.receiver,
          receive_mobile: this.receive_mobile,
          receive_addr: this.receive_addr, //字符串地址
          is_default: this.is_default, //是否默认地址
        })
        .then((res) => {
          console.log("添加地址的响应:", res);
          if (res.data.code == 200) {
            this.userInfo.addrs.push(res.data.addr);
            this.receiver = ""
            this.receive_mobile = ""
            this.receive_addr = ""
            this.notifySucceed(res.data.msg);
          } else {
            this.notifyError(res.data.msg);
          }
        })
        .catch((err) => {
          return Promise.reject(err);
        });
    },
  },
};
</script>

<style scoped>
* {
  margin: 0;
}
.user {
  background-color: #f5f5f5;
}
.user .user-header {
  height: 64px;
  background-color: #fff;
  border-bottom: 2px solid #ff6700;
}
.user .user-header .user-title {
  width: 1225px;
  margin: 0 auto;
  height: 64px;
  line-height: 58px;
  font-size: 28px;
}
.userCenter {
  width: 1225px;
  margin: 0 auto;
  padding: 48px 0 0;
  background-color: #fff;
}
.user-content {
  width: 800px;
  margin: 0 auto;
  height: 600px;
  line-height: 58px;
  font-size: 16px;
}

.user-content .bottom-line {
  height: 64px;
  background-color: #fff;
  /* border-bottom: 2px solid #ff6700; */
}
.addAddr{
  margin-left:3.4%;
}
</style>
