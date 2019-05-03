<template>
    <transition mode="out-in" name="fade">
        <router-view></router-view>
    </transition>
</template>

<script>
    export default {
        name: "Content"
    }
</script>

<style scoped>

</style>
