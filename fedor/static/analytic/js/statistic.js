/* Накопления по статусам мэтчинга */
/* Измененные статусы пользователем */
Vue.component('line-bar-status-matching', {
    extends: VueChartJs.Bar,
    props: ['statistic'],
    methods:{
      draw_statistic(){
          this.renderChart({
              labels: ['В обработке', 'Ручная', 'Не найдено', 'Предложено добавить', 'Штрих-код', 'Штрих-код проверка', 'Алгоритм', 'Прочее'],
              datasets: this.statistic
          }, {responsive: true, maintainAspectRatio: false})
      },

    },

    watch:{
        statistic: function (){
            this.draw_statistic()
        }
    },
    mounted () {
        this.draw_statistic()
    }
})

Vue.component('line-bar-user-status-matching', {
    extends: VueChartJs.Bar,
    props: ['statistic'],
    methods:{
      draw_statistic(){
          this.renderChart({
              labels: ['Ручная', 'Не найдено', 'Предложено добавить', 'Штрих-код', 'Штрих-код проверка', 'Алгоритм', 'Прочее'],
              datasets: this.statistic
          }, {responsive: true, maintainAspectRatio: false})
      },

    },

    watch:{
        statistic: function (){
            this.draw_statistic()
        }
    },
    mounted () {
        this.draw_statistic()
    }
})

/* Рейтинг пользователей */
Vue.component('bar-user-rating', {
    extends: VueChartJs.Bar,
    props: ['statistic'],
    methods:{
        draw_statistic(){
            this.renderChart(
                this.statistic
            , {responsive: true, maintainAspectRatio: false})
        },

    },

    watch:{
        statistic: function (){
            this.draw_statistic()
        }
    },
    mounted () {
        this.draw_statistic()
    }
})

/* Виды изменения статусов */
/*Vue.component('line-status-changes', {
    extends: VueChartJs.Line,
    props: ['statistic'],
    methods:{
        draw_statistic(){
            this.renderChart(this.statistic, {responsive: true, maintainAspectRatio: false})
        },

    },
    watch:{
        statistic: function (){
            this.draw_statistic()
        }
    },
    mounted() {
        this.draw_statistic()
    }
})*/

