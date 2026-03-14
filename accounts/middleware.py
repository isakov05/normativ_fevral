import datetime

class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR', 'Noma\'lum IP')
        now = datetime.datetime.now()
        path = request.path
        user = request.user


        with open("requests.log", "a", encoding="utf-8") as f:
            f.write(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}]\n")
            f.write(f"User: {user}\n")
            f.write(f"IP: {ip}\n")
            f.write(f"Path: {path}\n")
            f.write("-"*40 + "\n")

        response = self.get_response(request)
        return response



