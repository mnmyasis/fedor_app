axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';


Vue.prototype.$load_sku_list = function (){
    let request_params = {'number_competitor_id' : JSON.stringify(number_competitor_app.sel_comp())}
    let url = '/matching/manual-matching/page/get/sku/?format=json'
    axios.get(url, {params: request_params})
    .then(function (response){
        manual_matching_app.sku = (JSON.parse(response.data.sku))
        manual_matching_app.eas = null
    }).catch(function (error){
        error_message(error)
    })
}

Vue.prototype.$load_eas_list = function (id_sku, url){
    let request_params = {
        'sku_id': id_sku
    }
    axios.get(url, {params: request_params})
        .then(function (response){
            manual_matching_app.eas = JSON.parse(response.data.eas)
        }).catch(function (error){
            error_message(error)
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
        rematch_url: '/matching/manual-matching/match/',
        active_sku: 0,
        active_sku_competitor: 0,
        font_size: 24,
        match_sku_id: 0,
        match_competitor_id: 0,
        active_name_sku: '',
        tn_fv: '',  // Используется в модальном окне перепривязки мэтчинга
        manufacturer: '', // Используется в модальном окне перепривязки мэтчинга
        filter_for_eas_rematch: '/matching/filters-by-tn_fv/?format=json',
        eas_rematch: [], // Используется в модальном окне ремэтчинга, массив результат поиска по ЕАС
        drop_menu_manufacturer_status: false,
        click_menu_manufacturer: false,
        manufacturer_rematch: ''
    },
    methods: {
        /* Запись ручной мэтчинг СКУ к ЕАС */
        matching(id_eas, type_binding, id_sku){
            this.match_sku_id = this.active_sku
            this.match_competitor_id = this.active_sku_competitor
            let request_params = {
                'number_competitor_id' : this.match_competitor_id,
                'eas_id': id_eas,
                'sku_id': this.match_sku_id,
                'type_binding': type_binding
            }
            axios.post(this.sku_eas_match_url, {data: request_params})
                .then(function (response){
                    manual_matching_app.sku = (JSON.parse(response.data.sku))
                }).catch(function (error){
                    error_message(error)
                });

            this.$load_sku_list() //Подгрузить данные
            this.eas = null
        },

        /* Выгрзука вариантов мэтчинга */
        load_eas_variants_for_sku(id_sku, name_sku, id_competitor){
            /* Активное состояние элемента */
            this.active_name_sku = name_sku
            this.active_sku_competitor = id_competitor
            this.active_sku = id_sku // Для какой номенклатуры выгружаются варианты мэтчинга
            this.$load_eas_list(id_sku, this.eas_load_url)
        },

        /* Выделение цветом выбранного элемента css класс eac-select*/
        change_status(id_sku){
            /* Вешаем активный класс на элемент клиентского товара */
            return{
            'sku-selected active' : this.active_sku === id_sku
            }
        },
        event_manufacturer_dropdown(data){
            this.manufacturer = data.manufacturer
            this.click_menu_manufacturer = true
            this.drop_menu_manufacturer_status= false
        },
        search_for_eas_filter(){
            let request_params = {
                'tn_fv': this.tn_fv,
                'manufacturer': this.manufacturer
            }
            axios.get(this.filter_for_eas_rematch, {params: request_params})
                .then(function (response){
                    manual_matching_app.eas_rematch = JSON.parse(response.data.eas.res)
                    manual_matching_app.manufacturer_rematch = JSON.parse(response.data.eas.mfcr)
                }).catch(function (error){
                    error_message(error)
                });
        },
        open_rematching(){
            /* ОТКРЫТЬ МОДАЛЬНОЕ ОКНО РЕМЭТЧИНГ */

            /* Удаление старых результатов */
            this.manufacturer = ''
            this.tn_fv = ''
            this.eas_rematch = []

            /* Открытие модального окна */
            let modal_re_matching= document.getElementById('re-matching')
            let instance = M.Modal.getInstance(modal_re_matching)
            instance.open()

        }
    },
    watch:{

        tn_fv: function(){
            if(this.tn_fv.length > 0){
                 this.search_for_eas_filter()
            }
        },

        manufacturer: function(){
            if(this.manufacturer.length == 0 || this.click_menu_manufacturer){ //Если был клик по выпадающему меню, то меню скрывается
                this.drop_menu_manufacturer_status = false // Скрывает меню
                this.click_menu_manufacturer = false
            }else{
               this.drop_menu_manufacturer_status = true
            }
            if(this.manufacturer.length > 0 ){
                this.search_for_eas_filter()
            }
        }

    },
    mounted(){
        let tabs = document.querySelector('.tabs');
        M.Tabs.init(tabs);
        /* Выгрузка ску номенклатуры */
        this.$load_sku_list();

        /* инициализация редактора мэтчинга */
        let modal_edit_match = document.getElementById('re-matching');
        let instance_modal_edit_match = M.Modal.init(modal_edit_match);

        /* инициализация select form в редакторе мэтчинга */
        let select_from = document.querySelector('.binding-type');
        M.FormSelect.init(select_from);

        let tooltip = document.querySelectorAll('.tooltipped');
        M.Tooltip.init(tooltip);

    },
})