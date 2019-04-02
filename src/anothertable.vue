<template>
<div>
	<input type="text" v-model="mess">
	<p> {{mess}}</p>
	
	<input type="checkbox" id="java" v-model="checked" style="float: left; margin-top: 5px;">
	<p style="margin-left: 25px;"> Java
	</p>
	<label for="java">{{ checked }}</label> 
	
	<input type="checkbox" id="python" v-model="checked" style="float: left; margin-top: 5px;">
	<p style="margin-left: 25px;"> Python
	</p>
	<label for="python">{{ checked }}</label> 
	
	<input type="checkbox" id="c" v-model="checked" style="float: left; margin-top: 5px;">
	<p style="margin-left: 25px;"> C
	</p>
	<label for="c">{{ checked }}</label> 
	
	<input type="checkbox" id="sqlite" v-model="checked" style="float: left; margin-top: 5px;">
	<p style="margin-left: 25px;"> Sqlite
	</p>
	<label for="sqlite">{{ checked }}</label> 
	
	<input type="checkbox" id="mongo" v-model="checked" style="float: left; margin-top: 5px;">
	<p style="margin-left: 25px;"> MongoDB
	</p>
	<label for="mongo">{{ checked }}</label> 
	
	<input type="checkbox" id="css" v-model="checked" style="float: left; margin-top: 5px;">
	<p style="margin-left: 25px;"> CSS
	</p>
	<label for="css">{{ checked }}</label> 

	
	
	
	
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