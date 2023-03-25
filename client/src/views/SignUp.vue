<template>
    <div style="background: #ececec; padding: 30px; height: 100%; margin: 0; position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  overflow: auto;">
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
          :rules="[{ required: true }]"
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
          :rules="[{ required: true }]"
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
        <a-form-item :name="['user', 'gender']" label="Gender" :colon="false">
          <a-radio-group v-model:value="formState.gender">
            <a-radio value="M">Male</a-radio>
            <a-radio value="F">Female</a-radio>
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
import axios from "axios";
import { defineComponent, reactive } from "vue";
import router from "../router";
export default defineComponent({
  setup() {
    const layout = {
      labelCol: {
        span: 6,
      },
      wrapperCol: {
        span: 12,
      },
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
        name: "",
        age: undefined,
        email: "",
        password: "",
        website: "",
        introduction: "",
      },
    });
    const onFinish = (values) => {
      console.log("Success:", values);
    };
    const onSubmit = async () => {
      await axios
        .post("auth/register", formState.user)
        .then((response) => {
          console.log(response);
          router.push("/login");
        })
        .catch((error) => {
          console.log(error);
        });
    };

    return {
      formState,
      onFinish,
      onSubmit,
      layout,
      validateMessages,
    };
  },
});
</script>
