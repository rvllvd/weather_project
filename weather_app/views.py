import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SearchHistory
from . import weather_api

def index(request):
    last_city = request.session.get("last_city")
    return render(request, "weather_app/index.html", {"last_city": last_city})

@csrf_exempt
def weather_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Только POST запросы разрешены"}, status=405)
    try:
        data = json.loads(request.body)
        city = data.get("city", "").strip()
        if not city:
            return JsonResponse({"error": "Город не указан"}, status=400)
    except Exception:
        return JsonResponse({"error": "Неверный формат данных"}, status=400)

    coords = weather_api.get_city_coordinates(city)
    if coords is None:
        return JsonResponse({"error": "Город не найден"}, status=404)

    lat, lon = coords
    try:
        weather = weather_api.get_weather(lat, lon)
    except Exception:
        return JsonResponse({"error": "Ошибка получения данных о погоде"}, status=500)

    request.session["last_city"] = city.title()

    obj, created = SearchHistory.objects.get_or_create(city=city.title())
    obj.count += 1
    obj.save()

    response_data = {
        "city": city.title(),
        **weather,
    }
    return JsonResponse(response_data)

def autocomplete_view(request):
    q = request.GET.get("q", "").strip()
    if not q:
        return JsonResponse({"results": []})
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "format": "json",
        "q": q,
        "limit": 5,
    }
    headers = {"User-Agent": weather_api.USER_AGENT}
    try:
        r = requests.get(url, params=params, headers=headers)
        r.raise_for_status()
        results = r.json()
        cities = [r["display_name"].split(",")[0] for r in results]
    except Exception:
        cities = []
    return JsonResponse({"results": cities})

def history_view(request):
    data = list(SearchHistory.objects.order_by("-count").values("city", "count"))
    return JsonResponse({"history": data})
