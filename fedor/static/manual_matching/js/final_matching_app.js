final_matching_app = new Vue({
    delimiters: ['{(', ')}'],
    el: '#final-matching-app',
    data: {
        matching_data: null,
        error: null,
    },
    methods: {

    },
    mounted(){
        preloader_app.show_preloading = true
        axios.get('/matching/final-matching/page/get/?format=json',{
            params: {
                'number_competitor_id' : 1
            }
        }).then(response => {
            this.matching_data = JSON.parse(response.data.matching)
            console.log(this.matching_data)

        }).catch(error => {
            this.error = error
            console.log(error)
            /* запуск окна с ошибкой */
            error_message()
        }).then(function(){
            preloader_app.show_preloading = false

        })

    }
})