<template>
  <div id="app">
    <template v-if="!is_login_page">
      <Header/>
    </template>

    <div class="jumbotron">
      <div class="container">
        <div :class="`alert ${alert.type}`" v-if="alert.message">{{alert.message}}</div>
        <router-view/>
      </div>
    </div>

    <template v-if="!is_login_page">
      <Footer/>
    </template>
  </div>
</template>

<script>
  import {mapActions, mapState} from 'vuex'
  import header from './components/Header'
  import footer from './components/Footer'

  export default {
    name: 'App',
    head: {
      meta: [
        {charset: 'UTF-8', undo: false}
      ],
      link: [
        {
          rel: 'stylesheet',
          href: 'http://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',
          id: 'bootstrap-css',
          undo: false
        },
      ],
    },
    computed: {
      ...mapState({
        alert: state => state.alert
      }),
      is_login_page() {
        return this.$route.path === '/login' || this.$route.path === '/register'
      }
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
    components: {
      Header: header,
      Footer: footer,
    }
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
