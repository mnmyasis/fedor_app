class FinalMatchingRequest extends PatternRequest{ //Выгрузка данных в таблицу
    constructor(competitor){
        super();
        this.competitor = competitor
    }

    get_params() {
        return {
            'number_competitor_id' : this.competitor
        }
    }

    response_access(response) {
        final_matching_app.matching_data = JSON.parse(response.data.matching)
    }

}

class EditStatusMatchingRequest extends PatternRequest{ //Редактор статуса мэтчинга
    constructor(sku_id, competitor, type_bindig){
        super();
        this.competitor = competitor
        this.sku_id = sku_id
        this.type_binding = type_bindig
    }

    get_params() {
        return {
            'sku_id': this.sku_id,
            'type_binding': this.type_binding,
            'number_competitor_id': this.competitor
        }
    }

    response_access(response) {
        get_matching_lines() //Обновление данных в таблице после редактирования
    }
}

function get_matching_lines(){
    /* Стартовая выгрузка данных мэтчинга */
    final_matching_request = new FinalMatchingRequest(1)
    request = new Request(final_matching_request)
    request.business_logic('/matching/final-matching/page/get/?format=json', 'get')
}

function matching_redactor(){
    /* инициализация редактора мэтчинга */
    var modal_access = document.getElementById('edit-matching-modal');
    var instance = M.Modal.init(modal_access);
    instance.open()
    /* инициализация select form в редакторе мэтчинга */
    var select_from = document.querySelector('.binding-type');
    var options = {};
    M.FormSelect.init(select_from, options);
}

final_matching_app = new Vue({
    delimiters: ['{(', ')}'],
    el: '#final-matching-app',
    data: {
        edit_matching_url: '/matching/final-matching/edit-match/',
        matching_data: null, //Данные мэтчинга для главной таблицы
        select_matching: { //Выбранная запись для редактирования
            sku_dict__pk: null,
            sku_dict__name: null,
            eas_dict__tn_fv: null,
            name_binding: null,
            type_binding: null
        },
        type_binding: '',//Статус мэтчинга в форме редактирования
        selected: '',
        number_competitor: 1,

    },
    methods: {
        /* Событие по клику, запуск редактора мэтчинга */
        show_redactor_matching(data){
            this.select_matching = data
            matching_redactor()
        },
        /* Изменение статуса мэтчинга */
        edit_matching_request(sku_id){
            if(this.type_binding == ''){
                modal_error_app.error = 'Не выбран type_binding' //Сообщение об ошибке
                error_message()//запуск модального окна
                return false;
            }
            edit_status_request = new EditStatusMatchingRequest(sku_id, this.number_competitor, this.type_binding)
            request = new Request(edit_status_request)
            request.business_logic(this.edit_matching_url,'post')
        }
    },
    mounted(){
        /* Стартовая выгрузка данных мэтчинга */
        get_matching_lines()
    }
})