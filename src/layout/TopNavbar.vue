<template>
    <nav class="navbar navbar-expand-lg">
        <div class="container-fluid">
            <span class="navbar-brand">Dashboard</span>
            <div class="collapse navbar-collapse justify-content-end">
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item">
                        <router-link :to="getAccountUrl" class="nav-link">
                            Account
                        </router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/login">
                            Log out
                        </router-link>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<script>
    import DropDown from '../components/DropDown';
    import {store} from '../_store';

    export default {
        name: 'TopNavBar',
        components: {
            DropDown,
        },
        computed: {
            routeName() {
                const {name} = this.$route;
                return this.capitalizeFirstLetter(name)
            },
            getAccountUrl: () => {
                return store.getters["account/getUrl"]('/account');
            }
        },
        data() {
            return {
                activeNotifications: false
            }
        },
        methods: {
            capitalizeFirstLetter(string) {
                return string.charAt(0).toUpperCase() + string.slice(1)
            },
            toggleNotificationDropDown() {
                this.activeNotifications = !this.activeNotifications
            },
            closeDropDown() {
                this.activeNotifications = false
            },
            toggleSidebar() {
                this.$sidebar.displaySidebar(!this.$sidebar.showSidebar)
            },
            hideSidebar() {
                this.$sidebar.displaySidebar(false)
            }
        }
    }

</script>

<style scoped>

</style>
