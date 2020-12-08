function error_message(){
    let modal_error = document.getElementById('error-modal');
    let instance = M.Modal.init(modal_error);
    instance.open()
}


modal_error_app = new Vue({
    delimiters: ['{(', ')}'],
    el: '#error-modal',
    data: {
        'error': ''
    },
    methods:{
        error_message(message){
            this.error = message
            let modal_error = document.getElementById('error-modal');
            let instance = M.Modal.init(modal_error);
            instance.open()
        }
    }
})