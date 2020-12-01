final_filters_app = new Vue({
    delimiters: ['{(', ')}'],
    el: '#final-filters-app', //работает в файле final_filters.html
    data: {
        url:'/matching/filters-statuses/',
        statuses: [],
    },
    methods:{
        clear_filter(){
            this.statuses = []
            let filter_status_form = document.querySelector(".filters-statuses-form")
            filter_status_form.querySelector(".select-dropdown").value='Мэтчинг Статус'
            this.$get_matching_lines() // manual_matching/final_matching_apps.js выгрузка без фильтров

        }
    },
    mounted(){
        let filter_final_select = document.getElementById('filter-final-select');
        let select_instance = M.FormSelect.init(filter_final_select);
    },
    watch:{
        statuses: function (){
            if(this.statuses.length > 0){
                let request_params = {
                    'number_competitor_id': number_competitor_app.selected_competitor,
                    'statuses': JSON.stringify(this.statuses)
                }
                axios.get(this.url, {params: request_params})
                    .then(function (response){
                        final_matching_app.matching_data = (JSON.parse(response.data.matching))
                    }).catch(function (error){
                        modal_error_app.error = error
                        error_message()
                    });
            }
        }
    }

})