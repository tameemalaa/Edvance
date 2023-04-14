<template>
  <div class = "form-container">
    <Alert v-if="alertVisible" :show-icon="true" :closable="true" :type="alertType" :message = " alertMessage">
    </Alert>

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
          <a-form-item name="rememberMe" no-style>
            <a-checkbox v-model:checked="formState.rememberMe"
              >Remember me</a-checkbox
            >
          </a-form-item>
          <a class="login-form-forgot" href="forgotpassword">Forgot password</a>
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
import { Alert } from 'ant-design-vue';
import { defineComponent, reactive, computed,ref} from "vue";
import { UserOutlined, LockOutlined } from "@ant-design/icons-vue";
import { logIn} from '../services/auth'
import { setJWTToken } from '../services/token'
import router from "../router";

export default defineComponent({
  components: {
    UserOutlined,
    LockOutlined,
    Alert,
  },  
  setup() {
    const formState = reactive({
      username: "",
      password: "",
      rememberMe: true,
    });
    const alertVisible = ref(false);
    const alertType = ref('info');
    const alertMessage = ref('');

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
      try {
        const response = await logIn(formState)
        setJWTToken(response.data.access_token)
        router.push("/");
        console.log("Success:", response);
        return response.data.user
      } catch (error) {
        console.log("Failed:", error);
          alertType.value  = 'error';
          alertMessage.value  = error.response.data.message;
          alertVisible.value  = true;
      }
    };
    return {
      formState,
      onFinish,
      onSubmit,
      onFinishFailed,
      disabled,
      alertVisible,
      alertType,
      alertMessage,
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
.form-container{
  background: #ececec; padding: 30px; height: 100%; margin: 0; position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  overflow: auto;
}
</style>
