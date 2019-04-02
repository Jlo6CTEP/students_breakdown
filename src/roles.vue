<template>
<div>
	
	<input type="checkbox" id="pm" v-model="checked" style="float: left; margin-top: 5px;">
	<p style="margin-left: 25px;"> Product Manager
	</p>
	<label for="pm">{{ checked }}</label> 
	
	<input type="checkbox" id="frontender" v-model="checked" style="float: left; margin-top: 5px;">
	<p style="margin-left: 25px;"> Frontender
	</p>
	<label for="frontender">{{ checked }}</label> 
	
	<input type="checkbox" id="backender" v-model="checked" style="float: left; margin-top: 5px;">
	<p style="margin-left: 25px;"> Backender
	</p>
	<label for="backender">{{ checked }}</label> 
	
	<input type="checkbox" id="devops" v-model="checked" style="float: left; margin-top: 5px;">
	<p style="margin-left: 25px;"> Devops
	</p>
	<label for="devops">{{ checked }}</label> 	
	
	
	
</div>
</template>

<script>
export default {
	data(){
		return{
			mess: ''
		}
	}
}
</script>