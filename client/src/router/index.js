import { createRouter, createWebHistory } from "vue-router";
const routes = [
    {
        path: "/",
        name: "home",
        component: () => import("../views/HomeView.vue"),
    },
    {
        path: "/login",
        name: "LogIn",
        component: () => import("../views/LogIn.vue"),
    },
    {
        path: "/signup",
        name: "Signup",
        component: () => import("../views/SignUp.vue"),
    },
    {
        path: "/forgot-password",
        name: "ForgotPassword",
        component: () => import("../views/ForgotPassword.vue"),
    },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

export default router;
