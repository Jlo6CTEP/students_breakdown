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
    <div
      class="survey"
      v-for="survey in surveys">
      <Survey v-bind:course="survey.course"
              v-bind:due_date="survey.due_date"
              v-bind:is_formed="survey.is_formed"
              v-bind:name="survey.name"/>
    </div>
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
        .get(`${config.apiUrl}/user/surveys`)
        .then(response => {
          this.surveys = response
        })
        .catch(error => {
          console.log(error);
          this.surveys = [
            {name: "Group project", course: "SWP", due_date: "2019-05-18", is_formed: false},
            {name: "Assigment II", course: "AI", due_date: "2019-03-18", is_formed: false},
            {name: "Assigment I", course: "AI", due_date: "2019-03-18", is_formed: true},
          ];
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
