<template>
  <div class="card" style="width: 18rem;">
    <div class="card-body">
      <h5 class="card-title">{{name}}</h5>
      <p class="card-text">{{course}}</p>
      <p class="card-text">{{due_date}}</p>
      <a class="btn btn-primary formed" href="#" v-if="is_formed">Formed</a>
      <a class="btn btn-primary closed" href="#" v-else-if="is_closed(due_date)">Closed</a>
      <a class="btn btn-primary open" href="#" v-else>Fill</a>
    </div>
  </div>
</template>

<script>
  export default {
    name: "Survey",
    props: {
      course: {
        type: String,
        required: true
      },
      name: {
        type: String,
        required: true
      },
      due_date: {
        type: String,
        required: true,
        validator: function (due_date) {
          try {
            new Date(due_date);
            return true;
          } catch (e) {
            return false;
          }
        }
      },
      is_formed: {
        type: Boolean,
        default: false
      },
    },
    methods: {
      is_closed(due_date) {
        let current_date = new Date();
        console.log(new Date(due_date));
        console.log(new Date());

        return (new Date(due_date) <= current_date);
      }
    }
  }
</script>

<style scoped>
  .formed {
    background-color: cornflowerblue;
    border-color: cornflowerblue;
  }

  .closed {
    background-color: crimson;
    border-color: crimson;
  }

  .open {
    background-color: #42b983;
    border-color: #42b983;
  }
</style>

