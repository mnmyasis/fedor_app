axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';


Vue.prototype.$load_sku_list = function (){
    let request_params = {'number_competitor_id' : number_competitor_app.selected_competitor}
    let url = '/matching/manual-matching/page/get/sku/?format=json'
    axios.get(url, {params: request_params}).then(function (response){
        manual_matching_app.sku = (JSON.parse(response.data.sku))
    }).catch(function (error){
        modal_error_app.error = error
        error_message()
    })
}

Vue.prototype.$load_eas_list = function (id_sku, url){
    let request_params = {
        'number_competitor_id' : number_competitor_app.selected_competitor,
        'sku_id': id_sku
    }
    axios.get(url, {params: request_params})
        .then(function (response){
            console.log(response)
            manual_matching_app.eas = JSON.parse(response.data.eas)
        }).catch(function (error){
            modal_error_app.error = error
            error_message()
        });
}

manual_matching_app = new Vue({
    delimiters: ['{(', ')}'],
    el: '#manual_matching_app',
    data: {
        sku: null,
        eas: null,
        old_eas: null,
        eas_load_url: '/matching/manual-matching/page/get/eas/?format=json',
        sku_eas_match_url: '/matching/manual-matching/match/',
        active_sku: 0,
    },
    methods: {

        /* Запись ручной мэтчинг СКУ к ЕАС */
        matching(id_eas){
            let id_sku = this.active_sku
            let request_params = {
                'number_competitor_id' : number_competitor_app.selected_competitor,
                'eas_id': id_eas,
                'sku_id': id_sku
            }
            axios.post(this.sku_eas_match_url, {data: request_params})
                .then(function (response){
                    manual_matching_app.sku = (JSON.parse(response.data.sku))
                }).catch(function (error){
                    modal_error_app.error = error
                    error_message()
                });

            this.$load_sku_list() //Подгрузить данные
            this.eas = null
        },

        /* Выгрзука вариантов мэтчинга */
        load_eas_variants_for_sku(id_sku){
            /* Активное состояние элемента */
            console.log(id_sku)
            this.active_sku = id_sku // Для какой номенклатуры выгружаются варианты мэтчинга
            this.$load_eas_list(id_sku, this.eas_load_url)

        },

        /* Выделение цветом выбранного элемента css класс eac-select*/
        change_status(id_sku){
            /* Вешаем активный класс на элемент */
            return{
            'eas-select' : this.active_sku === id_sku
            }
        },
    },
    mounted(){
        let tabs = document.querySelector('.tabs');
        M.Tabs.init(tabs);
        /* Выгрузка ску номенклатуры */
        this.$load_sku_list();
    },
})