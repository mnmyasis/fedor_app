group_changes_app = new Vue({
    el: '#group_changes_app',
    delimiters: ['{(', ')}'],
    data: {
        url_add_group_change: '/directory/group_changes/add/', // Добавление новых подмен в БД
        url_group_changes_update: '/directory/group_changes/update/', // Изменение в бд подмен
        url_group_changes_filter: '/directory/group_changes/filter/', // Фильтрация подмен в модальном окне
        url_edit_group_change_list: '/directory/group_changes/edit-list/', // Список подмен в модальном окне
        url_group_changes_start: '/directory/group_changes/', // Запуск массовых подмен
        exclude_list: [], // Список выбранных исключений
        edit_group_change_list: [], // Список всех подмен в модальном окне
        group_change_input: '', // Фильтр в модальном окне подмен
        group_search_input: '', // Фильтр в модальном окне подмен
        update_change: '', // редактирование подмены
        update_search: '', // редактирование подмены
        selected_group_change_pk: '',
        add_change: '',
        add_search: ''
    },
    methods: {
        exclude_group_changes(change_id, change_name){ // Клик по элементу выпадающего списка подмен для исключения
            this.exclude_list.push({
                pk: change_id,
                change: change_name
            })
        },
        group_change_start(){ // Запуск массовых подмен
            preloader_app.show_preloading = true
            for(i = 0; i < this.edit_group_change_list.length; i++){
                if(this.edit_group_change_list[i].exclude == true){
                    console.log(this.edit_group_change_list[i])
                    this.exclude_group_changes(this.edit_group_change_list[i].pk, this.edit_group_change_list[i].change)
                }
            }
            let request_params = {
                'number_competitor_id': JSON.stringify(number_competitor_app.sel_comp()),
                'exclude_list': JSON.stringify(this.exclude_list),
            }
            axios.get(this.url_group_changes_start, {params: request_params})
                .then(function (response) {
                    access_message()
                }).catch(function (error) {
                    error_message(error)
                }).then(function(){
                    preloader_app.show_preloading = false
                });
        },
        edit_group_change_load(){ // Список всех подмен в модальном окне
            axios.get(this.url_edit_group_change_list)
                .then(function (response) {
                    group_changes_app.edit_group_change_list = JSON.parse(response.data.group_changes_list)
                }).catch(function (error) {
                    error_message(error)
                });
        },
        update_group_change(){ // Изменение в БД записи подмен
            let request_params = {
                'pk': this.selected_group_change_pk,
                'change': this.update_change,
                'search': this.update_search
            }
            axios.post(this.url_group_changes_update, {data: request_params})
                .then(function (response){
                    if(response.data.error){
                        modal_error_app.error_message(response.data.error_message)
                    }else{
                        modal_access_app.access_message(response.data.access)
                    }
                }).catch(function (error){
                    error_message(error)
                });
            /* Обновление записи в таблице */
            for(let i = 0; i < this.edit_group_change_list.length; i++){
                if(this.edit_group_change_list[i].pk == this.selected_group_change_pk){
                    this.edit_group_change_list[i].change = this.update_change
                    this.edit_group_change_list[i].search = this.update_search
                    break
                }
            }
        },
        add_group_change(){ // Добавление новых подмен в БД
            if(this.add_change && this.add_search){
                let request_params = {
                    'change': this.add_change,
                    'search': this.add_search
                }
                axios.post(this.url_add_group_change, {data: request_params})
                    .then(function (response){
                        if(response.data.error){
                            modal_error_app.error_message(response.data.error_message)
                        }else{
                            modal_access_app.access_message(response.data.access)
                            M.Modal.init(document.getElementById('add-group-change-modal')).close(); // Закрытие модального окна
                        }
                    }).catch(function (error){
                        error_message(error)
                    });
            }else{
                modal_error_app.error_message("Необходимо заполнить обе формы.")
            }
        },
        select_group_change(change){ // Выбранная запись в таблице для редактирования
            this.selected_group_change_pk = change.pk // id для обновления записи в бд
            this.update_change = change.change // заполнение формы
            this.update_search = change.search // заполнение формы
        }
    },
    mounted(){
        M.Modal.init(document.getElementById('edit-group-changes-modal'));
        M.Modal.init(document.getElementById('edit-group-change-line-modal'));
        M.Modal.init(document.getElementById('add-group-change-modal'));
        this.edit_group_change_load() // Подгрузка всего спика подмен для модального окна Редактирование подмен
    },
    computed:{
        filter_edit_changes: function (){ // Фильтрация списка подмен
            let request_params = {
                'group_change_input': this.group_change_input,
                'group_search_input': this.group_search_input,
            }
            axios.get(this.url_group_changes_filter, {params: request_params})
                .then(function (response) {
                    group_changes_app.edit_group_change_list = JSON.parse(response.data.group_changes_list)
                }).catch(function (error) {
                    error_message(error)
                });
        },
    },
    watch:{
        filter_edit_changes: function (){},
    }
})