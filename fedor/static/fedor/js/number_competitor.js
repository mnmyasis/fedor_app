class CompetitorRequest extends PatternRequest{

    response_access(response) {
        number_competitor_app.number_competitors = JSON.parse(response.data.number_competitors)
        console.log(JSON.parse(response.data.number_competitors))
    }
}

function get_number_competitor(){
    return number_competitor_app.select_number_competitor
}

let number_competitor_app = new Vue({
    delimiters: ['{(', ')}'],
    el: '#number-competitor-app',
    data: {
        url: '/directory/number-competitor-list/?format=json',
        number_competitors : [], // Список клиентских справочников
        select_number_competitor: 1, // Выбранный клиентский справочник
    },
    methods:{
        refresh_load_data(){
            if(typeof(final_matching_app) != 'undefined'){
                get_matching_lines()
            }
            if(typeof(manual_matching_app) != 'undefined'){
                load_sku_list()
            }
        }
    },
    mounted(){
        let competitor_request = new Request(new CompetitorRequest())
        competitor_request.business_logic(this.url, 'get')
    },
    updated(){
        let select_competitor = document.querySelector('.sel-competitor');
        M.FormSelect.init(select_competitor);
    }
})



