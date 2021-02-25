filters_app = new Vue({
    delimiters: ['{(', ')}'],
    el: '#filters-app', //работает в файле manual_filters.html
    data: {
        tn_fv: '', // Для фильтр формы номенклатуры
        manufacturer: '', // Для фильтр формы производитель
        barcode: '', // Для фильтр формы штрих код
        url: '/matching/filters-matching/?format=json',
        sku_filter_url: '/matching/filters-matching/sku/?format=json',
        filter_lines: { // Выпадающий список при поиске по фильтру
            'manufacturer' : null,
            'tn_fv': null,
            'barcode': null
        },
        drop_menu_status: { // При false выпадающий список не показывается
            'manufacturer': false, //Производитель ЕАС
            'tn_fv': false, //наименование номенклатуры ЕАС
            'barcode': false //Штрихкод СКУ
        },
        sku_filter_line: '',
        type_sku_filter: '',
        stop_watch_for_click: false,
    },
    methods:{
        /* Сброс фильтров */
        reset_filter(){
            this.drop_menu_status.manufacturer = false // Статус показывать\не показывать
            this.drop_menu_status.tn_fv = false
            this.drop_menu_status.barcode = false
            this.filter_lines.tn_fv = null // Значение в выпадающего списка
            this.filter_lines.manufacturer = null
            this.filter_lines.barcode = null
            this.tn_fv = ''  // Значение в форме
            this.manufacturer = ''
            this.barcode = ''

            // Выгрузка без фильтров
            this.$load_eas_list(manual_matching_app.active_sku, manual_matching_app.eas_load_url)
        },

        /* Клик по записи в выпадающем списке filter_line и type_menu получаем из filters.html */
        change_drop_menu_status(filter_line, type_menu){
            this.stop_watch_for_click = true // запрещает показывать выпадающее меню.
            if(type_menu == 1){ //barcode
                this.barcode = filter_line //Заполнение формы выбранной записью из выпадающего списка
            }
            if(type_menu == 2){ //tn_fv
                this.tn_fv = filter_line
            }
            if(type_menu == 3){ //manufacturer
                this.manufacturer = filter_line
            }
        },
    },

    computed: {
        filter_for_eas_variant:
            function () {
                if(manual_matching_app.active_sku) {
                    //console.log('computed ' + this.tn_fv + ' ' + this.manufacturer + ' ' + this.barcode)
                    let request_params = {
                        'number_competitor_id': number_competitor_app.selected_competitor,
                        'tn_fv': this.tn_fv,
                        'sku_id': manual_matching_app.active_sku,
                        'barcode': this.barcode,
                        'manufacturer': this.manufacturer
                    }
                    axios.get(this.url, {params: request_params})
                        .then(function (response) {
                            manual_matching_app.eas = JSON.parse(response.data.eas)
                            filters_app.filter_lines.manufacturer = JSON.parse(response.data.manufacturer)
                            filters_app.filter_lines.barcode = JSON.parse(response.data.barcode)
                            filters_app.filter_lines.tn_fv = JSON.parse(response.data.tn_fv)
                        }).catch(function (error) {
                        modal_error_app.error = error
                        error_message()
                    });

                }else if(this.manufacturer.length > 0 || this.tn_fv.length > 0 || this.barcode.length > 0){
                    modal_error_app.error = 'Не выбрана запись SKU'
                    error_message()
                    return false;
                }
        },
    },
    watch: {
        filter_for_eas_variant: function (){},
        manufacturer: function () {
            if(this.manufacturer.length == 0 || this.stop_watch_for_click) { //Если был клик по выпадающему меню, то меню скрывается
                this.drop_menu_status.manufacturer = false
                this.stop_watch_for_click = false // Разрешает показывать всплывающее меню
            }else{
                this.drop_menu_status.manufacturer = true
            }
        },
        tn_fv: function (){
            if(this.tn_fv.length == 0 || this.stop_watch_for_click) {
                this.drop_menu_status.tn_fv = false
                this.stop_watch_for_click = false
            }else{
                this.drop_menu_status.tn_fv = true
            }
        },
        barcode: function (){
            if(this.barcode.length == 0 || this.stop_watch_for_click) {
                this.drop_menu_status.barcode = false
                this.stop_watch_for_click = false
            }else{
                this.drop_menu_status.barcode = true
            }
        },
        sku_filter_line: function (){
            if(this.sku_filter_line.length > 0){ //Если в форме есть значение
                if(this.type_sku_filter){ // Если выбран фильтр, иначе ошибка
                    let request_params = {
                        'number_competitor_id': number_competitor_app.selected_competitor,
                        'search_line': this.sku_filter_line,
                        'type_filter': this.type_sku_filter,
                    }
                    axios.get(this.sku_filter_url, {params: request_params})
                        .then(function (response) {
                            manual_matching_app.sku = JSON.parse(response.data.sku)
                        }).catch(function (error) {
                            modal_error_app.error = error
                            error_message()
                        });
                }else{
                    modal_error_app.error = 'Не выбрано поле фильтра'
                    error_message()
                }
            }else{
                this.$load_sku_list() // Выгрузка номенклатуры без фильтрации
            }
        }
    },
    mounted(){
        let sku_filter_form = document.getElementById('sku-filter-form');
        let instances = M.FormSelect.init(sku_filter_form);
    },
})