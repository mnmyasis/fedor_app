final_filters_app = new Vue({
    delimiters: ['{(', ')}'],
    el: '#final-filters-app', //работает в файле final_filters.html
    data: {
        url:'/matching/final-filters/',
        statuses: [],
        sku_form: '',
        eas_form: ''
    },
    methods:{
        clear_filter(){
            this.statuses = []
            this.sku_form = ''
            this.eas_form = ''
            let filter_status_form = document.querySelector(".filters-statuses-form")
            filter_status_form.querySelector(".select-dropdown").value='Мэтчинг Статус'
            this.$get_matching_lines() // manual_matching/final_matching_apps.js выгрузка без фильтров

        },

        filter(){
            if(this.statuses.length > 0 || this.sku_form || this.eas_form){
                let request_params = {
                    'number_competitor_id': JSON.stringify(number_competitor_app.selected_competitor),
                    'statuses': JSON.stringify(this.statuses),
                    'sku_form': this.sku_form,
                    'eas_form': this.eas_form
                }
                axios.get(this.url, {params: request_params})
                    .then(function (response){
                        final_matching_app.matching_data = (JSON.parse(response.data.matching))
                    }).catch(function (error){
                        error_message(error)
                    });
            }
        },

    },
    mounted(){
        let filter_final_select = document.getElementById('filter-final-select');
        let select_instance = M.FormSelect.init(filter_final_select);
    },
    watch:{
        statuses: function(){
            this.filter()
        },
        sku_form: function(){
            this.filter()
        },
        eas_form: function(){
            this.filter()
        }
    }

})