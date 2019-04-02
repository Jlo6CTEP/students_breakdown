<template>
<div class="blocktext">
<h1>Project priority</h1>
<app-input></app-input>
<app-button></app-button>
</div>

</template>

<script>
import Input from './field2.vue';
import Button from './nicebutton.vue';
export default {
	components:{
		'app-input':Input,
		'app-button':Button}
	}
</script>

