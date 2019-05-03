<template>
    <div class="wrapper d-flex align-items-lg-start">
        <div class="sidebar col-lg-2">
            <Slide isOpen>
                <nav class="navbar navbar-light">
                    <router-link id="student-surveys" to="/student/surveys">
                    <span class="btn btn-lg btn-outline-light col-lg-10">
                        <font-awesome-icon icon="dice"/>
                        My Surveys
                    </span>
                    </router-link>
                </nav>
                <nav class="navbar navbar-light">
                    <router-link id="student-teams" to="/student/teams">
                    <span class="btn btn-lg btn-outline-light col-lg-10">
                        <font-awesome-icon icon="users"/>
                        My Teams
                    </span>
                    </router-link>
                </nav>
                <nav class="navbar navbar-light">
                    <router-link id="student-account" to="/student/account">
                    <span class="btn btn-lg btn-outline-light col-lg-10">
                        <font-awesome-icon icon="user-circle"/>
                        My Profile
                    </span>
                    </router-link>
                </nav>
                <nav class="navbar navbar-light">
                    <router-link id="student-charts" to="/student/charts">
                    <span class="btn btn-lg btn-outline-light col-lg-10">
                        <font-awesome-icon icon="chart-line"/>
                        Statistic
                    </span>
                    </router-link>
                </nav>
            </Slide>
        </div>
        <div class="main-panel col-lg-8">
            <top-navbar/>

            <dashboard-content/>

            <content-footer/>
        </div>
    </div>
</template>
<style>

</style>
<script>
    import {Slide} from 'vue-burger-menu'
    import TopNavbar from './TopNavbar.vue'
    import ContentFooter from './ContentFooter.vue'
    import DashboardContent from './Content.vue'

    export default {
        name: 'DashboardStudent',
        data() {
            return {}
        },
        components: {
            Slide,
            TopNavbar,
            ContentFooter,
            DashboardContent,
        },
        methods: {}
    }

</script>
