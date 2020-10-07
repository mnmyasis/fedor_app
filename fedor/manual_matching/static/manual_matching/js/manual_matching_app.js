manual_matching_app = new Vue({
    delimiters: ['{(', ')}'],
    el: '#manual_matching_app',
    data: {
        sku: null,
        error: null
    },
    methods: {
        element_select(id_client_directory){
            /* Функция выбора элемента */
            console.log(id_client_directory)
            /* Активное состояние элемента */
            this.activeIndex = id_client_directory
        },
        change_status: function(id_client_directory){
            /* Вешаем активный класс на элемент */
            return{
            'eac-select' : this.activeIndex === id_client_directory
            }
        },
    },
    mounted(){
        preloader_app.show_preloading = true
        axios.get('/matching/manual-matching/page/get/?format=json',{
                params: {
                   'number_competitor_id' : 1
                }
            }).then(response => {
                this.sku = JSON.parse(response.data.sku)
                console.log(this.sku)

            }).catch(error => {
                console.log('#################################################')
                this.error = error
                console.log(error)
                /* запуск окна с ошибкой */
                error_message()
                console.log('#################################################')
            }).then(function(){
                preloader_app.show_preloading = false
            })
    }
})