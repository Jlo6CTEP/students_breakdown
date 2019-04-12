<template>
  <div id="app">
    <div class="jumbotron">
      <div class="container">
        <div class="row">
          <div class="col-sm-6 offset-sm-3">
            <div :class="`alert ${alert.type}`" v-if="alert.message">{{alert.message}}</div>
            <router-view/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import {mapActions, mapState} from 'vuex'

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
      is_hidden() {
        return this.$route.path !== '/login' && this.$route.path !== '/register'
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
  }
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
