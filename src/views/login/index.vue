<template>
<div>
  <video src="../../../video/wust.mp4" style="videocss" autoplay="true" loop="true" muted="true"></video>
  <div class="box-form">
    <div class="left">
      <div class="overlay">
        <h1 style="font-size: 100px">WUST2022</h1>
        <h2 style="font-size: 55px">遥感图像智能解译平台</h2>
      </div>
    </div>
    <div class="right">
      <h5>Login</h5>
      <p style="display: inline-block;">
        没有账号？点击注册
      </p>
      <p style="display: inline-block;visibility: hidden;">没有账号？点击注册</p>
      <div class="login-container">
        <el-form ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form" autocomplete="on" label-position="left">
          <el-form-item prop="username">
            <el-input ref="username" v-model="loginForm.username" placeholder="Username" name="username" type="text"
              tabindex="1" autocomplete="on" />
          </el-form-item>
          <el-tooltip v-model="capsTooltip" content="Caps lock is On" placement="right" manual>
            <el-form-item prop="password">
              <el-input :key="passwordType" ref="password" v-model="loginForm.password" :type="passwordType"
                placeholder="Password" name="password" tabindex="2" autocomplete="on" @keyup.native="checkCapslock"
                @blur="capsTooltip = false" @keyup.enter.native="handleLogin" />
              <span class="show-pwd" @click="showPwd">
                <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
              </span>
            </el-form-item>
          </el-tooltip>

          <el-button :loading="loading" type="primary" style="width:100%;margin-bottom:30px;"
            @click.native.prevent="handleLogin">Login</el-button>
        </el-form>
      </div>
    </div>
  </div>
  </div>
</template>

<script>
  import {
    validUsername
  } from "@/utils/validate"
  import SocialSign from "./components/SocialSignin";

  export default {
    name: "Login",
    components: {
      SocialSign
    },
    data() {
      const validateUsername = (rule, value, callback) => {
        if (!validUsername(value)) {
          callback(new Error("Please enter the correct user name"));
        } else {
          callback();
        }
      };
      const validatePassword = (rule, value, callback) => {
        if (value.length < 6) {
          callback(new Error("The password can not be less than 6 digits"));
        } else {
          callback();
        }
      };
      return {
        loginForm: {
          username: "admin",
          password: "111111",
        },
        loginRules: {
          username: [{
            required: true,
            trigger: "blur",
            validator: validateUsername
          }, ],
          password: [{
            required: true,
            trigger: "blur",
            validator: validatePassword
          }, ],
        },
        passwordType: "password",
        capsTooltip: false,
        loading: false,
        showDialog: false,
        redirect: undefined,
        otherQuery: {},
      };
    },
    watch: {
      $route: {
        handler: function(route) {
          const query = route.query;
          if (query) {
            this.redirect = query.redirect;
            this.otherQuery = this.getOtherQuery(query);
          }
        },
        immediate: true,
      },
    },
    created() {
      // window.addEventListener('storage', this.afterQRScan)
    },
    mounted() {
      if (this.loginForm.username === "") {
        this.$refs.username.focus();
      } else if (this.loginForm.password === "") {
        this.$refs.password.focus();
      }
    },
    destroyed() {
      // window.removeEventListener('storage', this.afterQRScan)
    },
    methods: {
      checkCapslock(e) {
        const {
          key
        } = e;
        this.capsTooltip = key && key.length === 1 && key >= "A" && key <= "Z";
      },
      showPwd() {
        if (this.passwordType === "password") {
          this.passwordType = "";
        } else {
          this.passwordType = "password";
        }
        this.$nextTick(() => {
          this.$refs.password.focus();
        });
      },
      handleLogin() {
        this.$refs.loginForm.validate((valid) => {
          if (valid) {
            this.loading = true;
            this.$store
              .dispatch("user/login", this.loginForm)
              .then(() => {
                this.$router.push({
                  path: this.redirect || "/",
                  query: this.otherQuery,
                });
                this.loading = false;
              })
              .catch(() => {
                this.loading = false;
              });
          } else {
            console.log("error submit!!");
            return false;
          }
        });
      },
      getOtherQuery(query) {
        return Object.keys(query).reduce((acc, cur) => {
          if (cur !== "redirect") {
            acc[cur] = query[cur];
          }
          return acc;
        }, {});
      },
    },
  };
