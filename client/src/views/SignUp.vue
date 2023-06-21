<template>
<div class="form-container">
    <Alert v-if="alertVisible" :show-icon="true" :closable="true" :type="alertType" :message = " alertMessage">
    </Alert>
    <a-card
      title="Sign Up"
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
          :name="['User', 'username']"
          label="Username"
          :colon="false"
          :rules="[{ required: true }, { pattern: /^[a-zA-Z0-9_]+$/, message: 'Username can only contain letters, numbers and underscores' }]"
        >
          <a-input v-model:value="formState.User.username" />
        </a-form-item>
        <a-form-item
          :name="['User', 'first_name']"
          label="Firstname"
          :colon="false"
          :rules="[{ required: true }]"
        >
          <a-input v-model:value="formState.User.first_name" />
        </a-form-item>
        <a-form-item
          :name="['User', 'last_name']"
          label="Lastname"
          :colon="false"
          :rules="[{ required: true }]"
        >
          <a-input v-model:value="formState.User.last_name" />
        </a-form-item>
        <a-form-item
          :name="['User', 'email']"
          label="Email"
          :colon="false"
          :rules="[{ type: 'email', required: true }]"
        >
          <a-input v-model:value="formState.User.email" />
        </a-form-item>
        <a-form-item
          :name="['User', 'password']"
          label="Password"
          :colon="false"
          :rules="[{ required: true }]"
        >
          <a-input-password v-model:value="formState.User.password" />
        </a-form-item>
        <a-form-item
          :name="['User', 're_password']"
          label="Confirm Password"
          :colon="false"
          :rules="[{ required: true }, {validator: validatePass}]"
        >
          <a-input-password v-model:value="formState.User.re_password" />
        </a-form-item>
        <a-form-item
          :name="['User', 'birthdate']"
          label="Birthdate"
          :colon="false"
          :rules="[{ required: true }]"
          
        >
          <a-date-picker
            v-model:value="formState.User.birthdate"
            value-format="YYYY-MM-DD"
          />
        </a-form-item>
        <a-form-item  label="Gender" :colon="false" :rules="[{ required: true }]" :name="['User', 'gender']">
          <a-radio-group v-model:value="formState.User.gender" >
            <a-radio value="M" >Male</a-radio>
            <a-radio value="F" >Female</a-radio>
          </a-radio-group>
        </a-form-item>
        <a-form-item  label="Role" :colon="false" :rules="[{ required: true }]" :name="['User', 'role']">
          <a-radio-group v-model:value="formState.User.role">
            <a-radio value=1>Student</a-radio>
            <a-radio value=2 >Teaching Assistant</a-radio>
            <a-radio value=3 >Professor</a-radio>
          </a-radio-group>
        </a-form-item>
        <a-form-item :wrapper-col="{ ...layout.wrapperCol, offset: 6 }">
          <a-button type="primary" html-type="submit">Submit</a-button>
          Or
          <a href="/login">Log In!</a>
        </a-form-item>
      </a-form>
    </a-card>
  </div>
</template>

<script>
import { Alert } from 'ant-design-vue';
import { defineComponent, reactive, ref } from "vue";
import { signUp} from '../services/auth'

export default defineComponent({
  components: {
    Alert,
  },
  setup() {
    const alertVisible = ref(false);
    const alertType = ref('info');
    const alertMessage = ref('');

    const layout = {
      labelCol: {
        span: 6,
      },
      wrapperCol: {
        span: 12,
      },
    };
    let validatePass = async (_rule, value) => {
      if (value === '') {
        return Promise.reject('Please input the password again');
      } else if (value !== formState.User.password) {
        return Promise.reject("Two inputs don't match!");
      } else {
        return Promise.resolve();
      }
    };
    const validateMessages = {
      required: "${label} is required!",
      types: {
        email: "${label} is not a valid email!",
        number: "${label} is not a valid number!",
      },
      number: {
        range: "${label} must be between ${min} and ${max}",
      },
      
    };

    const formState = reactive({
      User: {
        username: "",
        first_name: "",
        last_name: "",
        email: "",
        password: "",
        gender: "",
        birthdate:"",
        role:"",
        re_password: "",
      },
    });
    const onFinish = (values) => {
      console.log("Success:", values);
    };
    const onSubmit = async () => {

    try {
    const response = await signUp(formState.User)
    console.log(response);
    alertType.value = 'success';
    alertMessage.value = "Verification Email has been sent";
    alertVisible.value = true;

    return response.data.user
    } catch (error) {
      console.log(error);
      alertType.value  = 'error';
      alertMessage.value  = "";

      for (const key in error.response.data) {
          if (Object.hasOwnProperty.call(error.response.data, key)) {
            const value = error.response.data[key];
            alertMessage.value  += value + "\n"
          }
        }

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
});
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
