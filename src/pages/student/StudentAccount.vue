<template>
    <div class="content">
        <div class="container-fluid">
            <div class="row">
                <div class="col-md-8">
                    <student-account-edit/>
                </div>
                <div class="col-md-4">
                    <Card class="card-user">
                        <div class="author">
                            <a href="#">
                                <h4 class="title">{{account.user.firstName}} {{account.user.lastName}}<br/>
                                    <small>{{account.user.username}}</small>
                                </h4>
                            </a>
                        </div>
                        <p class="description text-center">Academic group: {{account.user.group}}</p>
                        <p class="description text-center"> Lamborghini Messy <br>
                            Your chick she so thirsty <br>
                            I'm in that two seat Lambo"
                        </p>
                        <div class="text-center d-flex justify-content-center" slot="footer">
                        </div>
                    </Card>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import StudentAccountEdit from './StudentAccountEdit';
    import Card from '../../components/cards/Card';
    import {mapState} from "vuex";

    export default {
        name: "StudentAccount",
        components: {
            Card,
            StudentAccountEdit
        },
        data() {
            return {
                details: [
                    {
                        title: '12',
                        subTitle: 'Files'
                    },
                    {
                        title: '2GB',
                        subTitle: 'Used'
                    },
                    {
                        title: '24,6$',
                        subTitle: 'Spent'
                    }
                ]
            }
        },
        computed: {
            ...mapState({
                account: state => state.account,
            })
        },
        methods: {
            getClasses(index) {
                let remainder = index % 3;
                if (remainder === 0) {
                    return 'col-md-3 col-md-offset-1'
                } else if (remainder === 2) {
                    return 'col-md-4'
                } else {
                    return 'col-md-3'
                }
            }
        }
    }
</script>

<style scoped>

</style>
