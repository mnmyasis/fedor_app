Vue.prototype.$get_matching_lines = function(){
    //Стартовая выгрузка записей в таблицу
    if(final_filters_app.statuses.length > 0 || final_filters_app.sku_form.length > 0 || final_filters_app.eas_form.length > 0){
        final_filters_app.filter()
        return;
    }
    let request_params = {
    'number_competitor_id' : JSON.stringify(number_competitor_app.sel_comp()),
    }
    let url = '/matching/final-matching/page/get/?format=json'
    axios.get(url, {params: request_params})
        .then(function (response){
             console.log(response.data.matching )
            final_matching_app.matching_data = JSON.parse(response.data.matching)

        }).catch(function (error){
            error_message(error)
        });
}

final_matching_app = new Vue({
    delimiters: ['{(', ')}'],
    el: '#final-matching-app',
    data: {
        delete_matching_url: '/matching/final-matching/delete/',
        filter_for_eas: '/matching/filters-by-tn_fv/?format=json',
        matching_data: null, //Данные мэтчинга для главной таблицы

        tn_fv: '',  // Используется в модальном окне перепривязки мэтчинга
        manufacturer: '', // Используется в модальном окне перепривязки мэтчинга
        filter_for_eas_rematch: '/matching/filters-by-tn_fv/?format=json',
        sku_eas_match_url: '/matching/manual-matching/match/',
        eas_rematch: [], // Используется в модальном окне ремэтчинга, массив результат поиска по ЕАС
        drop_menu_manufacturer_status: false,
        click_menu_manufacturer: false,
        manufacturer_rematch: '',
        active_name_sku: '',
        match_sku_id: '',
        match_competitor_id: ''

    },
    methods: {
        delete_matching(id_sku, competitor){
            /* Удалить результат и отправить обратно в алгоритм */
            let request_params = {
                'number_competitor_id' : competitor,
                'sku_id': id_sku,
            }
            axios.post(this.delete_matching_url, {data: request_params})
                .then(function (response){
                    final_matching_app.$get_matching_lines()
                }).catch(function (error){
                    error_message(error)
                });
        },
        open_rematching(id_sku, name_sku, competitor_id){
            /* ОТКРЫТЬ МОДАЛЬНОЕ ОКНО РЕМЭТЧИНГ */

            /* Удаление старых результатов */
            this.manufacturer = ''
            this.tn_fv = ''
            this.eas_rematch = [],
            this.active_name_sku = name_sku
            this.match_sku_id = id_sku
            this.match_competitor_id = competitor_id

            /* Открытие модального окна */
            let modal_re_matching= document.getElementById('final-re-matching')
            let instance = M.Modal.getInstance(modal_re_matching)
            instance.open()

        },
        search_for_eas_filter(){
            /* Поиск по ЕАС в модальном окне */
            let request_params = {
                'tn_fv': this.tn_fv,
                'manufacturer': this.manufacturer
            }
            axios.get(this.filter_for_eas_rematch, {params: request_params})
                .then(function (response){
                    final_matching_app.eas_rematch = JSON.parse(response.data.eas.res)
                    final_matching_app.manufacturer_rematch = JSON.parse(response.data.eas.mfcr)
                }).catch(function (error){
                    error_message(error)
                });
        },
        event_manufacturer_dropdown(data){
            /* Выпадающее меню производителя в модальном окне*/
            this.manufacturer = data.manufacturer
            this.click_menu_manufacturer = true
            this.drop_menu_manufacturer_status= false
        },

        matching(id_eas, type_binding){
            let request_params = {
                'number_competitor_id' : this.match_competitor_id,
                'eas_id': id_eas,
                'sku_id': this.match_sku_id,
                'type_binding': type_binding
            }
            axios.post(this.sku_eas_match_url, {data: request_params})
                .then(function (response){
                   final_matching_app.$get_matching_lines()
                }).catch(function (error){
                    error_message(error)
                });
        },
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
        /* Стартовая выгрузка данных мэтчинга */
        let final_tab = document.querySelector('.final');
        /* инициализация редактора мэтчинга */
        let modal_edit_match = document.getElementById('final-re-matching');
        let instance_modal_edit_match = M.Modal.init(modal_edit_match);

        final_tab.onclick = function(){
            final_matching_app.$get_matching_lines()
        }

    }
})