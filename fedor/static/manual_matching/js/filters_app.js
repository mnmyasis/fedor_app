class FilterRequest extends PatternRequest{
    get_params() {
        return {
            'tn_fv': filters_app.tn_fv,
            'number_competitor_id': get_number_competitor(),
            'sku_id': manual_matching_app.active_sku,
            'barcode': filters_app.barcode,
            'manufacturer': filters_app.manufacturer
        }
    }

    response_access(response) {
        manual_matching_app.eas = JSON.parse(response.data.eas) // Выгрузка для списка EAS файлы manual.html и manual_matching_app.js
        filters_app.filter_lines.manufacturer = JSON.parse(response.data.manufacturer) //Выгрузка для выпадающего списка фильтров
        filters_app.filter_lines.barcode = JSON.parse(response.data.barcode)
        filters_app.filter_lines.tn_fv = JSON.parse(response.data.tn_fv)
    }

}

class SkuFilterRequest extends PatternRequest{
    constructor(search_line, type_filter) {
        super();
        this.search_line = search_line; //Строка из формы поиска
        this.type_filter = type_filter; //Select форма с выбором штрихкод\наименование
        this.competitor = get_number_competitor()
    }

    get_params() {
        return {
            'search_line': this.search_line,
            'type_filter': this.type_filter,
            'number_competitor_id': this.competitor,
        };
    }

    response_access(response) {
        console.log(response.data)
        manual_matching_app.sku = JSON.parse(response.data.sku)
    }
}

function filter_request(filter_value){
    if(manual_matching_app.active_sku){ //Актвная запись в таблице ску
        /* Если в форме фильтра нет данных, скрываем выпадающее меню */
        /* Как только в форме фильтра появляется значение, показываем */
        if(filter_value.length == 0){
            menu_status = false
        }else{
            menu_status = true
        }
        filters_app.request.business_logic(filters_app.url, 'get') //Обновляем информацию в таблице EAS
        return menu_status
    }else{
        modal_error_app.error = 'Не выбрана запись SKU'
        error_message()
        return false;
    }

}

filters_app = new Vue({
    delimiters: ['{(', ')}'],
    el: '#filters-app', //работает в файле manual_filters.html
    data: {
        tn_fv: '', // Для фильтр формы номенклатуры
        manufacturer: '', // Для фильтр формы производитель
        barcode: '', // Для фильтр формы штрих код
        url: '/matching/filters-matching/?format=json',
        sku_filter_url: '/matching/filters-matching/sku/?format=json',
        filter_lines: { // Результат для выпадающего списка, нужен для filters.html
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
        request: new Request(new FilterRequest())
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
            const eas_request = new EasRequest(manual_matching_app.active_sku, get_number_competitor());
            this.request.set_request(eas_request)
            this.request.business_logic(manual_matching_app.eas_load_url, 'get')
        },
        /* Запрос при записи данных в фильтрах */
        filter_manufacturer(){
            this.drop_menu_status.manufacturer= filter_request(this.manufacturer)//Фильтр производителя ЕАС
        },
        filter_tn_fv(){
            this.drop_menu_status.tn_fv= filter_request(this.tn_fv) //Фильтр наименования номенклатуры ЕАС
        },
        filter_barcode(){
            this.drop_menu_status.barcode= filter_request(this.barcode) //Фильтр Штрих код СКУ
        },
        filter_sku(){
            if(this.type_sku_filter){
                let sku_filter = new SkuFilterRequest(this.sku_filter_line, this.type_sku_filter)
                this.request.set_request(sku_filter)
                this.request.business_logic(this.sku_filter_url, 'get')
            }else{
                modal_error_app.error = 'Не выбрано поле фильтра'
                error_message()
            }

        },

        /* Клик по записи в выпадающем списке filter_line и type_menu получаем из filters.html */
        change_drop_menu_status(filter_line, type_menu){
            if(type_menu == 1){ //barcode
                this.barcode = filter_line //Заполнение формы выбранной записью из выпадающего списка
                this.drop_menu_status.barcode = false //Скрытие списка
            }
            if(type_menu == 2){ //tn_fv
                this.tn_fv = filter_line
                this.drop_menu_status.tn_fv = false
            }
            if(type_menu == 3){ //manufacturer
                this.manufacturer = filter_line
                this.drop_menu_status.manufacturer = false
            }
            this.request.business_logic(this.url, 'get') //обновляет список таблицы ЕАС на интерфейсе
        }
    },
    mounted(){
        let elems = document.querySelectorAll('sku-filter-form');
        let instances = M.FormSelect.init(elems);
    }
})