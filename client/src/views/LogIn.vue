<template>
<div class="form-container">
    <a-card
      title="Log In"
      :bordered="false"
      :hoverable="true"
      style="margin: 30px;
      top: 20%;"
    >
      <a-form
        :model="formState"
        name="normal_login"
        class="login-form"
        @finish="onFinish"
        @submit="onSubmit"
        @finishFailed="onFinishFailed"
      >
        <a-form-item
          label="Username / E-mail"
          name="username"
          :colon="false"
          :rules="[{ required: true, message: 'Please input your username!' }]"
        >
          <a-input v-model:value="formState.username">
            <template #prefix>
              <UserOutlined class="site-form-item-icon" />
            </template>
          </a-input>
        </a-form-item>

        <a-form-item
          label="Password"
          name="password"
          :colon="false"
          :rules="[{ required: true, message: 'Please input your password!' }]"
        >
          <a-input-password v-model:value="formState.password">
            <template #prefix>
              <LockOutlined class="site-form-item-icon" />
            </template>
          </a-input-password>
        </a-form-item>

        <a-form-item>
          <a-form-item name="remember" no-style>
            <a-checkbox v-model:checked="formState.remember"
              >Remember me</a-checkbox
            >
          </a-form-item>
          <a class="login-form-forgot" href="forgot-password">Forgot password</a>
        </a-form-item>

        <a-form-item>
          <a-button
            :disabled="disabled"
            type="primary"
            html-type="submit"
            class="login-form-button"
          >
            Log in
          </a-button>
          Or
          <a href="/signup">register now!</a>
        </a-form-item>
      </a-form>
    </a-card>
  </div>
</template>
<script>
import { defineComponent, reactive, computed } from "vue";
import { UserOutlined, LockOutlined } from "@ant-design/icons-vue";
import axios from "axios";
import router from "../router";
import store from "@/store";
export default defineComponent({
  components: {
    UserOutlined,
    LockOutlined,
  },
  setup() {
    const formState = reactive({
      username: "",
      password: "",
      remember: true,
    });
    const onFinish = (values) => {
      console.log("Success:", values);
    };
    const onFinishFailed = (errorInfo) => {
      console.log("Failed:", errorInfo);
    };
    const disabled = computed(() => {
      return !(formState.username && formState.password);
    });
    const onSubmit = async () => {
      localStorage.removeItem["access"];

      await axios
        .post("auth/login", formState)
        .then((response) => {
          console.log(response);
          const access = response.data.access;
          store.commit("setAccess", access);
          axios.defaults.headers.common["Authorization"] = "JWT " + access;
          router.push("/");
        })
        .catch((error) => {
          console.log(error);
        });
    };
    return {
      formState,
      onFinish,
      onSubmit,
      onFinishFailed,
      disabled,
    };
  },
});
</script>
<style>
#components-form-demo-normal-login .login-form-forgot {
  float: right;
}
#components-form-demo-normal-login .login-form-button {
  width: 100%;
}
</style>
