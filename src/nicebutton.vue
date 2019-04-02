<template>
  <VueLoadingButton class='send' aria-label='Send message'/>
</template>

<script>
import VueLoadingButton from './nbutton/vue-loading-button'

export default {
  components: {
    VueLoadingButton,
  }
}
</script>

<style>
VueLoadingButton.send{
	margin-top: 5px;
}
</style>