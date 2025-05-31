from datetime import datetime
from django.core.cache import cache
from django.shortcuts import render
import requests as http
from requests.exceptions import RequestException, Timeout
import pytz
from babel.dates import format_datetime
from weather.models import CitySearch


# Create your views here.
def index(request):

    last_city = request.session.get("last_city")

    weather = None
    lat = None
    lon = None
    timezone = None
    tz = None
    now = None
    target_time = None

    WMO_CODES = {
        0: "Ясное небо",
        1: "Преимущественно ясно",
        2: "Переменная облачность",
        3: "Пасмурно",
        45: "Туман",
        48: "Туман с изморозью",
        51: "Слабая морось",
        53: "Умеренная морось",
        55: "Сильная морось",
        56: "Слабая замерзающая морось",
        57: "Сильная замерзающая морось",
        61: "Слабый дождь",
        63: "Умеренный дождь",
        65: "Сильный дождь",
        66: "Слабый ледяной дождь",
        67: "Сильный ледяной дождь",
        71: "Слабый снегопад",
        73: "Умеренный снегопад",
        75: "Сильный снегопад",
        77: "Снежные зерна (град/крупа)",
        80: "Слабые ливни",
        81: "Умеренные ливни",
        82: "Сильные ливни",
        85: "Слабые снежные ливни",
        86: "Сильные снежные ливни",
        95: "Гроза",
        96: "Гроза с небольшим градом",
        99: "Гроза с сильным градом",
    }

    location = request.GET.get("location")
    if location:
        cache_key = f"weather:{location.lower()}"
        weather = cache.get(cache_key)
        if not weather:
            request.session["last_city"] = location
            try:
                geocoding = http.get(
                    "https://geocoding-api.open-meteo.com/v1/search?",
                    params={"name": location, "count": 7},
                    timeout=2,
                )
                if geocoding.status_code == 200:
                    results = geocoding.json().get("results", [])
                    if results:
                        lat = results[0]["latitude"]
                        lon = results[0]["longitude"]
                        timezone = results[0]["timezone"]
                    else:
                        raise Exception(
                            f"Город '{location}' не найден. Попробуйте ввести его на английском."
                        )
                else:
                    raise Exception(
                        f"Error API geocoding: status - {geocoding.status_code}"
                    )

            except (RequestException, Timeout) as e:
                weather = {
                    "error": "Сетевая ошибка при подключении к погодному сервису. Попробуйте позже."
                }
            except Exception as e:
                weather = {"error": str(e)}

            if lat is not None and lon is not None:
                try:
                    response = http.get(
                        "https://api.open-meteo.com/v1/forecast",
                        params={
                            "latitude": lat,
                            "longitude": lon,
                            "timezone": timezone,
                            "hourly": "temperature_2m,apparent_temperature,wind_speed_10m,pressure_msl,precipitation,weathercode,relativehumidity_2m",
                        },
                        timeout=2,
                    )
                    tz = pytz.timezone(timezone)
                    now = datetime.now(tz).replace(
                        minute=0, second=0, microsecond=0
                    )
                    target_time = now.replace(tzinfo=None).isoformat(
                        timespec="minutes"
                    )
                    if response.status_code == 200:
                        hourly_data = response.json().get("hourly", {})
                        time_list = hourly_data.get("time", [])
                        if not request.session.session_key:
                            request.session.create()
                        CitySearch.objects.create(
                            city=location,
                            session_key=request.session.session_key,
                            user_agent=request.META.get("HTTP_USER_AGENT", ""),
                            ip_address=request.META.get("REMOTE_ADDR", "0.0.0.0"),
                        )
                        if target_time in time_list:
                            idx = time_list.index(target_time)
                            date_time_en_format = datetime.now(tz).replace(
                                microsecond=0, tzinfo=None
                            )
                            weather = {
                                "date_time": format_datetime(
                                    date_time_en_format,
                                    "d MMMM y, HH:mm",
                                    locale="ru",
                                ),
                                "temperature": hourly_data["temperature_2m"][idx],
                                "apparent_temperature": hourly_data[
                                    "apparent_temperature"
                                ][idx],
                                "wind_speed": hourly_data["wind_speed_10m"][idx],
                                "pressure": round(
                                    hourly_data["pressure_msl"][idx] * 0.75
                                ),
                                "precipitation": hourly_data["precipitation"][idx],
                                "humidity": hourly_data["relativehumidity_2m"][idx],
                                "weathercode": WMO_CODES[
                                    hourly_data["weathercode"][idx]
                                ],
                            }
                            cache.set(cache_key, weather, timeout=60 * 5)
                    else:
                        raise Exception(
                            f"Error API geocoding: status - {geocoding.status_code}"
                        )
                except (RequestException, Timeout) as e:
                    weather = {
                        "error": "Сетевая ошибка при подключении к погодному сервису. Попробуйте позже."
                    }
                except Exception as e:
                    weather = {"error": str(e)}

    return render(
        request,
        "weather/index.html",
        {"location": location, "weather": weather, "last_city": last_city},
    )
