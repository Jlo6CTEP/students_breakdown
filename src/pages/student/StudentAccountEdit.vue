<template>
    <card>
        <h4 class="card-title" slot="header">Edit Profile</h4>
        <form>
            <div class="row">
                <div class="col-md-5">
                    <base-input :disabled="true"
                                label="Academic Group"
                                placeholder="Here your academic group"
                                type="text"
                                v-model="user.group">
                    </base-input>
                </div>
                <div class="col-md-3">
                    <base-input label="Username"
                                placeholder="Username"
                                type="text"
                                v-model="user.username">
                    </base-input>
                </div>
                <div class="col-md-4">
                    <base-input label="Email"
                                placeholder="Email"
                                type="email"
                                v-model="user.username">
                    </base-input>
                </div>
            </div>

            <div class="row">
                <div class="col-md-6">
                    <base-input label="First Name"
                                placeholder="First Name"
                                type="text"
                                v-model="user.firstName">
                    </base-input>
                </div>
                <div class="col-md-6">
                    <base-input label="Last Name"
                                placeholder="Last Name"
                                type="text"
                                v-model="user.lastName">
                    </base-input>
                </div>
            </div>

            <div class="row">
                <div class="col-md-12">
                    <base-input :disabled="true"
                                label="Address"
                                placeholder="Here your home address"
                                type="text"
                                v-model="user.address">
                    </base-input>
                </div>
            </div>

            <!--            <div class="row">-->
            <!--                <div class="col-md-4">-->
            <!--                    <base-input label="City"-->
            <!--                                placeholder="City"-->
            <!--                                type="text"-->
            <!--                                v-model="user.city">-->
            <!--                    </base-input>-->
            <!--                </div>-->
            <!--                <div class="col-md-4">-->
            <!--                    <base-input label="Country"-->
            <!--                                placeholder="Country"-->
            <!--                                type="text"-->
            <!--                                v-model="user.country">-->
            <!--                    </base-input>-->
            <!--                </div>-->
            <!--                <div class="col-md-4">-->
            <!--                    <base-input label="Postal Code"-->
            <!--                                placeholder="ZIP Code"-->
            <!--                                type="number"-->
            <!--                                v-model="user.postalCode">-->
            <!--                    </base-input>-->
            <!--                </div>-->
            <!--            </div>-->

            <div class="row">
                <div class="col-md-12">
                    <div class="form-group">
                        <label>About Me</label>
                        <textarea class="form-control border-input" placeholder="Here can be your description"
                                  rows="5"
                                  v-model="user.aboutMe">
                        </textarea>
                    </div>
                </div>
            </div>
            <div class="text-center">
                <button @click.prevent="updateProfile(user)" class="btn btn-info btn-fill float-right" type="submit">
                    Update Profile
                </button>
            </div>
            <div class="clearfix"></div>
        </form>
    </card>
</template>

<script>
    import Card from '../../components/cards/Card.vue'
    import BaseInput from '../../components/inputs/BaseInput';
    import {mapActions, mapState} from "vuex";

    export default {
        components: {
            Card,
            BaseInput
        },
        data() {
            return {}
        },
        computed: {
            ...mapState({
                user: state => state.account.user,
            }),
        },
        methods: {
            ...mapActions({
                updateProfile: 'users/update'
            }),
        }
    }

</script>

<style scoped>

</style>
