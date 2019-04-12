<template>
  <div id="content-main">
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

  export default {
    name: 'Main',
    data() {
      return {
        surveys: [
          {name: "Group project", course: "SWP", due_date: "2019-05-18", is_formed: false},
          {name: "Assigment II", course: "AI", due_date: "2019-03-18", is_formed: false},
          {name: "Assigment I", course: "AI", due_date: "2019-03-18", is_formed: true},
        ],
        loading: true,
        errored: false,
      }
    },
    // mounted: {
    // surveys: () => {
    //   return [
    //     {name: "Group project", course: "SWP", due_date: "12.05.18", is_formed: false},
    //     {name: "Assigment II", course: "AI", due_date: "12.03.18", is_formed: false},
    //     {name: "Assigment I", course: "AI", due_date: "12.03.18", is_formed: true},
    //   ];
    // }
    // },
    components: {
      Survey
    }
  }
</script>

<style scoped>

</style>
