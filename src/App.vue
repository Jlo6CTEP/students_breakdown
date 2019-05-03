<template>
    <div id="app"> <!--:class="{'nav-open': $sidebar.showSidebar}">-->
        <div :class="`alert ${alert.type}`" v-if="alert.message">{{alert.message}}</div>
        <notification/>
        <router-view/>
    </div>
</template>

<script>
    import {mapActions, mapState} from 'vuex'
    import Notification from "./components/notifications/Notification";

    export default {
        name: 'App',
        components: {Notification},
        computed: {
            ...mapState({
                alert: state => state.alert
            }),
        },
        methods: {
            ...mapActions({
                clearAlert: 'alert/clear'
            })
        },
        watch: {
            $route(to, from) {
                // clear alert on location change
                this.clearAlert();
            }
        },
    }
</script>

<style>
    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        color: #2c3e50;
    }
</style>
