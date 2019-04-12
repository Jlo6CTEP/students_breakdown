import Vue from 'vue'
import Router from 'vue-router'
import Home from "../components/Main";
import LoginPage from "../components/LoginPage";
import RegisterPage from "../components/RegisterPage";

Vue.use(Router)

export const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: LoginPage
    }, {
      path: '/register',
      name: 'Register',
      component: RegisterPage
    }, {
      path: '/',
      name: 'Home',
      component: Home
    },

    // otherwise redirect to home
    {
      path: '*',
      redirect: Home
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
