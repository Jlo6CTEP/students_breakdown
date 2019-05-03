import Vue from 'vue'
import {store} from "../_store";
import Router from 'vue-router'

import Login from "../pages/Login";
import Register from "../pages/Register";

import WrongPermission from "../pages/WrongPermission";
import NotFound from "../pages/NotFound";

import DashboardAdmin from "../layout/DashboardAdmin";
import DashboardTa from "../layout/DashboardTa";
import DashboardStudent from "../layout/DashboardStudent";

import AdminOverview from "../pages/admin/AdminOverview";
import AdminAccount from "../pages/admin/AdminAccount";
import AdminTasks from "../pages/admin/AdminTasks";
import AdminCharts from "../pages/admin/AdminCharts";

import TaSurveys from "../pages/ta/TaSurveys";
import TaTeamManagement from "../pages/ta/TaTeamManagement";
import TaAccount from "../pages/ta/TaAccount";
import TaCreateSurvey from "../pages/ta/TaCreateSurvey";
import TaCharts from "../pages/ta/TaCharts";

import StudentSurveys from "../pages/student/StudentSurveys";
import StudentTeams from "../pages/student/StudentTeams";
import StudentAccount from "../pages/student/StudentAccount";
import StudentCharts from "../pages/student/StudentCharts";

Vue.use(Router);

export const router = new Router({
    mode: 'history',
    routes: [
        {
            path: '/login',
            name: 'Login',
            component: Login
        }, {
            path: '/register',
            name: 'Register',
            component: Register
        }, {
            path: '/admin',
            name: 'AdminDashBoard',
            redirect: '/admin/overview',
            component: DashboardAdmin,
            children: [
                {
                    path: 'overview',
                    name: 'AdminOverview',
                    component: AdminOverview
                }, {
                    path: 'account',
                    name: 'AdminAccount',
                    component: AdminAccount
                }, {
                    path: 'tasks',
                    name: 'AdminTasks',
                    component: AdminTasks
                }, {
                    path: 'charts',
                    name: 'AdminCharts',
                    component: AdminCharts
                }

            ]
        }, {
            path: '/ta',
            name: 'TaDashboard',
            redirect: '/ta/surveys',
            component: DashboardTa,
            children: [
                {
                    path: 'surveys',
                    name: 'TaSurveys',
                    component: TaSurveys
                }, {
                    path: 'teams',
                    name: 'TeacherTeamManagement',
                    component: TaTeamManagement
                }, {
                    path: 'account',
                    name: 'TeacherAccount',
                    component: TaAccount
                }, {
                    path: 'create',
                    name: 'CreateSurvey',
                    component: TaCreateSurvey
                }, {
                    path: 'charts',
                    name: 'TeacherCharts',
                    component: TaCharts
                }
            ]
        }, {
            path: '/student',
            name: 'StudentDashboard',
            redirect: '/student/surveys',
            component: DashboardStudent,
            children: [
                {
                    path: 'surveys',
                    name: 'StudentSurveys',
                    component: StudentSurveys
                }, {
                    path: 'teams',
                    name: 'StudentTeams',
                    component: StudentTeams
                }, {
                    path: 'account',
                    name: 'StudentAccount',
                    component: StudentAccount
                }, {
                    path: 'charts',
                    name: 'StudentCharts',
                    component: StudentCharts
                }
            ]
        }, {
            path: '/permission-restriction',
            name: 'WrongPermission',
            component: WrongPermission
        }, {
            path: '*',
            component: NotFound
        }
    ]
});

router.beforeEach((to, from, next) => {
    // redirect to login page if not logged in and trying to access a restricted page
    const publicPages = ['/login', '/register'];
    const isAdminPage = to.path.startsWith('/admin');
    const isTeacherPage = to.path.startsWith('/teacher');
    const isStudentPage = to.path.startsWith('/student');
    const authRequired = !publicPages.includes(to.path);
    const loggedIn = localStorage.getItem('user');
    const status = store.getters["account/getStatus"];
    const wrongPermission = isAdminPage && status !== 'admin' || isTeacherPage && status !== 'ta'
        || isStudentPage && status !== 'student';

    if (authRequired && !loggedIn) {
        return next('/login');
    } else if (wrongPermission) {
        console.log('Permission restriction to access to page' + to.path + 'for user with status ' + status);
        return next('/permission-restriction');
    }

    next();
});
