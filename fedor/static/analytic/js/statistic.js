Vue.component('line-chart', {
    extends: VueChartJs.Bar,
    mounted () {
        this.renderChart({
            labels: ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
            datasets: [
                {
                    label: 'Коммиты на GitHub',
                    backgroundColor: '#f87979',
                    data: [40, 20, 12, 39, 10, 40, 39, 80, 40, 20, 12, 11]
                }
            ]
        }, {responsive: true, maintainAspectRatio: false})
    }
})

app = new Vue({
    el: '#test',
    data:{
        url_status_mathings: '/analytic/status-matchings/'
    },
    methods:{
        status_matchings(){
            axios.get(url, {params: request_params})
                .then(function (response){
                    manual_matching_app.eas = JSON.parse(response.data.eas)
                }).catch(function (error){
                modal_error_app.error = error
                error_message()
            });
        }
    },
    mounted() {
        let tabs = document.querySelector('.tabs');
        M.Tabs.init(tabs);
    }
})
