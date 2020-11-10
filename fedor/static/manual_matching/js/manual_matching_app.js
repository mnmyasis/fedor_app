class SkuRequest extends PatternRequest{
    get_params(number_competitor = 1){
        return {
            'number_competitor_id' : number_competitor,
        }
    }

    response_access(response) {
        manual_matching_app.sku = JSON.parse(response.data.sku)
    }

}

class EasRequest extends PatternRequest{
    get_params() {
        return {
            'number_competitor_id' : manual_matching_app.number_competitor,
            'sku_id' : manual_matching_app.active_sku
        }
    }
    response_access(response) {
        manual_matching_app.eas = JSON.parse(response.data.eas)
    }


}

class MatchingRequest extends PatternRequest{
    get_params(){
        return {
            'eas_id': manual_matching_app.active_eas,
            'sku_id': manual_matching_app.active_sku,
            'number_competitor_id' : manual_matching_app.number_competitor,
        }
    }

    response_access(response) {
        manual_matching_app.sku = JSON.parse(response.data.sku)
    }
}

manual_matching_app = new Vue({
    delimiters: ['{(', ')}'],
    el: '#manual_matching_app',
    data: {
        sku: null,
        eas: null,
        number_competitor: 1,
        active_sku: 0,
        active_eas: 0,
    },
    methods: {

        /* Ручной мэтчинг СКУ к ЕАС */
        matching(id_eas){
            this.active_eas = id_eas
            matching_request = new MatchingRequest()
            request_match = new Request(matching_request)
            request_match.business_logic('/matching/manual-matching/match/', 'post')
            this.eas = null
        },

        /* Функция выбора элемента и выгрузки данных из ЕАС*/
        element_select(id_sku){
            /* Активное состояние элемента */
            this.active_sku = id_sku
            eas_request = new EasRequest()
            request1 = new Request(eas_request)
            request1.business_logic('/matching/manual-matching/page/get/eas/?format=json', 'get')
        },

        /* Выделение цветом выбранного элемента css класс eac-select*/
        change_status: function(id_sku){
            /* Вешаем активный класс на элемент */
            return{
            'eas-select' : this.active_sku === id_sku
            }
        },
    },
    mounted(){
        var tabs = document.querySelector('.tabs');
        var options = {};
        M.Tabs.init(tabs, options);

        sku_request = new SkuRequest()
        request = new Request(sku_request)
        request.business_logic('/matching/manual-matching/page/get/sku/?format=json', 'get')
    },
})