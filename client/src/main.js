import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

import Antd from "ant-design-vue";
import "ant-design-vue/dist/antd.css";

import axios from "axios";
axios.defaults.baseURL = "http://127.0.0.1:8000";

createApp(App).use(Antd).use(router,axios).mount("#app");

