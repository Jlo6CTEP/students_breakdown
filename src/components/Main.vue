<template>
    <div id="content-main">
        <div class="album py-5 bg-light">
            <div class="container">

                <div class="row">
                    <template v-if="errored">
                        <p>We're sorry, we're not able to retrieve this information at the moment, please try back
                            later</p>
                        <br>
                    </template>

                    <template v-else>
                        <template v-if="loading">
                            <h1>Loading...</h1>
                        </template>

                        <template v-else>
                            <label class="text-center query">
                                <input placeholder="Search" v-model="query">
                            </label>

                            <transition-group
                                class="survey_arr text-center"
                                name="staggered-fade"
                                tag="div"
                                v-bind:css="false"
                                v-on:before-enter="beforeEnter"
                                v-on:enter="enter"
                                v-on:leave="leave"
                            >
                                <div :key="get_key(survey, index)" class="col-md"
                                     v-for="(survey, index) in computedSurveys">
                                    <Survey
                                        v-bind:course="survey.course"
                                        v-bind:description="survey.description"
                                        v-bind:due_date="survey.due_date"
                                        v-bind:is_formed="survey.is_formed"
                                        v-bind:project_name="survey.project_name"/>
                                </div>
                            </transition-group>
                        </template>
                    </template>
                </div>
            </div>
        </div>
    </div>

</template>
<script>
    import Survey from './Survey';
    import axios from "axios";
    import Velocity from 'velocity-animate';

    export default {
        name: 'Main',
        data() {
            return {
                surveys: null,
                loading: true,
                errored: false,
                query: ''
            }
        },
        mounted() {
            axios
                .get(process.env.API_URL + '/user/surveys')
                .then(response => {
                    this.surveys = response.data.data;
                })
                .catch(error => {
                    console.log(error);
                    if (process.env.NODE_ENV !== 'production') {
                        this.surveys = [
                            {project_name: "ERROR", course: "ERROR", due_date: "2019-05-18", is_formed: false}
                        ];
                    } else {
                        this.errored = true;
                    }
                })
                .finally(() => {
                    this.loading = false;
                })
        },
        computed: {
            is_valid_date(due_date) {
                console.log("Date: " + due_date);
                if (due_date instanceof Date && !isNaN(due_date)) {
                    console.log("should be not valid" + due_date);
                }
                return due_date instanceof Date && !isNaN(due_date);
            },
            computedSurveys: function () {
                let vm = this;
                return this.surveys
                    .filter(function (item) {
                        let contain_in_name = item.project_name.toLowerCase().indexOf(vm.query.toLowerCase()) !== -1;
                        let contain_in_course = item.course.toLowerCase().indexOf(vm.query.toLowerCase()) !== -1;
                        return contain_in_name || contain_in_course;
                    })
                    .sort((a, b) => {
                        function date_compare(o1, o2) {
                            return new Date(o2) - o1 > 0;
                        }

                        let d_a = a.due_date;
                        let d_b = b.due_date;
                        let d = new Date();
                        return !date_compare(d_a, d) && date_compare(d_b, d) ? -1 : date_compare(d_a, d) && !date_compare(d_b, d) ? 1 : 0
                    })
                    .sort((a, b) => {
                        return new Date(b.due_date) - new Date(a.due_date);
                    })
                    .sort((a, b) => {
                        let n_a = a.project_name;
                        let n_b = b.project_name;
                        return n_a > n_b ? -1 : n_a < n_b ? 1 : 0
                    })
                    .sort((a, b) => {
                        let f_a = a.is_formed;
                        let f_b = b.is_formed;
                        return f_b && !f_a ? -1 : !f_b && f_a ? 1 : 0
                    })


            },
        },
        methods: {
            rank(is_formed, due_date) {
                return '' + (new Date(due_date))
            },
            get_key(survey, index) {
                return index;
            },
            beforeEnter: function (el) {
                el.style.opacity = 0;
                el.style.height = 0
            },
            enter: function (el, done) {
                let delay = el.dataset.index * 300;
                setTimeout(function () {
                    Velocity(
                        el,
                        {opacity: 1, height: '370px'},
                        {complete: done}
                    )
                }, delay)
            },
            leave: function (el, done) {
                let delay = el.dataset.index * 300;
                setTimeout(function () {
                    Velocity(
                        el,
                        {opacity: 0, height: 0},
                        {complete: done}
                    )
                }, delay)
            }
        },
        components: {
            Survey
        },
    }
</script>

<style scoped>
    section {
        display: flex;
    }

    .row .survey_arr {
        /*display: flex;*/
        /*flex-wrap: wrap;*/
        /*margin-right: auto;*/
        /*margin-left: auto;*/
        /*text-align: center;*/
    }

    .survey_arr {
        display: flex;
        flex-wrap: wrap;
        /*justify-content: space-between;*/
        align-content: space-between;
    }

    .query {
        margin-right: auto;
        margin-left: auto;
    }

    .text-center {
        text-align: center;
    }

</style>
