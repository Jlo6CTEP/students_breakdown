<template>
    <div>
        <h1>Hi {{account.user.firstName}}!</h1>
        <p>Surname: {{account.user.lastName}}</p>
        <p>Email: {{account.user.username}}</p>
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