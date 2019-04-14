<template>
  <div id="content-main">
    <section v-if="errored">
      <p>We're sorry, we're not able to retrieve this information at the moment, please try back later</p>
    </section>

    <section v-else>
      <div v-if="loading">Loading...</div>
      <div
        class="survey"
        v-else
        v-for="survey in surveys">
        <Survey v-bind:course="survey.course"
                v-bind:due_date="survey.due_date"
                v-bind:is_formed="survey.is_formed"
                v-bind:name="survey.name"/>
      </div>
    </section>
  </div>
</template>

<script>
  import Survey from './Survey';
  import axios from "axios";
  import config from 'config';

  export default {
    name: 'Main',
    data() {
      return {
        surveys: null,
        loading: true,
        errored: false,
      }
    },
    mounted() {
      axios
        .get(`http://127.0.0.1:8000/user/surveys`)
        .then(response => {
          console.log(response.data.data);
          this.surveys = response.data.data;
        })
        .catch(error => {
          console.log(error);

          this.errored = true;
        })
        .finally(() => {
          this.loading = false;
        })
    },
    components: {
      Survey
    }
  }
</script>

<style scoped>

</style>
