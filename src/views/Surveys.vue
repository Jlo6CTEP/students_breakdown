<template>
    <div class="main">
        <h1 class="title">Surveys</h1>
        <div class="survey" key="survey_id" v-for="survey in surveys">
            <p> Name: {{survey.name}}</p>
            <p> Due date: {{survey.due_date}}</p>
            <p> Status: {{survey.status}}</p>
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
                name: "sur1", due_date: "15.02.2020", status: 'open',
            }, {
                name: "sur2", due_date: "16.03.2019", status: 'close',
            }, {
                name: "sur3", due_date: "17.04.2021", status: 'open',
            }, {
                name: "sur4", due_date: "18.05.2022", status: 'open',
            }, {
                name: "sur5", due_date: "19.06.2023", status: 'open',
            },]
        }),
        created() {
            // let m = this.$modals.add({
            //     title: 'Title',
            //     theme: 'osx', // || mojave
            //     items: [
            //         {
            //             label: 'Username',
            //             name: 'username',
            //             type: 'text',
            //             value: 'Daniel',
            //         },
            //         {
            //             label: 'Bio',
            //             name: 'bio',
            //             type: 'textarea',
            //             value: 'web developer',
            //         }
            //     ],
            // });
            // m.open();
            //
            // m.onsave( (m) => {
            //     m.loading();
            //     setTimeout(() => {
            //         console.log(m.formData());
            //         console.log(m.getItems());
            //         m.loaded();
            //     },500)
            // });
            //
            // m.onreload( () => {
            //     console.log('Reloaded')
            // })
        }
    }
</script>
<style>
    .survey {
        padding: 10px;
        margin: 10px;
        width: 200px;
        height: 150px;
        position: relative;
        display: inline;
        float: left;
        border: black;
        box-sizing: border-box;
    }

    .survey:hover {
        background-color: aquamarine;
    }
</style>