
var search_form_app = new Vue({
    delimiters: ['{(', ')}'],
    el: '#search_form_app',
    data: {
        message: '',
        client_data: [],
        error: null,
        activeIndex: 0,

    },
    methods: {
        updateMessage(e){
            /* Функция поиска по ЕАК */
            console.log(e.target.value)
            axios.get('/auto/matching/client_directory/data/get/?format=json',{
                params: {
                   search_client_data : e.target.value,
                   number_competitor_id : 1
                }
            }).then(response => {
                this.client_data = JSON.parse(response.data.client_data)
            }).catch(error => {
                this.error = error
                console.log(error)
                /* запуск окна с ошибкой */
                error_message()
            })
        },
        element_select(id_client_directory){
            /* Функция выбора элемента */
            /* Активное состояние элемента */
            this.activeIndex = id_client_directory
        },
        change_status: function(id_client_directory){
            /* Вешаем активный класс на элемент */
            return{
            'eac-select' : this.activeIndex === id_client_directory
            }
        },
        /* Мэтчинг всех СКУ по ЕАК*/
        send_element_on_joint(event){
            console.log('index: ' + this.activeIndex)
            preloader_app.show_preloading = true
            axios.defaults.xsrfCookieName = 'csrftoken'
            axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
            axios.post('/auto/matching/client_directory/data/post/', {
                data: {
                    id_client_directory: this.activeIndex,
                    number_competitor_id: 1
                },
            }).then(function (response){
                console.log(response)
            }).catch(function(error){
                console.log(error)
            }).then(function(){
                preloader_app.show_preloading = false
            })
        }

    },
    mounted(){
        var tabs = document.querySelector('.tabs');
        var options = {};
        M.Tabs.init(tabs, options);

        var select_from = document.querySelector('.sel');
        var options = {};
        M.FormSelect.init(select_from, options);
    }
})

