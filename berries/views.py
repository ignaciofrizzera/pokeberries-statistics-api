from berries.service import BerriesService
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http.request import HttpRequest
from django.http import JsonResponse


@csrf_exempt
@require_http_methods(["GET"])
def all_berry_stats(request: HttpRequest) -> JsonResponse:
    try:
        berry_stats = BerriesService().get_statistics()
        return JsonResponse(berry_stats, status=200)
    except Exception:
        return JsonResponse({'error': 'There was an error processing the berry statistics.'}, status=500)