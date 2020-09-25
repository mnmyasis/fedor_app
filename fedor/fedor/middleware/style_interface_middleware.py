import logging


class ChangeStyleInterface:
    logger = logging.getLogger(__name__)

    def __set_cookie_color(self, response, element, css_class):
        response.set_cookie(element, css_class)
        return response

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)
        is_dark = request.COOKIES.get('is_dark')
        self.logger.info(is_dark)
        if is_dark:
            styles = [
                {'element': 'color', 'color': 'blue-grey darken-4'},
                {'element': 'body', 'color': 'blue-grey darken-4'}
            ]
        else:
            styles = [
                {'element': 'color', 'color': 'darken-4'},
                {'element': 'body', 'color': ''}
            ]
        for value in styles:
            response = self.__set_cookie_color(response, value['element'], value['color'])
        return response
