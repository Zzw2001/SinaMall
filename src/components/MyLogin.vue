<!--
 * @Description: 登录组件
 * @Author: hai-27
 * @Date: 2020-02-19 20:55:17
 * @LastEditors: hai-27
 * @LastEditTime: 2020-03-01 15:34:08
 -->
<template>
  <div id="myLogin">
    <el-dialog title="登录" width="300px" center :visible.sync="isLogin">
      <el-form
        :model="LoginUser"
        :rules="rules"
        status-icon
        ref="ruleForm"
        class="demo-ruleForm"
      >
        <!-- 用户名 -->
        <el-form-item prop="name">
          <el-input
            prefix-icon="el-icon-user-solid"
            placeholder="请输入账号"
            v-model="LoginUser.name"
          ></el-input>
        </el-form-item>

        <!-- 用户密码 -->
        <el-form-item prop="pass">
          <el-input
            prefix-icon="el-icon-view"
            type="password"
            placeholder="请输入密码"
            v-model="LoginUser.pass"
          ></el-input>
        </el-form-item>

        <!-- 点击登录 -->
        <el-form-item>
          <el-button
            size="medium"
            type="primary"
            @click="Login"
            style="width: 100%"
            >登录</el-button
          >
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  // 登录组件
  name: "MyLogin",
  data() {
    // 用户名的校验方法
    let validateName = (rule, value, callback) => {
      if (!value) {
        return callback(new Error("请输入用户名"));
      }
      // 用户名以字母开头,长度在5-16之间,允许字母数字下划线
      const userNameRule = /^[a-zA-Z][a-zA-Z0-9_]{4,15}$/;
      const mobileRule = /^1[3-9]\d{9}$/; // 手机号的验证规则
      // 正则测试输入的用户名
      if (userNameRule.test(value) | mobileRule.test(value)) {
        // 选择节点，设置验证通过
        this.$refs.ruleForm.validateField("checkPass");
        return callback();
      } else {
        //用户名验证未通过
        return callback(new Error("字母开头,长度5-16之间,允许字母数字下划线"));
      }
    };
    // 密码的校验方法
    let validatePass = (rule, value, callback) => {
      if (value === "") {
        return callback(new Error("请输入密码"));
      }
      // 密码以字母开头,长度在6-18之间,允许字母数字和下划线
      const passwordRule = /^[a-zA-Z]\w{5,17}$/;
      if (passwordRule.test(value)) {
        this.$refs.ruleForm.validateField("checkPass");
        return callback();
      } else {
        //密码验证未通过
        return callback(
          new Error("字母开头,长度6-18之间,允许字母数字和下划线")
        );
      }
    };
    return {
      LoginUser: {
        name: "",
        pass: "",
      },
      // 用户信息校验规则,validator(校验方法),trigger(触发方式),blur为在组件 Input 失去焦点时触发
      rules: {
        name: [{ validator: validateName, trigger: "blur" }],
        pass: [{ validator: validatePass, trigger: "blur" }],
      },
    };
  },
  computed: {
    // 获取vuex中的showLogin，控制登录组件是否显示
    isLogin: {
      get() {
        return this.$store.getters.getShowLogin;
      },
      set(val) {
        this.$refs["ruleForm"].resetFields();
        this.setShowLogin(val);
      },
    },
  },
  methods: {
    //将store中的actions方法映射到methods
    ...mapActions(["setUser", "setShowLogin"]),

    // 点击登录触发
    Login() {
      // 通过element自定义表单校验规则，校验用户输入的用户信息
      this.$refs["ruleForm"].validate((valid) => {
        //如果通过校验开始登录
        if (valid) {
          // 发送ajax
          this.$axios
            .post("/users/login/", {
              user: this.LoginUser.name,
              pwd: this.LoginUser.pass,
              // withCredentials: true,
            })
            .then((res) => {
              console.log("@@登录的响应：", res.data);
              // 200代表登录成功，其他的均为失败
              if (res.data.code == 200) {
                // res.data为后端响应的json
                // 隐藏登录组件
                this.isLogin = false;
                // 登录信息存到本地缓存
                let user = JSON.stringify(res.data.user);
                console.log("@@user", user);
                //要求后台返回什么样的数据？
                //{
                //     "code":200,
                //     'msg': "欢迎user",
                //     "user":{
                //       userName:"xxx",
                //     },
                //
                //}
                // 前端存储用户信息，表示登录成功
                localStorage.setItem("user", user);
                localStorage.setItem('token',res.data.token);
                // sessionStorage.setItem("")
                // 登录信息存到vuex,控制页面欢迎信息
                // console.log("@@res.data.user", res.data.user)
                this.setUser(res.data.user);
                // 弹出通知框提示登录成功信息
                this.notifySucceed(res.data.msg);
              } else {
                //响应不是200
                // 清空输入框的校验状态
                this.$refs["ruleForm"].resetFields();
                // 弹出通知框提示登录失败信息
                this.notifyError(res.data.msg);
              }
            })
            .catch((err) => {
              console.log(err);
              return Promise.reject(err);
            });
        } else {
          //未通过用户校验
          return false;
        }
      });
    },
  },
};
</script>
<style>
</style>