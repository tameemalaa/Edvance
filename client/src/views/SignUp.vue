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
          :name="['user', 'username']"
          label="Username"
          :colon="false"
          :rules="[{ required: true }, { pattern: /^[a-zA-Z0-9_]+$/, message: 'Username can only contain letters, numbers and underscores' }]"
        >
          <a-input v-model:value="formState.user.username" />
        </a-form-item>
        <a-form-item
          :name="['user', 'firstname']"
          label="Firstname"
          :colon="false"
          :rules="[{ required: true }]"
        >
          <a-input v-model:value="formState.user.firstname" />
        </a-form-item>
        <a-form-item
          :name="['user', 'lastname']"
          label="Lastname"
          :colon="false"
          :rules="[{ required: true }]"
        >
          <a-input v-model:value="formState.user.lastname" />
        </a-form-item>
        <a-form-item
          :name="['user', 'email']"
          label="Email"
          :colon="false"
          :rules="[{ type: 'email', required: true }]"
        >
          <a-input v-model:value="formState.user.email" />
        </a-form-item>
        <a-form-item
          :name="['user', 'password']"
          label="Password"
          :colon="false"
          :rules="[{ required: true }]"
        >
          <a-input-password v-model:value="formState.user.password" />
        </a-form-item>
        <a-form-item
          :name="['user', 'confirmPassword']"
          label="Confirm Password"
          :colon="false"
          :rules="[{ required: true }, {validator: validatePass}]"
        >
          <a-input-password v-model:value="formState.user.confirmPassword" />
        </a-form-item>
        <a-form-item
          :name="['user', 'birthdate']"
          label="Birthdate"
          :colon="false"
          :rules="[{ required: true }]"
          
        >
          <a-date-picker
            v-model:value="formState.user.birthdate"
            value-format="YYYY-MM-DD"
          />
        </a-form-item>
        <a-form-item  label="Gender" :colon="false" :rules="[{ required: true }]" :name="['user', 'gender']">
          <a-radio-group v-model:value="formState.user.gender" >
            <a-radio value="M" >Male</a-radio>
            <a-radio value="F" >Female</a-radio>
          </a-radio-group>
        </a-form-item>
        <a-form-item  label="Role" :colon="false" :rules="[{ required: true }]" :name="['user', 'role']">
          <a-radio-group v-model:value="formState.user.role">
            <a-radio value="student">Student</a-radio>
            <a-radio value="professor" >Professor</a-radio>
            <a-radio value="TA" >TA</a-radio>
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
      } else if (value !== formState.user.password) {
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
      user: {
        username: "",
        firstname: "",
        lastname: "",
        email: "",
        password: "",
        gender: "",
        birthdate:"",
        role:"",
      },
    });
    const onFinish = (values) => {
      console.log("Success:", values);
    };
    const onSubmit = async () => {

    try {
    // Make a POST request to the Django API with the signup form data
    const response = await signUp(formState.user)
    console.log(response);
    alertType.value = 'success';
    alertMessage.value = "Verification Email has been sent";
    alertVisible.value = true;

    return response.data.user
    } catch (error) {
      alertType.value  = 'error';
      alertMessage.value  = error.response.data.message;
      alertVisible.value  = true;

      console.log(error);
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
