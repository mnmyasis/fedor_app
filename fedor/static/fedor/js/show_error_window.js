function error_message(){
    if(modal_error_app.error.response.status == '403'){
      let next = window.location.href
      document.location.href = "/auth/login/?next=" + next
      return;
    }
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
            if(modal_error_app.error.response.status == '403'){
                let next = window.location.href
                document.location.href = "/auth/login/?next=" + next
                return;
            }
            let modal_error = document.getElementById('error-modal');
            let instance = M.Modal.init(modal_error);
            instance.open()
        }
    }
})