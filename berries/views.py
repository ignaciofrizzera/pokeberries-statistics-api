from berries.service import BerriesService
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.http.request import HttpRequest
from django.http import JsonResponse, HttpResponse
from typing import Union


@csrf_exempt
@require_http_methods(["GET"])
def all_berry_stats(request: HttpRequest) -> JsonResponse:
    try:
        berry_stats = BerriesService().get_statistics()
        return JsonResponse(berry_stats, status=200)
    except Exception:
        return JsonResponse({'error': 'There was an error processing the berry statistics.'}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def berries_stats_visualization(request: HttpRequest) -> Union[HttpResponse, JsonResponse]:
    # try:
    berry_stats = BerriesService().get_statistics()
    return render(request, template_name='berries_stats_visualization.html', context=berry_stats)
    # except Exception:
        # return JsonResponse({'error': 'There was an error generating the visualization for the berries data.'}, status=500)