import Vue from 'vue';
import Router from 'vue-router';

import HomePage from '../home/HomePage'
import LoginPage from '../login/LoginPage'
import RegisterPage from '../register/RegisterPage'
import SurveyCreationPage from "../surveyCreation/SurveyCreationPage";
import CheckPage from "../surveyCreation/CheckPage";

import Contact from '../views/Contact'

Vue.use(Router);

export const router = new Router({
        mode: 'history',
        routes: [{
            path: '/',
            name: 'default',
            component: HomePage
        }, {
            path: '/login',
            name: 'login',
            component: LoginPage
        }, {
            path: '/register',
            name: 'register',
            component: RegisterPage
        }, {
            path: '/contact',
            name: 'contact',
            component: Contact
        }, {
            path: '/account',
            name: 'account',
            component: () =>
                import("../views/Account.vue")
        }, {
            path: "/surveys",
            name: "surveys",
            component: () =>
                import("../views/Surveys.vue")
        },{
            path: '/create_survey',
            component: SurveyCreationPage
        }, {
            path: '/check',
            component: CheckPage
        }, {
            path: '*',
            redirect: '/'
        }
        ]
    })
;

router.beforeEach((to, from, next) => {
    // redirect to login page if not logged in and trying to access a restricted page
    const publicPages = ['/login', '/register'];
    const authRequired = !publicPages.includes(to.path);
    const loggedIn = localStorage.getItem('user');

    if (authRequired && !loggedIn) {
        return next('/login');
    }

    next();
});