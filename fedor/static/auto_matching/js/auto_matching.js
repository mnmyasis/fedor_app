axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

auto_matching_app = new Vue({
    el: '#auto_matching_app',
    delimiters: ['{(', ')}'],
    data: {
        url_new_sku: '/directory/new-sku/',
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
                modal_error_app.error = error
                error_message()
            }).then(function(){
                preloader_app.show_preloading = false

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
            let request_params = {
                'number_competitor_id' : number_competitor_app.selected_competitor,
            }
            axios.get(this.url_new_sku, {params: request_params})
                .then(function (response){
                    auto_matching_app.new_sku_dates = JSON.parse(response.data.date_create_new_sku)

                });
        },
        new_sku_dates: function (){

        }
    }
})