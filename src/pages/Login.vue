<template>
    <div class="text-center" data-gr-c-s-loaded="true">
        <form @submit.prevent="handleSubmit" class="form-signin">
            <img alt="" class="mb-4" height="72" src="../assets/owl.svg"
                 width="72">
            <div class="form-group">
                <label for="username">Email</label>
                <input :class="{ 'is-invalid': submitted && !username }" autofocus="" class="form-control"
                       name="username"
                       placeholder="Email address" type="text" v-model="username"/>
                <div class="invalid-feedback" v-show="submitted && !username">Username is required</div>
            </div>
            <div class="form-group">
                <label htmlFor="password">Password</label>
                <input :class="{ 'is-invalid': submitted && !password }" class="form-control" name="password"
                       placeholder="Password"
                       type="password" v-model="password"/>
                <div class="invalid-feedback" v-show="submitted && !password">Password is required</div>
            </div>
            <div class="checkbox mb-3">
                <label>
                    <input type="checkbox" value="remember-me"> Remember me
                </label>
            </div>

            <div class="form-group">
                <button :disabled="auth.loggingIn" class="btn btn-primary">Login</button>
                <img
                    src="data:image/gif;base64,R0lGODlhEAAQAPIAAP///wAAAMLCwkJCQgAAAGJiYoKCgpKSkiH/C05FVFNDQVBFMi4wAwEAAAAh/hpDcmVhdGVkIHdpdGggYWpheGxvYWQuaW5mbwAh+QQJCgAAACwAAAAAEAAQAAADMwi63P4wyklrE2MIOggZnAdOmGYJRbExwroUmcG2LmDEwnHQLVsYOd2mBzkYDAdKa+dIAAAh+QQJCgAAACwAAAAAEAAQAAADNAi63P5OjCEgG4QMu7DmikRxQlFUYDEZIGBMRVsaqHwctXXf7WEYB4Ag1xjihkMZsiUkKhIAIfkECQoAAAAsAAAAABAAEAAAAzYIujIjK8pByJDMlFYvBoVjHA70GU7xSUJhmKtwHPAKzLO9HMaoKwJZ7Rf8AYPDDzKpZBqfvwQAIfkECQoAAAAsAAAAABAAEAAAAzMIumIlK8oyhpHsnFZfhYumCYUhDAQxRIdhHBGqRoKw0R8DYlJd8z0fMDgsGo/IpHI5TAAAIfkECQoAAAAsAAAAABAAEAAAAzIIunInK0rnZBTwGPNMgQwmdsNgXGJUlIWEuR5oWUIpz8pAEAMe6TwfwyYsGo/IpFKSAAAh+QQJCgAAACwAAAAAEAAQAAADMwi6IMKQORfjdOe82p4wGccc4CEuQradylesojEMBgsUc2G7sDX3lQGBMLAJibufbSlKAAAh+QQJCgAAACwAAAAAEAAQAAADMgi63P7wCRHZnFVdmgHu2nFwlWCI3WGc3TSWhUFGxTAUkGCbtgENBMJAEJsxgMLWzpEAACH5BAkKAAAALAAAAAAQABAAAAMyCLrc/jDKSatlQtScKdceCAjDII7HcQ4EMTCpyrCuUBjCYRgHVtqlAiB1YhiCnlsRkAAAOwAAAAAAAAAAAA=="
                    v-show="auth.loggingIn"/>
                <router-link class="btn btn-link" to="/register">Register</router-link>
            </div>
        </form>
        <p class="mt-5 mb-3 text-muted">Students breakdown team</p>
    </div>
</template>

<script>
    import {mapActions, mapState} from 'vuex'

    export default {
        data() {
            return {
                username: '',
                password: '',
                submitted: false
            }
        },
        computed: {
            ...mapState('account', ['auth'])
        },
        created() {
            // reset login auth
            this.logout();
        },
        methods: {
            ...mapActions('account', ['login', 'logout']),
            handleSubmit(e) {
                this.submitted = true;
                const {username, password} = this;
                if (username && password) {
                    this.login({username, password})
                }
            }
        }
    };
</script>

<style scoped>
    .form-signin {
        width: 100%;
        max-width: 330px;
        padding: 15px;
        margin: 0 auto;

    }

    *, ::after, ::before {

        box-sizing: border-box;

    }
</style>
