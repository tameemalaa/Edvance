import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";


import Antd from "ant-design-vue";
import "ant-design-vue/dist/antd.css";
import VueCookies from 'vue-cookies';

import axios from "axios";
axios.defaults.baseURL = "http://localhost:8000";

createApp(App).use(Antd).use(router,axios).use(store).use(VueCookies).mount("#app");

