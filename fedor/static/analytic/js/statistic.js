Vue.component('line-bar-status-matching', {
    extends: VueChartJs.Bar,
    props: ['statistic'],
    methods:{
      drow_statistic(){
          this.renderChart({
              labels: ['В обработке', 'Ручная', 'Не найдено', 'Предложено добавить', 'Штрих код', 'штрих код проверка', 'Прочее'],
              datasets: [
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
              ]
          }, {responsive: true, maintainAspectRatio: false})
      }
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
        in_progress: 0

    },
    methods:{
        status_matchings(){
            let request_params = {
                'start_date': this.start_date,
                'end_date': this.end_date
            }
            console.log(request_params)
            axios.get(this.url_status_matchings, {params: request_params})
                .then(function (response){
                    console.log(response)

                    analytic.status_matchs = {
                        progress: response.data.progress,
                        manual: response.data.manual,
                        not_found: response.data.not_found,
                        other: response.data.other,
                        add_eas: response.data.add_eas,
                        barcode_check: response.data.barcode_check,
                        barcode: response.data.barcode
                    }

                    console.log(analytic.status_matchs)
                    //analytic.status_matchs = JSON.parse(response.data)
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
            format: 'yyyy/mm/dd'
        }
        M.Datepicker.init(datepicker, options);
        //this.status_matchings()
    }
})
