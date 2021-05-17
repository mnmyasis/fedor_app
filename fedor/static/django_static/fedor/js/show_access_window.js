function access_message(){
    let modal_access = document.getElementById('access_window');
    let instance = M.Modal.init(modal_access);
    instance.open()
}

modal_access_app = new Vue({
    delimiters: ['{(', ')}'],
    el: '#access_window',
    data: {
        'access': '',
    },
    methods: {
        access_message(message){
            this.access = message
            let modal_access = document.getElementById('access_window');
            let instance = M.Modal.init(modal_access);
            instance.open()
        }
    }
})