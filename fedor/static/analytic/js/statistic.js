Vue.component('line-bar-status-matching', {
    extends: VueChartJs.Bar,
    props: ['statistic'],
    methods:{
      drow_statistic(){
          this.renderChart({
              labels: ['В обработке', 'Ручная', 'Не найдено', 'Предложено добавить', 'Штрих код', 'Штрих код проверка', 'Прочее'],
              /*datasets: [
                  {
                      label: 'Наколпдения по статусам мэтчинга',
                      backgroundColor: '#f87979',
                      data: [
                          this.statistic.progress,
                          this.statistic.manual,
                          this.statistic.not_found,
                          this.statistic.add_eas,
                          this.statistic.barcode,
                          this.statistic.barcode_check,
                          this.statistic.other
                      ]
                  }
              ]*/
              datasets: this.statistic
          }, {responsive: true, maintainAspectRatio: false})
      },

    },

    watch:{
        statistic: function (){
            this.drow_statistic()
        }
    },
    mounted () {
        this.drow_statistic()
    }
})
function random_color(){
    let col = Math.round(255.0*Math.random());
    let r = col.toString(16);
    col = Math.round(255.0*Math.random());
    let g=col.toString(16);
    col = Math.round(255.0*Math.random());
    let d=col.toString(16);
    col= '#'+r+g+d;
    console.log(col)
    return col;
}

analytic = new Vue({
    el: '#test',
    data:{
        url_status_matchings: '/analytic/status-matchings/',
        status_matchs: {
            progress: 0,
            manual: 0,
            not_found: 0,
            other: 0,
            add_eas: 0,
            barcode_check: 0,
            barcode: 0
        },
        start_date: '',
        end_date: '',
        datasets: []

    },
    methods:{
        status_matchings(){
            this.datasets = []
            let request_params = {
                'start_date': this.start_date,
                'end_date': this.end_date
            }
            console.log(request_params)
            axios.get(this.url_status_matchings, {params: request_params})
                .then(function (response){
                    let stats = response.data.stats
                    for(let i = 0; i < stats.length; i++){
                        console.log(stats[i])
                        let dataset = {
                            label: stats[i].competitor_name,
                                backgroundColor: random_color(),
                            data: [
                                stats[i].values.progress,
                                stats[i].values.manual,
                                stats[i].values.not_found,
                                stats[i].values.add_eas,
                                stats[i].values.barcode,
                                stats[i].values.barcode_check,
                                stats[i].values.other
                             ]
                        }
                        analytic.datasets.push(dataset)
                    }

                }).catch(function (error){
                modal_error_app.error_message(error)
            });
        }
    },
    mounted() {
        let tabs = document.querySelector('.tabs');
        M.Tabs.init(tabs);
        let datepicker = document.querySelectorAll('.datepicker');
        let options = {
            default: 'now',
            autoClose: true,
            format: 'yyyy/mm/dd'
        }
        M.Datepicker.init(datepicker, options);
        this.start_date='2020/12/1'
        this.end_date='2020/12/16'
        this.status_matchings()
    }
})
