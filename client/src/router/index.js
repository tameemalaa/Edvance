import { createRouter, createWebHistory } from "vue-router";
const routes = [
    {
        path: "/",
        name: "home",
        component: () => import("../views/HomeView.vue"),
    },
    {
        path: "/dashboard",
        name: "dashboard",
        component: () => import("../views/DashBoard.vue"),
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
        path: "/password/reset/confirm",
        name: "ResetPassword",
        component: () => import("../views/ResetPassword.vue"),
        props: (route) => ({token: route.query.token, uid: route.query.uid}),
    },
    {
        path: "/activate",
        name: "ActivationView",
        component: () => import("../views/ActivationView.vue"),
        props: (route) => ({token: route.query.token, uid: route.query.uid}),
    },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

export default router;
