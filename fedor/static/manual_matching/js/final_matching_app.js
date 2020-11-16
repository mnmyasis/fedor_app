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

class FilterTNFVRequest extends PatternRequest{
    constructor(tn_fv, manufacturer) {
        super();
        this.tn_fv = tn_fv
        this.manufacturer = manufacturer

    }
    get_params() {
        return {
            'tn_fv': this.tn_fv,
            'manufacturer': this.manufacturer
        }
    }

    response_access(response) {
        final_matching_app.eas = JSON.parse(response.data.eas) // Выгрузка для списка EAS файлы manual.html и manual_matching_app.js
    }

}

class RematchingRequest extends PatternRequest{
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
        //get_matching_lines() //Подгрузить данные
    }
}

function get_matching_lines(){
    /* Стартовая выгрузка данных мэтчинга */
    final_matching_request = new FinalMatchingRequest(1)
    request = new Request(final_matching_request)
    request.business_logic('/matching/final-matching/page/get/?format=json', 'get')
}

/* Запускается по события клика по кнопке */
function matching_redactor(){
    /* инициализация редактора мэтчинга */
    var modal_edit_match = document.getElementById('edit-matching-modal');
    var instance_modal_edit_match = M.Modal.init(modal_edit_match);
    instance_modal_edit_match.open()
    /* инициализация select form в редакторе мэтчинга */
    var select_from = document.querySelector('.binding-type');
    var options = {};
    M.FormSelect.init(select_from, options);
}

function re_matching_redactor(){
    /* инициализация редактора ре-мэтчинга */
    var modal_re_matching= document.getElementById('re-matching');
    var instance_modal_re_matching = M.Modal.init(modal_re_matching);
    instance_modal_re_matching.open()
}

final_matching_app = new Vue({
    delimiters: ['{(', ')}'],
    el: '#final-matching-app',
    data: {
        edit_matching_url: '/matching/final-matching/edit-match/',
        rematch_url: '/matching/manual-matching/match/',
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
        tn_fv: '',
        manufacturer: '',
        eas: ''

    },
    methods: {
        /* Событие по клику, запуск редактора мэтчинга */
        show_redactor_matching(data){
            this.select_matching = data
            matching_redactor() //Инцилизация модального окна
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
        },
        redactor_rematching(){
            re_matching_redactor()
        },
        filter_tn_fv(){
            req = new Request(new FilterTNFVRequest(this.tn_fv, this.manufacturer))
            req.business_logic('/matching/filters-by-tn_fv/?format=json', 'get')
        },
        /* Перепривязка СКУ к другому элементу ЕАС */
        rematch_request(eas_id, tn_fv){
            this.eas_dict__tn_fv = this.tn_fv
            sku_id = this.select_matching.sku_dict__pk
            rematch_req = new RematchingRequest(eas_id,sku_id,this.number_competitor)
            req = new Request(rematch_req)
            req.business_logic(this.rematch_url, 'post')

            for(let i=0;i < this.matching_data.length;i++){
                this.matching_data[i]
                if(this.matching_data[i].sku_dict__pk == sku_id){
                    this.matching_data[i].eas_dict__tn_fv = tn_fv
                }
            }
            var modal_re_matching= document.getElementById('re-matching');
            var instance = M.Modal.getInstance(modal_re_matching);
            instance.destroy();

        }
    },
    mounted(){
        /* Стартовая выгрузка данных мэтчинга */
        get_matching_lines()
    }
})