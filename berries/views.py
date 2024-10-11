from django.http.request import HttpRequest
from django.http import HttpResponse


def all_berry_stats(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Hello Word', status=200)