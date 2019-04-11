<template>
    <div class="jumbotron">
        <div class="container">
            <Header/>
            <div class="row">
                <div class="col-sm-6 offset-sm-3">
                    <div :class="`alert ${alert.type}`" v-if="alert.message">{{alert.message}}</div>
                    <router-view/>
                </div>
            </div>
            <Footer/>
        </div>
    </div>
</template>

<script>
    import {mapActions, mapState} from 'vuex'
    import Header from "../components/Header";
    import Footer from "../components/Footer";


    export default {
        name: 'app',
        computed: {
            ...mapState({
                alert: state => state.alert
            })
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
        }, components: {
            Header,
            Footer
        }

    };
</script>
