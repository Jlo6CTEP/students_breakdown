<template>
    <div>
        <div slot="top-right">
            <button @click="$modal.hide('foo')" class="btn btn-done btn-group-sm">
                ❌
            </button>
        </div>
        <div class="card-body custom">
            <div class="window-header" slot="left">
                <img alt="" class="mb-4" src="../assets/drag_icon_633892.png" width="20px">
            </div>
            <h4 class="card-title"><strong>{{project_name}}</strong></h4>
            <p class="card-text">Course: {{course}}</p>
            <p class="card-text ">Description: {{description}}</p>
            <div class="row choose-project" v-if="!is_formed">
                <div class="form-group col-md-4">
                    <label for="inputState1">Project 1</label>
                    <select class="form-control" id="inputState1">
                        <option disabled selected>Choose...</option>
                        <option>Timetable creation</option>
                        <option>Students breakdown</option>
                        <option>Renting System</option>
                        <option>Startup</option>
                        <option>Leave the university</option>
                    </select>
                </div>
                <div class="form-group col-md-4">
                    <label for="inputState2">Project 2</label>
                    <select class="form-control" id="inputState2">
                        <option disabled selected>Choose...</option>
                        <option>Timetable creation</option>
                        <option>Students breakdown</option>
                        <option>Renting System</option>
                        <option>Startup</option>
                        <option>Leave the university</option>
                    </select>
                </div>
                <div class="form-group col-md-4">
                    <label for="inputState3">Project 3</label>
                    <select class="form-control" id="inputState3">
                        <option disabled selected>Choose...</option>
                        <option>Timetable creation</option>
                        <option>Students breakdown</option>
                        <option>Renting System</option>
                        <option>Startup</option>
                        <option>Leave the university</option>
                    </select>
                </div>

            </div>
            <div class="col-lg-9" v-else>
                <div class="team">
                    <h5 class="card-title"><strong>For {{project_name}} project</strong></h5>
                    <h5 class="card-title">You and your perfect team will work on student breakdown topic</h5>
                    <ul>
                        <li>Ruslan Sabirov</li>
                        <li>Elena Lukyanchikova</li>
                        <li>Yuriy Sukhorukov</li>
                        <li>Natalia Tupikina</li>
                    </ul>
                </div>
            </div>
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <button @click="$emit('close')" class="btn btn-primary survey-button open"
                            v-if="!is_closed && !is_formed">Save
                    </button>
                    <button @click="$emit('close')" class="btn btn-primary survey-button">Cancel</button>
                </div>
                <small class="text-muted">Due: {{due_date_format}}</small>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "ModalWindow",
        props: {
            course: {
                type: String,
                required:
                    true
            },
            project_name: {
                type: String,
                required:
                    true
            },
            description: {
                type: String,
                // default: 'lol'
                default:
                    'This is a description for survey with supporting text below as a natural lead-in to additional content. This content is a little bit longer'
            },
            due_date_format: {
                type: String,
                required:
                    true,
                validator:
                    due_date => {
                        return due_date instanceof Date && !isNaN(due_date);
                    }
            },
            is_formed: {
                type: Boolean,
                default:
                    false
            },
            is_closed: {
                type: Boolean,
                default:
                    false
            },
        },
    }
</script>

<style scoped>
    .custom {
        align-content: center;
        text-align: center;
    }

    .survey-button {
    }

    .row {
        display: inline-flex;
    }

    .team {
        text-align: left;
    }

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
