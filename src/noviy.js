console.clear()


Vue.component('add-match-form', {
  template: '#add-match-template',
  data: function() {
    return {
      games: [
        {'value': 1, 'text': 'Game 1'},
        {'value': 4, 'text': 'Game 4'}
      ],
      selected_game: null
    }
  }
})

new Vue({
  el: "#add_match_form"
})