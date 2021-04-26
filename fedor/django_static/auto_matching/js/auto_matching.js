axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

auto_matching_app = new Vue({
    el: '#auto_matching_app',
    delimiters: ['{(', ')}'],
    data: {
        url_new_sku: '/directory/new-sku/',
        url_start_matching_worker: '/auto/matching/create-work-algoritm/',
        url_auto_matching: '/auto/matching/algoritm/',
        action: false, // Акция
        barcode_match: false, // Доверие ШК
        new_sku_status: false,
        new_sku: '', // Новая номенклатура
        new_sku_dates:  '', // Даты добавления номенклатуры
    },
    methods: {
        start_matching(){
            console.log(this.action)
            console.log(this.barcode_match)
            console.log(this.new_sku)
            console.log(number_competitor_app.selected_competitor)

            preloader_app.show_preloading = true
            axios.post(this.url_auto_matching, {
                data: {
                    number_competitor_id: number_competitor_app.selected_competitor,
                    action: this.action,
                    barcode_match: this.barcode_match,
                    new_sku: this.new_sku
                },
            }).then(function (response){
                access_message()
            }).catch(error => {
                error_message(error)
            }).then(function(){
                preloader_app.show_preloading = false

            })
        },

        start_worker_matching(){
            console.log(this.action)
            console.log(this.barcode_match)
            console.log(this.new_sku)
            console.log(number_competitor_app.selected_competitor)

            axios.post(this.url_start_matching_worker, {
                data: {
                    number_competitor_id: number_competitor_app.selected_competitor,
                    action: this.action,
                    barcode_match: this.barcode_match,
                    new_sku: this.new_sku,
                },
            }).then(function (response){
                access_message()
            }).catch(error => {
                error_message(error)
            }).then(function(){
            })
        }

    },
   mounted(){
    },
    updated(){
        let form_sel = document.querySelector('.select-new-sku');
        M.FormSelect.init(form_sel);
    },
    watch:{
        new_sku_status: function (){
            if(this.new_sku_status == true){
                let request_params = {
                    'number_competitor_id' : number_competitor_app.selected_competitor,
                }
                axios.get(this.url_new_sku, {params: request_params})
                    .then(function (response){
                        auto_matching_app.new_sku_dates = JSON.parse(response.data.date_create_new_sku)

                    }).catch(error => {
                        error_message(error)
                    });
            }else{
                this.new_sku = ''
            }
        },
    }
})