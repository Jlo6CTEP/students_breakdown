<template>
    <div>
        <h1>Hi dear user!</h1>
        <h2>You logged-in as {{account.user.firstName}} {{account.user.lastName}}</h2>
        <h2>Email: {{account.user.username}}</h2>
        <br>
        <label>
            <input @change="test_url" @onclick="test_url" @onload="test_url" autofocus min="1" type="number"
                   v-model="user_id">
        </label>
        <h3>{{user_info}}</h3>
        <!--    <h3>Users from secure api end point:</h3>-->
        <!--    <em v-if="users.loading">Loading users...</em>-->
        <!--    <span v-if="users.error" class="text-danger">ERROR: {{users.error}}</span>-->
        <!--    <ul v-if="users.items">-->
        <!--      <li v-for="user in users.items" :key="user.id">-->
        <!--        {{user.firstName + ' ' + user.lastName}}-->
        <!--        <span v-if="user.deleting"><em> - Deleting...</em></span>-->
        <!--        <span v-else-if="user.deleteError" class="text-danger"> - ERROR: {{user.deleteError}}</span>-->
        <!--        <span v-else> - <a @click="deleteUser(user.id)" class="text-danger">Delete</a></span>-->
        <!--      </li>-->
        <!--    </ul>-->
        <p>
            <router-link to="/login">Logout</router-link>
        </p>
    </div>
</template>

<script>
    import {mapActions, mapState} from 'vuex/types'
    import axios from "axios/index";

    export default {
        name: 'Account',
        data() {
            return {
                user_id: 1,
                user_info: null
            }
        },
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
            }),
            test_url() {
                axios
                    .get(`http://127.0.0.1:8000/users/${this.user_id}`)
                    .then(response => {
                        this.user_info = response.data
                    })
                    .catch(error => {
                        console.log(error);
                        this.user_info = {msg: `ERROR DURING LOADING USER INFO id: ${this.user_id}`}
                    })
                    .finally(() => {
                    })
            }
        }
    };
</script>
