var main_menu_app = new Vue({
    el: '#main_menu_app',
    methods:{
        show_menu(e){
            var instance = M.Sidenav.init($('.sidenav'));
        }
    }
})