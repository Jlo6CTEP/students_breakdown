<template>
    <div>
        <form>
            <div id="example1">
                <button v-on:click="increment(cour)">+1</button>
                <p>Кнопка выше была нажата {{ cour }} раз</p>

            </div>
        </form>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                cour: 1
            };
        }
    }

</script>

