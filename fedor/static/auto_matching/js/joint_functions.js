Vue.component('test-j',{
    template: '<h6>TEST</h6>'
})

var joint_app = new Vue({
    el: '#joint-app',
    delimiters: ['{(', ')}'],
    data: {
        error: null,
    },
    methods: {
        send_data_on_joint(e){
            this.error = null
            console.log('Отправляю данные на стыковку')
            preloader_app.show_preloading = true
            axios.defaults.xsrfCookieName = 'csrftoken'
            axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
            axios.post('/auto/matching/algoritm/', {
                data: {
                    number_competitor_id: 1
                },
            }).then(function (response){
                console.log(response)
                if(this.error == null){
                    access_message()
                }
            }).catch(error => {
                this.error = error
                //console.log(error)
                /* запуск окна с ошибкой */
                error_message()
            }).then(function(){
                preloader_app.show_preloading = false

            })
        }
    }
})