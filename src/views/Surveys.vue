<template>
    <div class="main">
        <h1 class="title">Surveys</h1>
        <div :key="survey.survey_id" class="survey" v-for="survey in surveys">
            <p> Name: {{survey.name}}</p>
            <p> Due date: {{survey.due_date}}</p>
            <p> Status: {{survey.status}}</p>
            <ul class="features" v-show-slide="featuresOpen">
                <p>Aliquam lorem</p>
                <p>Praesent porttitor nulla vitae posuere</p>
                <p>Suspendisse nisl elit rhoncus</p>
            </ul>
            <button @click="toggleFeatures" class="toggle-features">{{ featuresOpen ? 'Hide Features' : 'View Features'
                }}
            </button>
        </div>
        <div class="[add-survey, survey]" v-if="account.user.role === 'TA'">
            <router-link to="/createSurvey">Create new survey</router-link>
        </div>
    </div>
</template>

<script>
    import {mapState} from "vuex";

    export default {
        name: 'home',
        computed: {
            ...mapState({
                account: state => state.account
            })
        },
        data: () => ({
            surveys: [{
                survey_id: 1, name: "sur1", due_date: "15.02.2020", status: 'open',
            }, {
                survey_id: 2, name: "sur2", due_date: "16.03.2019", status: 'close',
            }, {
                survey_id: 3, name: "sur3", due_date: "17.04.2021", status: 'open',
            }, {
                survey_id: 4, name: "sur4", due_date: "18.05.2022", status: 'open',
            }, {
                survey_id: 5, name: "sur5", due_date: "19.06.2023", status: 'open',
            },],
            featuresOpen: false,
        }),
        methods: {
            toggleFeatures() {
                this.featuresOpen = !this.featuresOpen
            }
        }
    }
</script>
<style>
    .survey {
        box-sizing: border-box;
        /*padding: 10px;*/
        height: 100%;
        /*position: relative;*/
        display: flex;
        margin: 0;
        align-items: center;
        /*float: left;*/
    }

    .survey:hover {
        box-sizing: border-box;
        background-color: aquamarine;
    }
</style>