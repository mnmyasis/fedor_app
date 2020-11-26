class Request{
    constructor(request){
        this.request = request
    }

    set_request(request){
        this.request = request
    }

    get_request(){
        return this.request
    }

    start_preloader(){
        preloader_app.show_preloading = true
    }

    close_preloader(){
        preloader_app.show_preloading = false
    }

    business_logic(url, request_type, competitor=null){
        let result
        this.start_preloader()
        let request = this.get_request()
        if(request_type == 'get'){
            result = request.send_get_request(url)
        }else if(request_type == 'post'){
            result = request.send_post_request(url)
        }
        this.close_preloader()
        return result
    }

}

class PatternRequest{

    get_params(){
        //Вернуть ХЭШ параметров GET запроса
        return null
    }


    response_access(response){
        //Определить в дочернем классе логику после успешного GET запроса
    }

    response_error(error){
        console.log(error)
        modal_error_app.error = error //Сообщение об ошибке
        error_message()//запуск модального окна
    }

    resp_func1(){
        //Можно определить доп логику после POST запроса
    }

    resp_func2(){
        //Можно определить доп логику после POST запроса
    }


    send_get_request(url){
        axios.get(url,{
            params: this.get_params()
        }).then(response => {
            this.response_access(response)

        }).catch(error => {
            this.response_error(error)
        })

        this.resp_func1()
        this.resp_func2()
    }

    send_post_request(url){
        axios.defaults.xsrfCookieName = 'csrftoken'
        axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
        axios.post(url, {
            data: this.get_params()
        }).then(response => {
            this.response_access(response)
        }).catch(error => {
            this.response_error(error)
        })
        this.resp_func1()
        this.resp_func2()
    }
}