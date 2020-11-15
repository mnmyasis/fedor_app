class StatusesFilterRequest extends PatternRequest{
    constructor(statuses, number_competitor) {
        super();
        this.statuses = statuses
        this.competitor = number_competitor
    }
    get_params() {
        return {
            'statuses_id': this.statuses,
            'number_competitor_id': this.competitor
        }
    }

    response_access(response) {
        final_matching_app.matching_data = JSON.parse(response.data.matching)
    }
}

final_filters_app = new Vue({
    delimiters: ['{(', ')}'],
    el: '#final-filters-app', //работает в файле final_filters.html
    data: {
        url:'',
        statuses: [],
    },
    methods:{
        statuses_filter(){
            console.log(this.statuses)
            statuses_filter_request = new StatusesFilterRequest(this.statuses, final_matching_app.number_competitor)
            request = new Request(statuses_filter_request)
            request.business_logic(this.url, 'get')
        },
        clear_filter(){
            this.statuses = []
            document.querySelector(".select-dropdown").value='Мэтчинг Статус'

        }
    },
    mounted(){
        var elems = document.querySelectorAll('select');
        var select_instance = M.FormSelect.init(elems);
    }
})