
function sel(){
    cookie_value = document.cookie.replace(/(?:(?:^|.*;\s*)fedor_competitor\s*\=\s*([^;]*).*$)|^.*$/, "$1")
    if(cookie_value){
        return cookie_value
    }else{
        return 0
    }
}

number_competitor_app = new Vue({
    delimiters: ['{(', ')}'],
    el: '#number-competitor-app',
    data: {
        url: '/directory/number-competitor-list/?format=json',
        number_competitors : [], // Список клиентских справочников
        selected_competitor: sel()
    },
    methods:{
        refresh_load_data(){
            document.cookie = "fedor_competitor="+ this.selected_competitor +"; path=/";
            if(typeof(final_matching_app) != 'undefined'){
                this.$get_matching_lines()
            }
            if(typeof(manual_matching_app) != 'undefined'){
                this.$load_sku_list()
            }
            if(typeof(auto_matching_app) != 'undefined'){
                auto_matching_app.new_sku_status = false
            }
        },
    },
    mounted(){
        axios.get(this.url).then(response => this.number_competitors = (JSON.parse(response.data.number_competitors)))
    },
    updated(){
        let select_competitor = document.querySelector('.sel-competitor');
        M.FormSelect.init(select_competitor);
    }
})



