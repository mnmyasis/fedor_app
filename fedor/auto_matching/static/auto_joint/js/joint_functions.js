Vue.component('test-j',{
    template: '<h6>TEST</h6>'
})

var joint_app = new Vue({
    el: '#joint-app',
    delimiters: ['{(', ')}'],
    data: {

    },
    methods: {
        send_data_on_joint(e){
            console.log('Отправляю данные на стыковку')
        }
    }
})