
function sel(){
    cookie_value = document.cookie.replace(/(?:(?:^|.*;\s*)fedor_competitor\s*\=\s*([^;]*).*$)|^.*$/, "$1")
    if(cookie_value){
        cookie_value = cookie_value.split(',')
        console.log(cookie_value)
        return cookie_value
    }else{
        return [0]
    }
}

function _filter(number_competitors){
    options = []
    for(i=0;i<number_competitors.length;i++){
        text = number_competitors[i].name
        id = number_competitors[i].pk
        options.push({
            id: id,
            text: text
        })
     }
     return options
}


Vue.component("select2", {
        delimiters: ['{(', ')}'],
        props: ["options", "value"],
        template: "#select2-template",
        mounted: function() {
          var vm = this;
          $(this.$el)
            // init select2
            .select2({ data: this.options })
            .val(this.value)
            .trigger("change")
            // emit event on change.
            .on("change", function() {
              vm.$emit("input", this.value);
            });
        },
        watch: {
          value: function(value) {
            // update value
            $(this.$el)
              .val(value)
              .trigger("change");
          },
          options: function(options) {
            // update options
            $(this.$el)
              .empty()
              .select2({ data: options });
          }
        },
        destroyed: function() {
          $(this.$el)
            .off()
            .select2("destroy");
        }
      });

number_competitor_app = new Vue({
    delimiters: ['{(', ')}'],
    el: '#number-competitor-app',
    template: "#demo-template",
    data: {
        url: '/directory/number-competitor-list/?format=json',
        number_competitors : [], // Список клиентских справочников
        selected_competitor: sel(),
        selected: 0,
        options: [],
        comps: [],
        all_selected: false,
    },
    methods:{
        refresh_load_data(){
            //document.cookie = "fedor_competitor="+ this.comps +"; path=/";
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
        sel_comp(){
        // Получить список справочников, вызывается из других приложений
            competitors_id = []
            for(i=0; i < this.comps.length; i++){
                competitors_id.push(this.comps[i].pk)
            }
            return competitors_id
        },
        del_chip(comp){
            this.comps = []
            this.all_selected = false
            this.selected = 0
        }
    },

    watch:{
        comps: function(){
            this.refresh_load_data()
        },
        selected: function(){
            for(i=0; i < this.options.length; i++){
                if(this.selected == this.options[i].id){
                    this.comps.push({name: this.options[i].text, pk: this.options[i].id})
                }
            }
        },
        all_selected: function(){
            console.log(this.all_selected)
            if(this.all_selected == true){
                all = []
                for(i=0; i < this.options.length; i++){
                    all.push({name: this.options[i].text, pk: this.options[i].id})
                }
                this.comps = all
            }else{
                this.comps = []
            }
        }
    },
    mounted(){
        //axios.get(this.url).then(response => this.number_competitors = (JSON.parse(response.data.number_competitors)))
        axios.get(this.url)
                .then(function (response){
                   number_competitor_app.number_competitors = JSON.parse(response.data.number_competitors)
                   /*for(i=0;i<number_competitor_app.number_competitors.length;i++){
                        text = number_competitor_app.number_competitors[i].name
                        id = number_competitor_app.number_competitors[i].pk
                        number_competitor_app.options.push({
                            id: id,
                            text: text
                        })
                     }*/
                     number_competitor_app.options = _filter(number_competitor_app.number_competitors)
                     number_competitor_app.selected = number_competitor_app.options[0].id
                 })

    },
    updated(){
        //let select_competitor = document.querySelector('.sel-competitor');
        //M.FormSelect.init(select_competitor);
    }
})



