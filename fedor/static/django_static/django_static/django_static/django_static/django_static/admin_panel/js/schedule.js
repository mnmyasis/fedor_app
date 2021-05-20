axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

schedule_app = new Vue({
    delimiters: ['{(', ')}'],
    el: '#schedule_app',
    data: {
        url_create_schedule: '/admin/schedule/add/',
        date: '',
        time: ''
    },
    methods: {
        create_schedule(){
            if(this.date || this.time){
                axios.post(this.url_create_schedule, {
                    data: {
                        date: this.date,
                        time: this.time,
                    },
                }).then(function (response){
                    if(response.data==true){
                        document.location.href = "/admin/schedule/list/"
                    }
                }).catch(error => {
                    error_message(error)
                })
            }else{
                error_message('Не указаны дата и время запуска.')
            }
        }
    },
    mounted(){
        let datepicker = document.querySelectorAll('.datepicker');
        options_date_picker = {
            default: 'now',
            autoClose: true,
            format: 'yyyy-mm-dd'
        }
        M.Datepicker.init(datepicker, options_date_picker);

        let timepicker = document.querySelectorAll('.timepicker');
        options = {
            autoClose: true,
            twelveHour: false
        }
        M.Timepicker.init(timepicker, options);
    }
})