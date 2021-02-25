Vue.prototype.$get_matching_lines = function(){
    let request_params = {'number_competitor_id' : number_competitor_app.selected_competitor}
    let url = '/matching/final-matching/page/get/?format=json'
    axios.get(url, {params: request_params})
        .then(function (response){
            final_matching_app.matching_data = JSON.parse(response.data.matching)
        }).catch(function (error){
            error_message(error)
        });
}

final_matching_app = new Vue({
    delimiters: ['{(', ')}'],
    el: '#final-matching-app',
    data: {
        edit_matching_status_url: '/matching/final-matching/edit-match/',
        rematch_url: '/matching/manual-matching/match/',
        filter_for_eas: '/matching/filters-by-tn_fv/?format=json',
        matching_data: null, //Данные мэтчинга для главной таблицы
        select_matching: { //Выбранная запись для редактирования
            sku_dict__pk: null,
            sku_dict__name: null,
            eas_dict__tn_fv: null,
            name_binding: null,
            type_binding: null,
        },
        type_binding: '',//Статус мэтчинга в форме редактирования
        tn_fv: '',
        manufacturer: '', // Используется в модальном окне перепривязки мэтчинга
        eas: [] // Используется в модальном окне перепривязки мэтчинга, массив результат поиска по ЕАС

    },
    methods: {
        /* Событие по клику, запуск редактора мэтчинга */
        show_redactor_matching(data){
            this.select_matching = data
        },
        /* Изменение статуса мэтчинга */
        edit_matching_request(sku_id){
            if(this.type_binding == ''){
                modal_error_app.error = 'Не выбран type_binding' //Сообщение об ошибке
                error_message()//запуск модального окна
                return false;
            }
            let request_params = {
                'number_competitor_id' : number_competitor_app.selected_competitor,
                'sku_id': sku_id,
                'type_binding': this.type_binding
            }
            let this_vue_app = this
            axios.post(this.edit_matching_status_url, {data: request_params})
                .then(function (response){
                    let res = JSON.parse(response.data.matching);
                    for(let i=0;i < this_vue_app.matching_data.length;i++){ //Изменение записи в таблице
                        if(this_vue_app.matching_data[i].sku_dict__pk == sku_id){
                            this_vue_app.matching_data[i].type_binding = res[0].type_binding
                            this_vue_app.matching_data[i].name_binding = res[0].name_binding
                        }
                    }
                }).catch(function (error){
                    error_message(error)
                });


        },
        /* Перепривязка СКУ к другому элементу ЕАС */
        rematch_request(eas_id, tn_fv){
            let sku_id = this.select_matching.sku_dict__pk

            let request_params = {
                'number_competitor_id' : number_competitor_app.selected_competitor,
                'eas_id': eas_id,
                'sku_id': sku_id
            }
            axios.post(this.rematch_url, {data: request_params})
                .then(function (response){
                }).catch(function (error){
                    error_message(error)
                });


            for(let i=0;i < this.matching_data.length;i++){ //Изменение записи в таблице
                if(this.matching_data[i].sku_dict__pk == sku_id){
                    this.matching_data[i].eas_dict__tn_fv = tn_fv
                }
            }
            /* Закрывает модалку */
            let modal_re_matching= document.getElementById('edit-matching-modal');
            let instance = M.Modal.getInstance(modal_re_matching);
            instance.close();

        }
    },
    computed: {
        search_for_eas_filter(){ // Поиск по ЕАС в модальном окне перепривязки мэтчинга
            let request_params = {
                'tn_fv': this.tn_fv,
                'manufacturer': this.manufacturer
            }
            axios.get(this.filter_for_eas, {params: request_params})
                .then(function (response){
                    final_matching_app.eas = JSON.parse(response.data.eas)
                }).catch(function (error){
                    error_message(error)
                });
        }
    },
    watch:{
        search_for_eas_filter: function (){}
    },
    mounted(){
        /* Стартовая выгрузка данных мэтчинга */
        this.$get_matching_lines()

        /* модальное окно перепривязки мэтчинга */
        let modal_re_matching= document.getElementById('re-matching');
        let instance_modal_re_matching = M.Modal.init(modal_re_matching);

        /* инициализация редактора мэтчинга */
        let modal_edit_match = document.getElementById('edit-matching-modal');
        let instance_modal_edit_match = M.Modal.init(modal_edit_match);

        /* инициализация select form в редакторе мэтчинга */
        let select_from = document.querySelector('.binding-type');
        M.FormSelect.init(select_from);

    }
})