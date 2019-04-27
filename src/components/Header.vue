<template>
  <div class="header">
    <transition name="annotation">
      <div class="bg-dark" id="navbarHeader" v-if="!is_hidden">
        <div class="container">
          <div class="row">
            <div class="col-sm-8 col-md-7 py-4">
              <h4 class="text-white">About</h4>
              <p class="text-muted">
                It is our great web application for helping TAs and students to choose perfect project
                by their preferences. We hope you will enjoy</p>
            </div>
            <div class="col-sm-4 offset-md-1 py-4">
              <h4 class="text-white">Contact</h4>
              <ul class="list-unstyled">
                <li>
                  <a class="text-white" href="http://t.me/HardLight" target="_blank">Frontend-designer</a>
                </li>
                <li>
                  <a class="text-white" href="http://t.me/realnigger" target="_blank">Backend-designer</a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </transition>
    <div class="navbar navbar-dark bg-dark box-shadow">
      <div class="container d-flex justify-content-between">
        <ul class="nav nav-pills float-right">
          <li class="nav-item">
            <router-link active-class="active" class="nav-link" exact to="/"><strong>Home</strong></router-link>
          </li>
          <li class="nav-item">
            <router-link active-class="active" class="nav-link" to="/account"><strong>Account</strong></router-link>
          </li>
          <li class="nav-item">
            <router-link active-class="active" class="nav-link disabled" to="/news"><strong>News</strong></router-link>
          </li>
        </ul>
        <button @click="is_hidden=!is_hidden" aria-controls="navbarHeader" aria-expanded="false"
                aria-label="Toggle navigation"
                class="navbar-toggler" data-target="#navbarHeader" data-toggle="collapse"
                type="button">
          <span class="navbar-toggler-icon"></span>
        </button>
      </div>
    </div>
    <!--    <nav>-->
    <!--      <ul class="nav nav-pills float-right">-->
    <!--        <li class="nav-item">-->
    <!--          <router-link to="/" exact class="nav-link" active-class="active">Home</router-link>-->
    <!--        </li>-->
    <!--        <li class="nav-item">-->
    <!--          <router-link to="/account" class="nav-link" active-class="active">Account</router-link>-->
    <!--        </li>-->
    <!--        <li class="nav-item">-->
    <!--          <router-link to="/news" class="nav-link" active-class="active">News</router-link>-->
    <!--        </li>-->
    <!--      </ul>-->
    <!--    </nav>-->
    <!--    <h3 class="text-muted">Our fancy project</h3>-->
  </div>
</template>

<script>
  export default {
    name: "Header",
    data() {
      return {
        is_hidden: true
      }
    }
  }
</script>

<style scoped>
  .header {
    display: inline;
  }

  .nav-item {
    color: lavender;

  }

  .annotation-enter-active {
    animation: annotation-in .5s;
  }

  .annotation-leave-active {
    animation: annotation-in .5s reverse;
  }

  @keyframes annotation-in {
    0% {
      opacity: 0;
    }
    100% {
      opacity: 100;
    }
  }
</style>
