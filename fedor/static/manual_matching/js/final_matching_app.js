function get_matching_lines(){
    /* Стартовая выгрузка данных мэтчинга */
    preloader_app.show_preloading = true
    axios.get('/matching/final-matching/page/get/?format=json',{
        params: {
            'number_competitor_id' : 1
        }
    }).then(response => {
        final_matching_app.matching_data = JSON.parse(response.data.matching)
    }).catch(error => {
        modal_error_app.error = error //Сообщение обошибке
        error_message()//запуск модального окна
    }).then(function(){
        preloader_app.show_preloading = false

    })
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
        matching_data: null, //Данные мэтчинга для главной таблицы
        error: null,
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


            this.error = null
            preloader_app.show_preloading = true
            axios.defaults.xsrfCookieName = 'csrftoken'
            axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
            axios.post('/matching/final-matching/edit-match/', {
                data:{
                    sku_id: sku_id,
                    type_binding: this.type_binding,
                    number_competitor_id: this.number_competitor
                }
            }).then(function (response){
                this.matching_data= get_matching_lines()
            }).catch(error => {
                this.error = error
                modal_error_app.error = this.error //Сообщение об ошибке
                error_message()//запуск модального окна
            })

            preloader_app.show_preloading = false
        }
    },
    mounted(){
        /* Стартовая выгрузка данных мэтчинга */
        get_matching_lines()


    }
})