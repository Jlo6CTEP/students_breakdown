<template>
    <div class="header clearfix">
        <nav>
            <ul class="nav nav-pills float-right">
                <li class="nav-item">
                    <router-link active-class="active" class="nav-link" exact to="/">Home</router-link>
                </li>
                <li class="nav-item">
                    <router-link active-class="active" class="nav-link" exact to="/account">Account</router-link>
                </li>
                <li class="nav-item">
                    <router-link active-class="active" class="nav-link" to="/surveys">Surveys</router-link>
                </li>
                <li class="nav-item">
                    <router-link active-class="active" class="nav-link" to="/contact">Contacts</router-link>
                </li>
            </ul>
        </nav>
        <h3 class="text-muted">Breakdown project</h3>
    </div>
</template>

<script>
    export default {
        name: "Header"
    };
</script>
