<template>
    <form id="example1">
        <div >
            <button v-on:click= "cour = cour + 2" >+1</button>
            <p>Кнопка выше была нажата {{ cour }} раз</p>

        </div>
    </form>
</template>

<script>
    import Vue from 'vue';

    var sample = new Vue({
        el: '#example1',
        data: {
            cour: 0
        }
    })


    </script>

