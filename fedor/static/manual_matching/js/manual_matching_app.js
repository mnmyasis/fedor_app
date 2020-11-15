class SkuRequest extends PatternRequest{
    constructor(competitor){
        super();
        this.competitor = competitor
    }
    get_params(){
        return {
            'number_competitor_id' : this.competitor,
        }
    }

    response_access(response) {
        manual_matching_app.sku = JSON.parse(response.data.sku)
    }

}

class EasRequest extends PatternRequest{
    constructor(sku_id, competitor) {
        super();
        this.competitor = competitor
        this.sku_id = sku_id
    }

    get_params() {
        return {
            'number_competitor_id' : this.competitor ,
            'sku_id' :  this.sku_id
        }
    }
    response_access(response) {
        manual_matching_app.eas = JSON.parse(response.data.eas)
    }


}

class MatchingRequest extends PatternRequest{
    constructor(eas_id, sku_id, competitor) {
        super();
        this.eas_id = eas_id
        this.sku_id = sku_id
        this.competitor = competitor
    }
    get_params(){
        return {
            'eas_id': this.eas_id ,
            'sku_id': this.sku_id,
            'number_competitor_id' : this.competitor,
        }
    }

    response_access(response) {
        manual_matching_app.sku = JSON.parse(response.data.sku)
        load_sku_list() //Подгрузить данные
    }
}

function load_sku_list(){
    sku_request = new SkuRequest(1)
    request = new Request(sku_request)
    request.business_logic('/matching/manual-matching/page/get/sku/?format=json', 'get')
}

manual_matching_app = new Vue({
    delimiters: ['{(', ')}'],
    el: '#manual_matching_app',
    data: {
        sku: null,
        eas: null,
        eas_load_url: '/matching/manual-matching/page/get/eas/?format=json',
        sku_eas_match_url: '/matching/manual-matching/match/',
        number_competitor: 1,
        active_sku: 0,
    },
    methods: {

        /* Ручной мэтчинг СКУ к ЕАС */
        matching(id_eas){
            id_sku = this.active_sku
            matching_request = new MatchingRequest(id_eas, id_sku, this.number_competitor)
            request_match = new Request(matching_request)
            request_match.business_logic(this.sku_eas_match_url, 'post')
            this.eas = null
        },

        /* Функция выбора элемента и выгрузки данных из ЕАС*/
        element_select(id_sku){
            /* Активное состояние элемента */
            this.active_sku = id_sku
            eas_request = new EasRequest(id_sku, this.number_competitor)
            request1 = new Request(eas_request)
            request1.business_logic(this.eas_load_url, 'get')
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

        load_sku_list()
    },
})