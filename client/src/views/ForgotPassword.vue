<template>
  <div>

    <div class="form-container">
      <a-card 
        title="Forgot Password"
        :bordered="false"
        :hoverable="true"
        style="margin: 30px;
        top: 20%;"
      >
      <Alert v-if="alertVisible" :show-icon="true" :closable="true" :type="alertType" :message = " alertMessage">
    </Alert>
        <a-form
          :model="formState"
          :validate-messages="validateMessages"
          name="forgot-password"
          class="forgot-password-form"
          @finish="onFinish"
          @submit="onSubmit"
          @finishFailed="onFinishFailed"
        >
          <a-form-item
            label="E-mail"
            name="email"
            :colon="false"
            :rules="[{type: 'email', required: true }]"
          >
            <a-input v-model:value="formState.email"></a-input>
          </a-form-item>
  
          <a-form-item>
            <a-button
              :disabled="disabled"
              type="primary"
              html-type="submit"
              class="forgot-password-button"
            >
              Send Link
            </a-button>
            Or
            <a href="/signup">register now!</a>
          </a-form-item>
        </a-form>
      </a-card>
    </div>
  </div>
  </template>
  
  <script>
  import { Alert } from 'ant-design-vue';
  import { defineComponent, reactive, computed,ref } from "vue";
  import axios from "axios";
  export default defineComponent({
  components: {
    Alert,
  },
  
    setup() {
      const alertVisible = ref(false);
      const alertType = ref('info');
      const alertMessage = ref('');

      const validateMessages = {
      required: "${label} is required!",
      types: {
        email: "this is not a valid email!",
      },
    };
      const formState = reactive({
        email: "",
      });
      const onFinish = (values) => {
        console.log("Success:", values);
      };
      const onFinishFailed = (errorInfo) => {
        console.log("Failed:", errorInfo);
      };
      const disabled = computed(() => {
        return !(formState.email);
      });
      const onSubmit = async () => {
        localStorage.removeItem["access"];
        await axios.post("auth/rest", formState).then((response) => {
            console.log(response);
            alertType.value = 'success';
            alertMessage.value = "Email has been sent";
            alertVisible.value = true;
          })
          .catch((error) => {
            alertType.value  = 'error';
            alertMessage.value  = error.response.data.message;
            alertVisible.value  = true;

            console.log(error);
          });
          
      };

      return {
        formState,
        onFinish,
        onSubmit,
        onFinishFailed,
        disabled,
        validateMessages,
        alertVisible,
        alertType,
        alertMessage,
      };
    },
  });
  </script>
  
  <style>
  .form-container {
    background: #ececec; padding: 30px; height: 100%; margin: 0; position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    overflow: auto;
  }
  .forgot-password--forgot {
    float: right;
  }
  .forgot-password--button {
    width: 100%;
  }
  </style>
  