<template>
<div class="form-container">
  <Alert v-if="alertVisible" :show-icon="true" :closable="true" :type="alertType" :message = " alertMessage">
    </Alert>
        <a-card
          title="Rest Password"
          :bordered="false"
          :hoverable="true"
          style="margin: 30px;"
        >
          <a-form
            :model="formState"
            v-bind="layout"
            name="nest-messages"
            :validate-messages="validateMessages"
            @finish="onFinish"
            @submit="onSubmit"
          >
            <a-form-item
              :name="['password', 'password']"
              label="Password"
              :colon="false"
              :rules="[{ required: true }]"
            >
              <a-input-password v-model:value="formState.password.password" />
            </a-form-item>
            <a-form-item
              :name="['password', 'confirmPassword']"
              label="Confirm Password"
              :colon="false"
              :rules="[{ required: true }, {validator: validatePass}]"
            >
              <a-input-password v-model:value="formState.password.confirmPassword" />
            </a-form-item>
            <a-form-item :wrapper-col="{ ...layout.wrapperCol, offset: 6 }">
              <a-button type="primary" html-type="submit">Submit</a-button>
            </a-form-item>
          </a-form>
        </a-card>
      </div>
    </template>
    
<script>
import { Alert } from 'ant-design-vue';
import { defineComponent, reactive, ref} from "vue";
import { verifyResetToken,resetPassword} from '../services/auth'
import router from "../router";

export default defineComponent({
  components: {
    Alert,
  }, 
  props: {
    token: {
      type: String,
      required: true
    }}, 

    async mounted(){
      if (await verifyResetToken(this.token)) {
        console.log("Success");
      } else {
        router.push("/login");
      }
    },

    setup() {
    const layout = {
      labelCol: {
        span: 6,
      },
      wrapperCol: {
        span: 12,
      },
    };
    const alertVisible = ref(false);
    const alertType = ref('info');
    const alertMessage = ref('');

    let validatePass = async (_rule, value) => {
      if (value === '') {
        return Promise.reject('Please input the password again');
      } else if (value !== formState.password.password) {
        return Promise.reject("Two inputs don't match!");
      } else {
        return Promise.resolve();
      }
    };
    const validateMessages = {
      required: "${label} is required!",
    };

    const formState = reactive({
      password: {
        password: "",
        confirmPassword: "",
      },
    });

    const onFinish = (values) => {
      console.log("Success:", values);
    };
    const onSubmit = async () => {
    try {
    const response = await resetPassword(formState.password)
    console.log(response);
    router.push("/login");
    return response.data.password
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
      layout,
      validateMessages,
      validatePass,
      alertVisible,
      alertType,
      alertMessage,
    };
  },
},
);
</script>
<style>
.form-container{
  background: #ececec; padding: 30px; height: 100%; margin: 0; position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  overflow: auto;
}
</style>
