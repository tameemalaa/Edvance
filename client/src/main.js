import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import Antd from "ant-design-vue";
import "ant-design-vue/dist/antd.css";
import VueCookies from 'vue-cookies';

import axios from "axios";
axios.defaults.baseURL = "http://localhost:8000";

const app = createApp(App);
app.use(Antd);
app.use(router);
app.use(store);
app.use(VueCookies);
app.config.globalProperties.$axios = axios;
app.mount("#app");