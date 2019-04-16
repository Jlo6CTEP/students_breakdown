<template>
  <div class="survey">
    <div class="card box-shadow">
      <!--      <img class="card-img-top"-->
      <!--           data-src="holder.js/100px225?theme=thumb&amp;bg=55595c&amp;fg=eceeef&amp;text=Thumbnail"-->
      <!--           alt="Thumbnail [100%x225]" style="height: 225px; width: 100%; display: block;"-->
      <!--           src="data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22348%22%20height%3D%22225%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%20348%20225%22%20preserveAspectRatio%3D%22none%22%3E%3Cdefs%3E%3Cstyle%20type%3D%22text%2Fcss%22%3E%23holder_16a2315e0ef%20text%20%7B%20fill%3A%23eceeef%3Bfont-weight%3Abold%3Bfont-family%3AArial%2C%20Helvetica%2C%20Open%20Sans%2C%20sans-serif%2C%20monospace%3Bfont-size%3A17pt%20%7D%20%3C%2Fstyle%3E%3C%2Fdefs%3E%3Cg%20id%3D%22holder_16a2315e0ef%22%3E%3Crect%20width%3D%22348%22%20height%3D%22225%22%20fill%3D%22%2355595c%22%3E%3C%2Frect%3E%3Cg%3E%3Ctext%20x%3D%22116.5%22%20y%3D%22120.3%22%3EThumbnail%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fsvg%3E"-->
      <!--           data-holder-rendered="true">-->
      <div class="card-body">
        <h4 class="card-title"><strong>{{name}}</strong></h4>
        <p class="card-text">Course: {{course}}</p>
        <p class="card-text">This is a description for survey with supporting text below as a natural lead-in to
          additional content. This content is a little bit longer.</p>
        <div class="d-flex justify-content-between align-items-center">
          <div class="btn-group">
            <button class="btn btn-sm btn-primary formed" type="button" v-if="is_formed">Formed</button>
            <button class="btn btn-sm btn-primary closed" type="button" v-else-if="is_closed(due_date)">Closed</button>
            <button class="btn btn-sm btn-primary open" type="button" v-else>Fill now</button>
          </div>
          <small class="text-muted">Due: {{due_date_format}}</small>
        </div>
      </div>
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
        validator: due_date => {
          return due_date instanceof Date && !isNaN(due_date);
        }
      },
      is_formed: {
        type: Boolean,
        default: false
      },
    },
    computed: {
      due_date_format() {
        let convert_date = new Date(this.due_date);
        return convert_date.getDate() + '-' + convert_date.getMonth() + '-' + convert_date.getFullYear();
      }
    },
    methods: {
      is_closed(due_date) {
        let current_date = new Date();
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

  .survey {
    display: flex;
    margin: 20px;
  }
</style>

