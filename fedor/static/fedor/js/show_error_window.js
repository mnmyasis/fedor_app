function error_message(){
    var modal_error = document.getElementById('error-modal');
    var instance = M.Modal.init(modal_error);
    instance.open()
}

var modal_error_app = new Vue({
    delimiters: ['{(', ')}'],
    el: '#error-modal',
    data: {
        'error': ''
    },
})