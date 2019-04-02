<template>
    <div>
        <h2>Name {{account.user.firstName}}</h2>
        <h2>Surname: {{account.user.lastName}}</h2>
        <h2>Email: {{account.user.username}}</h2>
        <p>
            <router-link to="/login">Logout</router-link>
        </p>
    </div>
</template>

<script>
    import {mapActions, mapState} from 'vuex'

    export default {
        computed: {
            ...mapState({
                account: state => state.account,
                users: state => state.users.all
            })
        },
        created() {
            this.getAllUsers();
        },
        methods: {
            ...mapActions('users', {
                getAllUsers: 'getAll',
                deleteUser: 'delete'
            })
        }
    };
</script>