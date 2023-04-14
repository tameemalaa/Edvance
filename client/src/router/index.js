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
        path: "/forgotpassword",
        name: "ForgotPassword",
        component: () => import("../views/ForgotPassword.vue"),
    },
    {
        path: "/resetpassword",
        name: "ResetPassword",
        component: () => import("../views/ResetPassword.vue"),
        props: (route) => ({token: route.query.token}),
    },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

export default router;
