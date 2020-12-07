group_changes_app = new Vue({
    el: '#group_changes_app',
    delimiters: ['{(', ')}'],
    data: {
        url_group_changes_list: '/directory/group_changes/list/',
        url_group_changes_start: '/directory/group_changes/',
        group_changes_input: '',
        group_change_status: false,
        changes_list: [],
        exclude_list: []
    },
    methods: {
        exclude_group_changes(change_id, change_name){
            this.group_change_status = false
            this.exclude_list.push({
                id: change_id,
                change: change_name
            })
            console.log(this.exclude_list)
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
        }
    },
    watch:{
        group_changes_input: function (){
            let request_params = {
                'group_changes_input': this.group_changes_input,
            }
            axios.get(this.url_group_changes_list, {params: request_params})
                .then(function (response) {
                    group_changes_app.changes_list = JSON.parse(response.data.group_changes_list)
                    console.log(group_changes_app.changes_list)
                }).catch(function (error) {
                    modal_error_app.error = error
                    error_message()
                });
            this.group_change_status = true
        }
    }
})