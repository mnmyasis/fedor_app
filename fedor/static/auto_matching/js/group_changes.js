group_changes_app = new Vue({
    el: '#group_changes_app',
    delimiters: ['{(', ')}'],
    data: {
        url_group_changes_update: '/directory/group_changes/update/', // Изменение в бд подмен
        url_group_changes_filter: '/directory/group_changes/filter/', // Фильтрация подмен в модальном окне
        url_edit_group_change_list: '/directory/group_changes/edit-list/', // Список подмен в модальном окне
        url_group_changes_list: '/directory/group_changes/list/', // Поиск подмен для исключения
        url_group_changes_start: '/directory/group_changes/', // Запуск массовых подмен
        group_changes_input: '', //Форма поиска подмен для исключения
        group_change_status: false, // Показывать выпадающий список
        changes_list: [], // Список подмен в выпадающем меню исключений
        exclude_list: [], // Список выбранных исключений
        edit_group_change_list: [], // Список всех подмен в модальном окне
        group_change_input: '', // Фильтр в модальном окне подмен
        group_search_input: '', // Фильтр в модальном окне подмен
        update_change: '', // редактирование подмены
        update_search: '', // редактирование подмены
        selected_group_change_pk: ''
    },
    methods: {
        exclude_group_changes(change_id, change_name){
            this.group_change_status = false
            this.exclude_list.push({
                id: change_id,
                change: change_name
            })
        },
        group_change_start(){
            preloader_app.show_preloading = true
            let request_params = {
                'number_competitor_id': number_competitor_app.selected_competitor,
                'exclude_list': JSON.stringify(this.exclude_list),
            }
            axios.get(this.url_group_changes_start, {params: request_params})
                .then(function (response) {
                    access_message()
                }).catch(function (error) {
                    modal_error_app.error = error
                    error_message()
                }).then(function(){
                    preloader_app.show_preloading = false
                });
        },
        group_change_reset(){
            this.exclude_list = []
            this.group_changes_input = ''
            this.group_change_status = false
        },
        edit_group_change_load(){
            axios.get(this.url_edit_group_change_list)
                .then(function (response) {
                    group_changes_app.edit_group_change_list = JSON.parse(response.data.group_changes_list)
                }).catch(function (error) {
                modal_error_app.error = error
                error_message()
            });
        },
        update_group_change(change, search){
            let request_params = {
                'pk': this.selected_group_change_pk,
                'change': change,
                'search': search
            }
            axios.post(this.url_group_changes_update, {data: request_params})
                .then(function (response){
                    console.log(response)
                }).catch(function (error){
                modal_error_app.error = error
                error_message()
            });
        },
        select_group_change(change){
            this.selected_group_change_pk = change.pk
            this.update_change = change.change
            this.update_search = change.search
        }
    },
    mounted(){
        let modal_edit_group_changes = document.getElementById('edit-group-changes-modal');
        let instance_modal_group_changes = M.Modal.init(modal_edit_group_changes);
        M.Modal.init(document.getElementById('edit-group-change-line-modal'));
        this.edit_group_change_load()
    },
    computed:{
        filter_edit_changes: function (){
            let request_params = {
                'group_change_input': this.group_change_input,
                'group_search_input': this.group_search_input,
            }
            axios.get(this.url_group_changes_filter, {params: request_params})
                .then(function (response) {
                    group_changes_app.edit_group_change_list = JSON.parse(response.data.group_changes_list)
                }).catch(function (error) {
                modal_error_app.error = error
                error_message()
            });
        },
    },
    watch:{
        filter_edit_changes: function (){},
        group_changes_input: function (){
            if(this.group_changes_input.length > 0 || this.group_change_status){
                let request_params = {
                    'group_changes_input': this.group_changes_input,
                }
                axios.get(this.url_group_changes_list, {params: request_params})
                    .then(function (response) {
                        group_changes_app.changes_list = JSON.parse(response.data.group_changes_list)

                    }).catch(function (error) {
                        modal_error_app.error = error
                        error_message()
                    });
                this.group_change_status = true
            }
        },
    }
})