<!--
 * @Description: 修改密码组件
 * @Author: laufing
 * @Date: 2020-02-19 20:55:17
 * @LastEditors: laufing
 * @LastEditTime: 2020-03-01 15:34:08
 -->
<template>
  <div id="updatePw">
    <el-dialog title="修改密码" width="300px" center :visible.sync="isUpdatePw">
      <el-form
        :model="LoginUser"
        :rules="rules"
        status-icon
        ref="ruleForm"
        class="demo-ruleForm"
      >
        <el-form-item prop="name">
          <el-input
            prefix-icon="el-icon-user-solid"
            placeholder="请输入账号"
            v-model="LoginUser.name"
          ></el-input>
        </el-form-item>
        <el-form-item prop="originPw">
          <el-input
            prefix-icon="el-icon-view"
            type="password"
            placeholder="原始密码"
            v-model="LoginUser.originPw"
          ></el-input>
        </el-form-item>
        <el-form-item prop="newPw">
          <el-input
            prefix-icon="el-icon-view"
            type="password"
            placeholder="新密码"
            v-model="LoginUser.newPw"
          ></el-input>
        </el-form-item>
        <el-form-item prop="confirmNewPw">
          <el-input
            prefix-icon="el-icon-view"
            type="password"
            placeholder="确认密码"
            v-model="LoginUser.confirmNewPw"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button
            size="medium"
            type="primary"
            @click="updatePassword"
            style="width: 100%"
            >修改密码</el-button
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
  name: "UpdatePw",
  data() {
    // 用户名的校验方法
    let validateName = (rule, value, callback) => {
      if (!value) {
        return callback(new Error("请输入用户名"));
      }
      // 用户名以字母开头,长度在5-16之间,允许字母数字下划线
      const userNameRule = /^[a-zA-Z][a-zA-Z0-9_]{4,15}$/;
      // 正则测试输入的用户名
      if (userNameRule.test(value)) {
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
        originPw: "",
        newPw: "",
        confirmNewPw: "",
      },
      // 用户信息校验规则,validator(校验方法),trigger(触发方式),blur为在组件 Input 失去焦点时触发
      rules: {
        name: [{ validator: validateName, trigger: "blur" }],
        originPw: [{ validator: validatePass, trigger: "blur" }],
        newPw: [{ validator: validatePass, trigger: "blur" }],
        confirmNewPw: [{ validator: validatePass, trigger: "blur" }],
      },
    };
  },
  computed: {
    // 控制更新密码组件是否显示
    isUpdatePw: {
      get() {
        return this.$store.getters.getUpdatePw;
      },
      set(val) {
        this.$refs["ruleForm"].resetFields();
        this.setUpdatePw(val);
      },
    },
  },
  methods: {
    //将store中的actions方法映射到methods
    ...mapActions(["setUser", "setUpdatePw"]),

    // 点击修改密码触发
    updatePassword() {
      // 通过element自定义表单校验规则，校验用户输入的用户信息
      this.$refs["ruleForm"].validate((valid) => {
        //如果通过校验开始请求后端
        if (valid) {
          // 发送ajax
          // this.$axios
          console.log("开始发送请求，修改密码...")
          axios
            .post("/users/updatePassword/", {
              user: this.LoginUser.name,
              originPw: this.LoginUser.originPw,
              newPw: this.LoginUser.newPw,
              confirmNewPw: this.LoginUser.confirmNewPw,
              // withCredentials: true,
            })
            .then((res) =>{
              console.log("@@res", res);
              // 200代表登录成功，其他的均为失败
              if (res.data.code == 200) {
                // res.data为后端响应的json
                // 隐藏修改密码组件
                this.isUpdatePw = false;
                // 重新登录
                // this.setUser("");
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