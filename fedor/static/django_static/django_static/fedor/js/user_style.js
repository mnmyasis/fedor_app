user_style_app = new Vue({
    delimiters: ['{(', ')}'],
    el: '#user-style',
    data: {
        font_size: ''
    },
    methods:{
        style_change(){
            let cookie_value = document.cookie.replace(/(?:(?:^|.*;\s*)user_style\s*\=\s*([^;]*).*$)|^.*$/, "$1");
            if(cookie_value){
                if(cookie_value == 'dark'){
                   document.cookie = "user_style=lighten; path=/";
                }else{
                    document.cookie = "user_style=dark; path=/";
                }
            }else{
                document.cookie = "user_style=dark; path=/";
            }
            location.reload()
        },
        reset_font_size(){
           let cookie_date = new Date ( );  // Текущая дата и время
           cookie_date.setTime ( cookie_date.getTime() - 1 );
           document.cookie = "fedor_font_size=; expires=" + cookie_date.toGMTString();
           location.reload()
        }
    },
    created: function(){
        let cookie_font_size = document.cookie.replace(/(?:(?:^|.*;\s*)fedor_font_size\s*\=\s*([^;]*).*$)|^.*$/, "$1");
        if(cookie_font_size){
            this.font_size = cookie_font_size
            let fedor_items = document.querySelectorAll('.fedor-item')
            for(let i = 0; i < fedor_items.length; i++){
                fedor_items[i].style.fontSize = cookie_font_size;
            }
        }
    },
    watch: {
        font_size: function(){
            console.log(document.querySelectorAll('.fedor-item'))
            let fedor_items = document.querySelectorAll('.fedor-item')
            for(let i = 0; i < fedor_items.length; i++){
                fedor_items[i].style.fontSize = this.font_size + 'px';
            }
            let size = this.font_size + 'px';
            document.cookie = "fedor_font_size=" + size + '; path=/; SameSite=None; Secure';
        }
    },
    mounted(){
        let fixed = document.querySelector('.fixed-action-btn');
        M.FloatingActionButton.init(fixed);
    },
})