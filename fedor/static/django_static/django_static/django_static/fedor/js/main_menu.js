main_menu_app = new Vue({
    el: '#main_menu_app',
    methods:{
        show_menu(e){
            let main_menu = document.querySelector('.sidenav');
            M.Sidenav.init(main_menu);
        }
    }
})