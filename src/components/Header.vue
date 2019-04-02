<template>
    <div class="header clearfix">
        <nav>
            <ul class="nav nav-pills float-right">
                <li class="nav-item">
                    <router-link active-class="active" class="nav-link" exact to="/">Account</router-link>
                </li>
                <li class="nav-item">
                    <router-link active-class="active" class="nav-link" to="/users">Surveys</router-link>
                </li>
            </ul>
        </nav>
        <h3 class="text-muted">Our fancy project</h3>
    </div>
</template>

<script>
    export default {
        name: "Header"
    };
</script>
