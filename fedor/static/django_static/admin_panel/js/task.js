axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';

task_add_app = new Vue({
    delimiters: ['{(', ')}'],
    el: '#task-add-app',
    data: {
        url_competitors: '/directory/number-competitor-list/?format=json',
        url_new_sku: '/directory/new-sku/',
        url_add_task_algoritm: '/admin/task/add/algoritm/',
        url_schedule_list: '/admin/schedule/list/',
        new_sku: '',
        new_sku_dates: [],
        action: false,
        barcode_match: false,
        new_sku_status: '',
        name: '',
        description: '',
        schedule_list: [],
        task_status: true,
        one_task_status: false,
        selected_task: 0,
        selected_crontab: '',
        selected_competitor: 1,
        number_competitors: []
    },
    methods: {
        create_task_algoritm(){
            console.log(this.selected_task)
            console.log(this.name)
            console.log(this.selected_crontab)
            console.log(this.selected_competitor)
            if(this.selected_task != 0 && this.name && this.selected_crontab && this.selected_competitor){
                let request_params = {
                    'number_competitor_id' : JSON.stringify(number_competitor_app.sel_comp()),
                    'name': this.name,
                    'description': this.description,
                    'crontab': this.selected_crontab,
                    'new_sku': this.new_sku,
                    'action': this.action,
                    'barcode_match': this.barcode_match,
                    'task_status': this.task_status,
                    'one_task_status': this.one_task_status,
                    'selected_task': this.selected_task
                }
                axios.post(this.url_add_task_algoritm, {data: request_params})
                    .then(function (response){
                       console.log(response.data)
                       if(response.data==true){
                            document.location.href = "/admin/task/schedule-list/"
                       }

                    }).catch(error => {
                        error_message(error)
                    });
            }else{
                error_message('Не заполнены необходимые поля')
            }
        },
        create_task_sync_directory(){
            if(this.selected_task != 0 && this.name && this.selected_crontab){
                let request_params = {
                    'name': this.name,
                    'description': this.description,
                    'crontab': this.selected_crontab,
                    'task_status': this.task_status,
                    'one_task_status': this.one_task_status,
                    'selected_task': this.selected_task
                }
                axios.post(this.url_add_task_algoritm, {data: request_params})
                    .then(function (response){
                       console.log(response.data)
                       if(response.data==true){
                            document.location.href = "/admin/task/schedule-list/"
                       }

                    }).catch(error => {
                        error_message(error)
                    });
            }else{
                error_message('Не заполнены необходимые поля')
            }
        }
    },
    updated(){

        let sel_crontab = document.querySelector('.sel-crontab');
        M.FormSelect.init(sel_crontab);
        let form_sel = document.querySelector('.select-new-sku');
        M.FormSelect.init(form_sel);
        /*let select_competitor = document.querySelector('.sel-competitor');
        M.FormSelect.init(select_competitor);*/
    },
    mounted(){
        let sel_task = document.querySelectorAll('.select-task');
        M.FormSelect.init(sel_task);
        axios.get(this.url_competitors).then(response => this.number_competitors = (JSON.parse(response.data.number_competitors)))
        axios.get(this.url_schedule_list).then(response => this.schedule_list = (JSON.parse(response.data)))
    },
    watch:{
        new_sku_status: function (){
            if(this.new_sku_status == true){
                /*let request_params = {
                    'number_competitor_id' : this.selected_competitor,
                }*/
                let request_params = {
                    'number_competitor_id' : JSON.stringify(number_competitor_app.sel_comp()),
                }
                axios.get(this.url_new_sku, {params: request_params})
                    .then(function (response){
                        task_add_app.new_sku_dates = JSON.parse(response.data.date_create_new_sku)

                    }).catch(error => {
                        error_message(error)
                    });
            }else{
                this.new_sku = ''
            }
        },
    }
})