</script>
<style lang="scss" scoped>
  video {
              position: fixed;
              right: 0;
              bottom: 0;
              width: auto;
              height: auto;
              z-index: -100;
              top: 0;
              left: 0;
              width: 100%;
              height: 100%;
              object-fit: fill;
              opacity: 0.5;
          }
  body {
    background-image: linear-gradient(135deg, #FAB2FF 10%, #1904E5 100%);
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    font-family: "Open Sans", sans-serif;
    color: #333333;
  }

  .box-form {
    margin: 30PX auto;
    width: 80%;
    background: #FFFFFF;
    border-radius: 10px;
    overflow: hidden;
    display: flex;
    flex: 1 1 100%;
    opacity: 0.7;
    align-items: stretch;
    justify-content: space-between;
    box-shadow: 0 0 20px 6px #090b6f85;
  }

  @media (max-width: 980px) {
    .box-form {
      flex-flow: wrap;
      text-align: center;
      align-content: center;
      align-items: center;
    }
  }

  .box-form div {
    height: auto;
  }

  .box-form .left {
    color: #FFFFFF;
    background-size: cover;
    background-repeat: no-repeat;
    background-image: url("../../../images/640.png")
  }

  .box-form .left .overlay {
    padding: 30px;
    width: 100%;
    height: 100%;
    background: #5961f9ad;
    overflow: hidden;
    box-sizing: border-box;
  }

  .box-form .left .overlay h1 {
    font-size: 10vmax;
    line-height: 1;
    font-weight: 900;
    margin-top: 40px;
    margin-bottom: 20px;
  }

  .box-form .left .overlay span p {
    margin-top: 30px;
    font-weight: 900;
  }

  .box-form .left .overlay span a {
    background: #3b5998;
    color: #FFFFFF;
    margin-top: 10px;
    padding: 14px 50px;
    border-radius: 100px;
    display: inline-block;
    box-shadow: 0 3px 6px 1px #042d4657;
  }

  .box-form .left .overlay span a:last-child {
    background: #1dcaff;
    margin-left: 30px;
  }

  .box-form .right {
    padding: 40px;
    overflow: hidden;
  }

  @media (max-width: 980px) {
    .box-form .right {
      width: 100%;
    }
  }

  .box-form .right h5 {
    font-size: 4vmax;
    line-height: 0;
  }

  .box-form .right p {
    font-size: 25px;
    color: #B0B3B9;
  }

  .box-form .right button {
    color: #fff;
    font-size: 16px;
    padding: 12px 35px;
    border-radius: 50px;
    display: inline-block;
    border: 0;
    outline: 0;
    box-shadow: 0px 4px 20px 0px #49c628a6;
    background-image: linear-gradient(135deg, #70F570 10%, #49C628 100%);
  }
</style>
<style lang="scss" scoped>
  $bg: #2d3a4b;
  $dark_gray: #889aa4;
  $light_gray: #eee;

  .login-container {
    .login-form {
      position: relative;
      width: 520px;
      max-width: 100%;
      padding: 50px 0px 0;
      margin: 0 auto;
      overflow: hidden;
    }
    .tips {
      font-size: 14px;
      // color: #fff;
      margin-bottom: 10px;
      span {
        &:first-of-type {
          margin-right: 16px;
        }
      }
    }
    .title-container {
      position: relative;
      .title {
        font-size: 26px;
        /* 字体颜色 */
        color: $light_gray;
        margin: 0px auto 40px auto;
        text-align: center;
        font-weight: bold;
      }
    }

    .show-pwd {
      position: absolute;
      right: 10px;
      top: 7px;
      font-size: 16px;
      color: $dark_gray;
      cursor: pointer;
      user-select: none;
    }

    .thirdparty-button {
      position: absolute;
      right: 0;
      bottom: 6px;
    }

    @media only screen and (max-width: 470px) {
      .thirdparty-button {
        display: none;
      }
    }
  }
</style>
<style lang="scss">
  /* 修复input 背景不协调 和光标变色 */
  /* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

  $bg: #283443;
  $light_gray: #fff;
  $cursor: #fff;

  @supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
    .login-container .el-input input {
      color: $cursor;
    }
  }

  /* reset element-ui css */
  .login-container {
    .el-input {
      display: inline-block;
      height: 47px;
      width: 85%;
      input {
        background: transparent;
        border: 0px;
        -webkit-appearance: none;
        border-radius: 0px;
        padding: 12px 5px 12px 15px;
        color: $light_gray;
        height: 47px;
        caret-color: $cursor;

        &:-webkit-autofill {
          box-shadow: 0 0 0px 1000px $bg inset !important;
          -webkit-text-fill-color: $cursor !important;
        }
      }
    }

    .el-form-item {
      border: 1px solid rgba(255, 255, 255, 0.1);
      background: rgba(0, 0, 0, 0.2);
      border-radius: 5px;
      color: #454545;
    }
  }
</style>
