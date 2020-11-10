class FilterRequest extends PatternRequest{
    get_params() {
        return {
            'tn_fv': filters_app.tn_fv,
            'number_competitor_id': filters_app.number_competitor,
            'sku_id': manual_matching_app.active_sku
        }
    }

    response_access(response) {
        super.response_access(response);
    }
}

filters_app = new Vue({
    delimiters: ['{(', ')}'],
    el: '#filters-app',
    data: {
        tn_fv: '',
        url: '/matching/filters-matching/?format=json',
        number_competitor: 1
    },
    methods:{
        manufacturer(){
            console.log(this.tn_fv)
            filter_request = new FilterRequest()
            request = new Request(filter_request)
            request.business_logic(this.url, 'get')
        }
    }
})