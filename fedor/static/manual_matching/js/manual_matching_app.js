manual_matching_app = new Vue({
    delimiters: ['{(', ')}'],
    el: '#manual_matching_app',
    data: {
        sku: null,
        eas: null,
        error: null,
        active_sku: 0
    },
    methods: {
        matching(id_eas){
            this.error = null
            console.log('Отправляю данные на стыковку')
            preloader_app.show_preloading = true
            axios.defaults.xsrfCookieName = 'csrftoken'
            axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
            axios.post('/matching/manual-matching/match/', {
                data:{
                    eas_id: id_eas,
                    sku_id: this.active_sku
                }
            }).then(function (response){
                if(this.error == null){
                    access_message()
                }
                console.log(response)
            }).catch(error => {
                this.error = error
                console.log(error)
                /* запуск окна с ошибкой */
                error_message()
            })
            preloader_app.show_preloading = false
            this.eas = null
        },
        element_select(id_sku){
            /* Функция выбора элемента */
            console.log(id_sku)
            /* Активное состояние элемента */
            this.active_sku = id_sku
            axios.get('/matching/manual-matching/page/get/eas/?format=json',{
                params: {
                    'sku_id' : id_sku
                }
            }).then(response => {
                this.eas = JSON.parse(response.data.eas)

            }).catch(error => {
                this.error = error
                console.log(error)
                /* запуск окна с ошибкой */
                error_message()
            })

        },
        change_status: function(id_sku){
            /* Вешаем активный класс на элемент */
            return{
            'eac-select' : this.active_sku === id_sku
            }
        },
    },
    mounted(){
        preloader_app.show_preloading = true
        axios.get('/matching/manual-matching/page/get/sku/?format=json',{
                params: {
                   'number_competitor_id' : 1
                }
            }).then(response => {
                this.sku = JSON.parse(response.data.sku)

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