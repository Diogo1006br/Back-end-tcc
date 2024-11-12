from django.urls import resolve

class CookieTokenMiddleware:
    """
    Middleware to handle JWT authentication through cookies
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        url_name = resolve(request.path_info).url_name
        if url_name == 'token_obtain_pair' or url_name == 'is_authenticated':  # substitua 'obtain-token' pelo nome da URL da sua view ObtainTokenView
            return self.get_response(request)

        # Extract token from cookie and add to the header
        token = request.COOKIES.get('access_token')
        if token:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'

        response = self.get_response(request)

        return response