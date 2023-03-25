<template>
    <a-form
      :model="formState"
      v-bind="layout"
      name="nest-messages"
      :validate-messages="validateMessages"
      @finish="onFinish"
    >
      <a-form-item :name="['user', 'username']" label="Username" :rules="[{ required: true }]">
        <a-input v-model:value="formState.user.username" />
      </a-form-item>
      <a-form-item :name="['user', 'firstname']" label="Firstname" :rules="[{ required: true }]">
        <a-input v-model:value="formState.user.firstname" />
    </a-form-item>
        <a-form-item :name="['user', 'lastname']" label="Lastname" :rules="[{ required: true }]">
        <a-input v-model:value="formState.user.lastname" />
    </a-form-item>
        <a-form-item :name="['user', 'email']" label="Email" :rules="[{ type: 'email',required: true }]">
        <a-input v-model:value="formState.user.email" />
      </a-form-item>
      <a-form-item :name="['user', 'password']" label="Password" :rules="[{ required: true}]">
        <a-input-password v-model:value="formState.user.password" />
      </a-form-item>
      <a-form-item :name="['user', 'confirmPassword']" label="Confirm Password" :rules="[{ required: true}]">
        <a-input-password v-model:value="formState.user.confirmPassword" />
    </a-form-item>
    <a-form-item :name="['user','birthdate']" label="Birthdate" rules="[{ required: true}]">
      <a-date-picker v-model:value="formState.user.birthdate" value-format="YYYY-MM-DD" />
</a-form-item>
    <a-form-item :name="['user','gender']"  label="Gender">
      <a-radio-group v-model:value="formState.gender">
        <a-radio value="M">Male</a-radio>
        <a-radio value="F">Female</a-radio>
      </a-radio-group>
    </a-form-item>
      <a-form-item :wrapper-col="{ ...layout.wrapperCol, offset: 8 }">
        <a-button type="primary" html-type="submit">Submit</a-button>
      </a-form-item>
    </a-form>
  </template>
  <script>
  import { defineComponent, reactive } from 'vue';
  export default defineComponent({
    setup() {
      const layout = {
        labelCol: {
          span: 8,
        },
        wrapperCol: {
          span: 16,
        },
      };
      const validateMessages = {
        required: '${label} is required!',
        types: {
          email: '${label} is not a valid email!',
          number: '${label} is not a valid number!',
        },
        number: {
          range: '${label} must be between ${min} and ${max}',
        },
      };
      const formState = reactive({
        user: {
          name: '',
          age: undefined,
          email: '',
          website: '',
          introduction: '',
        },
      });
      const onFinish = values => {
        console.log('Success:', values);
      };
      return {
        formState,
        onFinish,
        layout,
        validateMessages,
      };
    },
  });
  </script>