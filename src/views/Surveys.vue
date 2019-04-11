<template>
    <div class="main">
        <h1 class="title">Surveys</h1>
        <button @click="toggleFeatures" class="toggle-features btn btn-primary btn-sm" type="button">{{ featuresOpen ?
            'Hide Features' : 'ViewFeatures'}}
        </button>

        <div :key="survey.survey_id" class="survey" v-for="survey in surveys">
            <ul><p> Name: {{survey.name}} </p></ul>
            <ul><p> Due date: {{survey.due_date}} </p></ul>
            <ul><p> Status: {{survey.status}} </p></ul>
            <ul class="features" v-show-slide="featuresOpen">
                <p>memento mori</p>
            </ul>
        </div>

        <br>
        <br>
        <br>
        <br>
        <br>
        <br>

        <div class="Wrap" id="app">
            <h1>Accordion</h1>
            <div :key="survey.survey_id" class="Accordion survey" v-for="survey in surveys">
                <Expander :fuction="getOpenInformation" :info="openInfo" animation="bottomToTop"
                          title=getOpenInformation()>
                    <ul><p> Name: {{survey.name}} </p></ul>
                    <ul><p> Due date: {{survey.due_date}} </p></ul>
                    <ul><p> Status: {{survey.status}} </p></ul>
                </Expander>
            </div>
        </div>

        <div class="[add-survey, survey]" v-if="account.user.role === 'TA'">
            <router-link to="/createSurvey">Create new survey</router-link>
        </div>
    </div>
</template>

<script>
    import {mapState} from "vuex";
    import Expander from "../components/Expander";

    var surveys;
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
            openInfo: {
                name: "surveys[0].name",
                due_date: "surveys[0].due_date",
            }
        }),
        methods: {
            toggleFeatures() {
                this.featuresOpen = !this.featuresOpen
            },
            getOpenInformation() {
                return "hhhhh";
            }
        },
        components: {
            Expander: Expander,
        }

    }

</script>
<style>
    .survey {
        box-sizing: border-box;
        padding: 10px;
        height: 100%;
        position: relative;
        display: flex;
        margin: 10px;
        align-items: center;
        float: left;
    }

    .survey:hover {
        box-sizing: border-box;
        background-color: aquamarine;
    }
</style>
