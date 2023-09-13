<!--
 * @Description: 用户注册组件
 * @Author: hai-27
 * @Date: 2020-02-19 22:20:35
 * @LastEditors: hai-27
 * @LastEditTime: 2020-03-01 15:34:34
 -->
<template>
  <div id="register">
    <el-dialog title="注册" width="300px" center :visible.sync="isRegister">
      <el-form
        :model="RegisterUser"
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
            v-model="RegisterUser.name"
          ></el-input>
        </el-form-item>
        <!-- 密码 -->
        <el-form-item prop="pass">
          <el-input
            prefix-icon="el-icon-view"
            type="password"
            placeholder="请输入密码"
            v-model="RegisterUser.pass"
          ></el-input>
        </el-form-item>
        <!-- 确认密码 -->
        <el-form-item prop="confirmPass">
          <el-input
            prefix-icon="el-icon-view"
            type="password"
            placeholder="请再次输入密码"
            v-model="RegisterUser.confirmPass"
          ></el-input>
        </el-form-item>

        <!-- 输入手机号 -->
        <el-form-item prop="mobile">
          <el-input
            prefix-icon="el-icon-user-solid"
            placeholder="请输入手机号"
            v-model="RegisterUser.mobile"
          ></el-input>
        </el-form-item>

        <!-- 增加的内容 -->
        <el-form-item prop="imageCode">
          <!-- 图片验证码 -->
          <el-input
            placeholder="输入验证码"
            v-model="RegisterUser.imageCode"
            :style="{ width: '60%' }"
          ></el-input>
          <img
            class="imageCode"
            v-bind:src="iamgeCodeUrl"
            alt="图形验证码"
            @click="genImageCode"
          />
        </el-form-item>
        <!-- 是否同意商城协议 -->
        <el-form-item prop="aggreement">
          <el-checkbox v-model="aggree">
            <label class="aggreement"
              >同意'商城用户使用协议'</label
            > </el-checkbox
          ><br />
          <span class="error_tip" v-show="flag">请勾选用户协议</span>
        </el-form-item>

        <!-- 点击注册 -->
        <el-form-item>
          <el-button
            size="medium"
            type="primary"
            @click="Register"
            style="width: 100%"
            >注册</el-button
          >
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>
<script>
// 生成uuid
import { v4 as uuid4 } from "uuid";
export default {
  name: "MyRegister",
  // 子组件接收父组件传来的值
  props: ["register"],
  data() {
    // 用户名的校验方法
    let validateName = (rule, value, callback) => {
      if (!value) {
        return callback(new Error("请输入用户名"));
      }
      // 用户名以字母开头,长度在5-16之间,允许字母数字下划线
      const userNameRule = /^[a-zA-Z][a-zA-Z0-9_]{4,15}$/;
      if (userNameRule.test(value)) {
        // 前端校验，用户名复合规则
        //请求后端， 判断用户名是否重复
        this.$axios
          .get("/users/check/username/" + this.RegisterUser.name + "/")
          .then((res) => {
            // 200代表用户名不重复，可以注册
            console.log("校验用户名是否重复：", res);
            if (res.data.code == 200) {
              this.$refs.ruleForm.validateField("checkPass");
              return callback();
            } else {
              // 用户名重复或者不符合规则
              return callback(new Error(res.data.msg));
            }
          })
          .catch((err) => {
            return Promise.reject(err);
          });
      } else {
        // 前端校验，用户名不符合规则
        return callback(new Error("字母开头,长度5-16之间,允许字母数字下划线"));
      }
    };
    // 手机号的校验方法
    let validateMobile = (rule, value, callback) => {
      if (value === "") {
        return callback(new Error("请输入手机号"));
      }
      // 手机号以1开头,第二位3-9之间的数字，长度为11,只允许数字
      const mobileRule = /^1[3-9]\d{9}$/;
      if (mobileRule.test(value)) {
        this.$axios
          .get("/users/check/mobile/" + this.RegisterUser.mobile + "/")
          .then((res) => {
            console.log("验证手机号是否可用:", res);
            if (res.data.code == 200) {
              this.$refs.ruleForm.validateField("checkPass");
              return callback();
            } else {
              return callback(new Error(res.data.msg));
            }
          })
          .catch((err) => {
            return Promise.reject(err);
          });
      } else {
        return callback(new Error("手机号不符合格式"));
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
        return callback(
          new Error("字母开头,长度6-18之间,允许字母数字和下划线")
        );
      }
    };
    // 确认密码的校验方法
    let validateConfirmPass = (rule, value, callback) => {
      if (value === "") {
        return callback(new Error("请输入确认密码"));
      }
      // 校验是否以密码一致
      if (this.RegisterUser.pass != "" && value === this.RegisterUser.pass) {
        this.$refs.ruleForm.validateField("checkPass");
        return callback();
      } else {
        return callback(new Error("两次输入的密码不一致"));
      }
    };
    // 校验图片验证码
    let validateImageCode = (rule, value, callback) => {
      if (value === "") {
        return callback(new Error("请输入图片验证码"));
      }
      // 图片验证码是由字母、数字组成，长度为4
      const iamgeCodeRule = /^[a-zA-Z0-9]{4}$/;
      if (iamgeCodeRule.test(value)) {
        this.$axios
          .get("/users/check_image_code/", {
            params: {
              imageCodeID: this.imageCodeID,
              imageCode: this.RegisterUser.imageCode,
            },
          })
          .then((res) => {
            if (res.data.code == 200) {
              this.$refs.ruleForm.validateField("checkPass");
              return callback();
            } else {
              return callback(new Error(res.data.msg));
            }
          })
          .catch((err) => {
            return Promise.reject(err);
          });
      } else {
        return callback(new Error("图片验证码不正确！"));
      }
    };
    return {
      imageCodeID: "", //即生成的uuid
      iamgeCodeUrl: "", //图形验证码的地址
      isRegister: false, // 控制注册组件是否显示
      aggree: false, //是否同意协议
      flag: false,
      // 返回的是注册用户信息
      RegisterUser: {
        name: "",
        pass: "",
        confirmPass: "",
        mobile: "",
        imageCode: "", //用户输入的图片验证码
      },
      // 用户信息校验规则,validator(校验方法),trigger(触发方式),blur为在组件 Input 失去焦点时触发
      rules: {
        // 这里的属性值，是prop的值
        // blur 输入框失去焦点时触发的方法
        name: [{ validator: validateName, trigger: "blur" }],
        pass: [{ validator: validatePass, trigger: "blur" }],
        confirmPass: [{ validator: validateConfirmPass, trigger: "blur" }],
        mobile: [{ validator: validateMobile, trigger: "blur" }],
        imageCode: [{ validator: validateImageCode, trigger: "blur" }], // 校验图片验证码
      },
    };
  },

  watch: {
    // 监听父组件传过来的register变量，设置this.isRegister的值
    register: function (val) {
      if (val) {
        this.isRegister = val;
      }
    },
    // 监听this.isRegister变量的值，更新父组件register变量的值
    isRegister: function (val) {
      if (!val) {
        this.$refs["ruleForm"].resetFields();
        this.$emit("fromChild", val);
      }
    },
  },
  mounted() {
    // DOM节点刚刚完成挂载，生成默认的图形验证码
    this.genImageCode();
  },
  methods: {
    // 生成图片验证码地址
    genImageCode() {
      // 生成一个uuid
      (this.imageCodeID = uuid4()),
        // 生成一个图片验证码地址
        (this.iamgeCodeUrl = "/users/image_code/" + this.imageCodeID + "/");
    },

    // 用户注册
    Register() {
      // 是否同意用户协议
      if (!this.aggree) {
        this.flag = true;
        return;
      }
      // 已勾选，则不显示提示信息
      this.flag = false;
      // 通过element自定义表单校验规则，校验用户输入的用户信息
      // 通过$refs去找到form表单中的ruleform组件,然后校验
      this.$refs["ruleForm"].validate((valid) => {
        //如果通过校验开始注册
        if (valid) {
          // 调用后端接口
          this.$axios
            .post("/users/register/", {
              userName: this.RegisterUser.name,
              pwd: this.RegisterUser.pass,
              mobile: this.RegisterUser.mobile,
              agree: this.aggree,
            })
            .then((res) => {
              // 200代表注册成功，其他的均为失败
              if (res.data.code == 201) {
                // 隐藏注册组件
                this.isRegister = false;
                // 弹出通知框提示注册成功信息
                this.notifySucceed(res.data.msg);
              } else {
                // 弹出通知框提示注册失败信息
                this.notifyError(res.data.msg);
              }
            })
            .catch((err) => {
              return Promise.reject(err);
            });
        } else {
          // 没有验证通过抛出异常
          return false;
        }
      });
    },
  },
};
</script>
<style>
.imageCode {
  /* padding-top:2%; */
  margin-bottom: -12px;
  width: 95px;
  height: 35px;
}
.aggreement {
  font-size: 10px;
  color: blue;
}
.error_tip {
  font-size: 3px;
  color: red;
}
</style>