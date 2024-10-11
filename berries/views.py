from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http.request import HttpRequest
from django.http import HttpResponse


@csrf_exempt
@require_http_methods(["GET"])
def all_berry_stats(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Hello Word', status=200)