<!--
 * @Description: 修改密码组件
 * @Author: laufing
 * @Date: 2020-02-19 20:55:17
 * @LastEditors: laufing
 * @LastEditTime: 2020-03-01 15:34:08
 -->
<template>
  <div id="addMyAddr">
    <el-dialog title="添加地址" width="300px" center :visible.sync="isAddMyAddr">
      <el-form
        :model="LoginUser"
        status-icon
        ref="ruleForm"
        class="demo-ruleForm"
      >
        <el-form-item prop="receiver">
          <el-input
            prefix-icon="el-icon-user-solid"
            placeholder="收件人"
            v-model="LoginUser.receiver"
          ></el-input>
        </el-form-item>
        <el-form-item prop="receive_mobile">
          <el-input
            prefix-icon="el-icon-view"
            type="text"
            placeholder="手机号"
            v-model="LoginUser.receive_mobile"
          ></el-input>
        </el-form-item>
        <el-form-item prop="receive_addr">
          <el-input
            prefix-icon="el-icon-view"
            type="text"
            placeholder="收件地址"
            v-model="LoginUser.receive_addr"
          ></el-input>
        </el-form-item>
        <el-form-item prop="is_default">
          <el-checkbox v-model="LoginUser.is_default">
            是否默认地址
          </el-checkbox>
        </el-form-item>
        <el-form-item>
          <el-button
            size="medium"
            type="primary"
            @click="addMyAddr"
            style="width: 100%"
            >添加地址</el-button
          >
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import axios from "axios";
axios.defaults.withCredentials = true;

export default {
  // 登录组件
  name: "AddMyAddr",
  data() {
    return {
      LoginUser: {
        receiver: "",
        receive_mobile: "",
        receive_addr: "",
        is_default: false,
      },
      
    };
  },
  computed: {
    // 获取vuex中的addMyAddr，控制添加地址组件是否显示
    isAddMyAddr: {
      get() {
        return this.$store.getters.getAddMyAddr;
      },
      set(val) {
        this.$refs["ruleForm"].resetFields();
        this.setAddMyAddr(val);
      },
    },
  },
  methods: {
    //将store中的actions方法映射到methods
    ...mapActions(["setUser", "setUpdatePw","setAddMyAddr"]),

    // 点击添加地址
    addMyAddr() {
      // 发送ajax
      // this.$axios
      console.log("开始发送请求，添加收货地址...")
      axios
        .post("/users/add_addrerss/", {
          user: this.$store.getters.getUser,
          receiver: this.LoginUser.receiver,
          receive_mobile: this.LoginUser.receive_mobile,
          receive_addr: this.LoginUser.receive_addr,
          is_default: this.LoginUser.is_default,
          // withCredentials: true,
        })
        .then((res) =>{
          console.log("@@res", res);
          // 200代表添加成功，其他的均为失败
          if (res.data.code == 200) {
            // 隐藏添加地址组件
            this.isAddMyAddr = false;
            this.$bus.$emit("test", res.data.addr)
            this.notifySucceed(res.data.msg)
            // this.$router.push("/confirmOrder")
          } else {
            //响应不是200
            // 清空输入框的校验状态
            // this.$refs["ruleForm"].resetFields();
            // 弹出通知框提示登录失败信息
            this.notifyError(res.data.msg);
          }
        })
        .catch((err) => {
          console.log(err);
          return Promise.reject(err);
        });
  
    },
  },
};
</script>
<style>
</style>