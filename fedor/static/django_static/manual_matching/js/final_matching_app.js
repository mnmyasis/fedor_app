Vue.prototype.$get_matching_lines = function(){
    //Стартовая выгрузка записей в таблицу
    //final_filters_app.clear_filter()
    /*let filter_value = final_filters_app.statuses // Если были выбраны статусы
    if(filter_value.length > 0){
        final_filters_app.filter()
        return;
    }*/
    if(final_filters_app.statuses.length > 0 || final_filters_app.sku_form.length > 0 || final_filters_app.eas_form.length > 0){
        final_filters_app.filter()
        return;
    }
    let request_params = {
    'number_competitor_id' : manual_matching_app.match_competitor_id,
    'sku_id': manual_matching_app.match_sku_id
    }
    let url = '/matching/final-matching/page/get/?format=json'
    axios.get(url, {params: request_params})
        .then(function (response){
            final_matching_app.matching_data = JSON.parse(response.data.matching)
        }).catch(function (error){
            error_message(error)
        });
}

final_matching_app = new Vue({
    delimiters: ['{(', ')}'],
    el: '#final-matching-app',
    data: {
        delete_matching_url: '/matching/final-matching/delete/',
        filter_for_eas: '/matching/filters-by-tn_fv/?format=json',
        matching_data: null, //Данные мэтчинга для главной таблицы

    },
    methods: {
        delete_matching(id_sku, competitor){
            let request_params = {
                'number_competitor_id' : competitor,
                'sku_id': id_sku,
            }
            axios.post(this.delete_matching_url, {data: request_params})
                .then(function (response){
                    final_matching_app.$get_matching_lines()
                }).catch(function (error){
                    error_message(error)
                });
        }
    },
    mounted(){
        /* Стартовая выгрузка данных мэтчинга */
        let final_tab = document.querySelector('.final');

        final_tab.onclick = function(){
            final_matching_app.$get_matching_lines()
        }

    }
})