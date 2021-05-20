axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
task_status_app = new Vue({
    delimiters: ['{(', ')}'],
    el: '#task-status-app',
    data: {
        url_task_list: '/admin/task-user/list/',
        tasks: []
    },
    methods:{
        load_status_tasks(){
            axios.get(this.url_task_list,{})
            .then(function (response) {
                task_status_app.tasks = JSON.parse(response.data)
                setTimeout(function() {
                  task_status_app.load_status_tasks();
                }, 1000);
            }).catch(function (error) {
                error_message(error)
            });
        }
    },

    created: function(){
        this.load_status_tasks()
    },

    mounted(){
    },
})