/* Необработанные */
Vue.component('bar-raw-sku', {
    extends: VueChartJs.Bar,
    props: ['statistic'],
    methods:{
        draw_statistic(){
            this.renderChart(
                this.statistic
                , {responsive: true, maintainAspectRatio: false})
        },

    },

    watch:{
        statistic: function (){
            this.draw_statistic()
        }
    },
    mounted () {
        this.draw_statistic()
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
    return col;
}

analytic = new Vue({
    el: '#analytic-graph',
    data:{
        url_raw_sku_all_number_competitor: '/analytic/raw-sku-all-number-competitor/',
        url_user_rating: '/analytic/user-rating/',
        url_user_status_changes: '/analytic/user-status-changes/',
        url_status_changes: '/analytic/status-changes/',
        url_status_matchings: '/analytic/status-matchings/',
        start_date: '',
        end_date: '',
        datasets_status_mathing: [],
        datasets_status_change: [],
        data_collection_status_change: {},
        data_collection_user_rating: {},
        data_collection_raw_sku: {},


    },
    methods:{
        /* Накопления по статусам мэтчинга */
       status_matchings(){
            this.datasets_status_mathing = []
            let request_params = {
                'start_date': this.start_date,
                'end_date': this.end_date
            }
            axios.get(this.url_status_matchings, {params: request_params})
                .then(function (response){
                    let stats = response.data.stats
                    for(let i = 0; i < stats.length; i++){
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
                                stats[i].values.algoritm,
                                stats[i].values.other
                             ]
                        }


                        analytic.datasets_status_mathing.push(dataset)
                    }

                }).catch(function (error){
                modal_error_app.error_message(error)
            });
        },

        /* Виды изменения статусов */
        /*status_changes(){
            let request_params = {
                'start_date': this.start_date,
                'end_date': this.end_date,
                'number_competitor': JSON.stringify(number_competitor_app.sel_comp())
            }
            axios.get(this.url_status_changes, {params: request_params})
                .then(function (response){
                    let stats = response.data.stats
                    let labels = []
                    let data_progress = []
                    let data_manual = []
                    let data_not_found = []
                    let data_add_eas = []
                    let data_barcode = []
                    let data_barcode_chek = []
                    let data_other = []
                    let data_algoritm = []
                    for(let i = 0; i < stats.length; i++){
                        labels.push(stats[i].date)
                        data_progress.push(stats[i].statistic.progress)
                        data_manual.push(stats[i].statistic.manual)
                        data_not_found.push(stats[i].statistic.not_found)
                        data_add_eas.push(stats[i].statistic.add_eas)
                        data_barcode.push(stats[i].statistic.barcode)
                        data_barcode_chek.push(stats[i].statistic.barcode_check)
                        data_other.push(stats[i].statistic.other)
                        data_algoritm.push(stats[i].statistic.algoritm)
                    }
                    let datasets = [
                        {
                            label: 'В обработке',
                            backgroundColor: "transparent",
                            borderColor: '#1fd191',
                            data: data_progress
                        },
                        {
                            label: 'Ручная',
                            backgroundColor: "transparent",
                            borderColor: '#d34767',
                            data: data_manual
                        },
                        {
                            label: 'Не найдено',
                            backgroundColor: "transparent",
                            borderColor: '#e9d3b0',
                            data: data_not_found
                        },
                        {
                            label: 'Предложено добавить',
                            backgroundColor: "transparent",
                            borderColor: '#bf8c1d',
                            data: data_add_eas
                        },
                        {
                            label: 'Штрих-код',
                            backgroundColor: "transparent",
                            borderColor: '#ffe21d',
                            data: data_barcode
                        },
                        {
                            label: 'Штрих-код проверка',
                            backgroundColor: "transparent",
                            borderColor: '#d870ef',
                            data: data_barcode_chek
                        },
                        {
                            label: 'Алгоритм',
                            backgroundColor: "transparent",
                            borderColor: '#909af4',
                            data: data_algoritm
                        },
                        {
                            label: 'Прочее',
                            backgroundColor: "transparent",
                            borderColor: '#ac9995',
                            data: data_other
                        },

                    ]
                    analytic.data_collection_status_change = {
                        labels: labels,
                        datasets: datasets
                    }

                }).catch(function (error){
                modal_error_app.error_message(error)
            });
        },*/

        /* Измененные статусы пользователем */
        user_status_changes(){
            this.datasets_status_change = []
            let request_params = {
                'start_date': this.start_date,
                'end_date': this.end_date,
                //'number_competitor': number_competitor_app.sel_comp()
            }
            axios.get(this.url_user_status_changes, {params: request_params})
                .then(function (response){
                    let stats = response.data.stats
                    for(let i = 0; i < stats.length; i++){
                        let dataset = {
                            label: stats[i].user,
                            backgroundColor: random_color(),

                            data: [
                                //stats[i].statistic.progress,
                                stats[i].statistic.manual,
                                stats[i].statistic.not_found,
                                stats[i].statistic.add_eas,
                                stats[i].statistic.barcode_not_check,
                                stats[i].statistic.barcode_check,
                                stats[i].statistic.algoritm,
                                stats[i].statistic.other

                            ]
                        }
                        analytic.datasets_status_change.push(dataset)
                    }

                }).catch(function (error){
                modal_error_app.error_message(error)
            });
        },

        /* Рейтинг пользователей */
        user_rating(){
            let request_params = {
                'start_date': this.start_date,
                'end_date': this.end_date,
                //'number_competitor': number_competitor_app.sel_comp()
            }
            axios.get(this.url_user_rating, {params: request_params})
                .then(function (response){
                    let stats = response.data.stats
                    let labels = []
                    let data = []
                    for(let i = 0; i < stats.length; i++){
                        labels.push(stats[i].user)
                        data.push(stats[i].count)
                    }
                    analytic.data_collection_user_rating = {
                        labels: labels,
                        datasets: [
                            {
                                label: 'Рейтинг',
                                backgroundColor: '#e14550',
                                maxBarThickness: 80,
                                minBarLength: 20,
                                data: data
                            }
                        ]
                    }

                }).catch(function (error){
                modal_error_app.error_message(error)
            });
        },

        /* Необработанные */
        raw_sku(){
            let request_params = {
                'start_date': this.start_date,
                'end_date': this.end_date,
            }
            axios.get(this.url_raw_sku_all_number_competitor, {params: request_params})
                .then(function (response){
                    let stats = response.data.stats
                    let labels = []
                    let data = []
                    for(let i = 0; i < stats.length; i++){
                        labels.push(stats[i].number_competitor)
                        data.push(stats[i].raw_count)
                    }
                    analytic.data_collection_raw_sku = {
                        labels: labels,
                        datasets: [
                            {
                                label: 'Необработанные',
                                backgroundColor: '#e15a00',
                                maxBarThickness: 80,
                                minBarLength: 20,
                                data: data
                            }
                        ]
                    }

                }).catch(function (error){
                modal_error_app.error_message(error)
            });
        }
    },
    mounted() {
        this.start_date='2020-12-1'
        this.end_date='2020-12-16'
        let tabs = document.querySelector('.tabs');
        M.Tabs.init(tabs);
        let datepicker = document.querySelectorAll('.datepicker');
        let options = {
            default: 'now',
            autoClose: true,
            format: 'yyyy-mm-dd'
        }
        M.Datepicker.init(datepicker, options);

    }
})
