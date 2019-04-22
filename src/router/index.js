import Vue from 'vue'
import Router from 'vue-router'
import Main from "../components/Main";
import LoginPage from "../components/LoginPage";
import RegisterPage from "../components/RegisterPage";
import Account from "../components/Account";
import News from "../components/News";
import NotFound from "../components/NotFound";

Vue.use(Router)

export const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: LoginPage
    },
    {
      path: '/api-auth/login',
      name: 'Login',
      component: LoginPage
    },
    {
      path: '/register',
      name: 'Register',
      component: RegisterPage
    }, /*{
      path: '/account',
      name: 'Account',
      component: Account
    },*/
    {
      path: '/accounts/profile/',
      name: 'Account',
      component: Account
    },
    {
      path: '/news',
      name: 'News',
      component: News
    },
    {
      path: '/',
      name: 'Main',
      component: Main
    },

    // otherwise redirect to not found page
    {
      path: '*',
      component: NotFound
    }
  ]
});

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
