axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

joint_app = new Vue({
    el: '#auto_matching_app',
    delimiters: ['{(', ')}'],
    data: {
        url_auto_matching: '/auto/matching/algoritm/'
    },
    methods: {
        send_data_on_joint(){
            preloader_app.show_preloading = true
            axios.post(this.url_auto_matching, {
                data: {
                    number_competitor_id: this.$number_competitor
                },
            }).then(function (response){
                access_message()
            }).catch(error => {
                modal_error_app.error = error
                error_message()
            }).then(function(){
                preloader_app.show_preloading = false

            })
        }
    },
    mounted(){
        let form_sel = document.querySelector('select');
        M.FormSelect.init(form_sel);
    }
})