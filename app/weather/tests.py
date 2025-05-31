from django.test import Client, SimpleTestCase, TestCase, override_settings
from django.urls import resolve, reverse
from weather.models import CitySearch
from django.core.exceptions import ValidationError
from weather.views import index
from django.core.cache import cache
from unittest.mock import patch
from datetime import datetime
import pytz


# Create your tests here.
class SearchCityModelTets(TestCase):

    def setUp(self):
        self.city = CitySearch.objects.create(
            city="Москва",
            session_key="knksjdnjkcndkjsncdjkcnd",
            user_agent="Mozilla/4.0 (Windows NT 10.0; Win32; x32)  Chrome/136.0.0.1 Safari/217.90",
            ip_address="127.0.0.1",
        )

    def test_create_city(self):
        self.assertIsInstance(self.city, CitySearch)

    def test_saving_and_retrieving_city(self):
        london_city = CitySearch()
        london_city.city = "london"
        london_city.session_key = "lajknoeicbuiabclekcndhbcaklcie"
        london_city.user_agent = (
            "Mozilla/5.0 (Windows NT 9.0; Win32; x32) Chrome/191.0.0.1 Safari/217.90"
        )
        london_city.ip_address = "127.0.0.1"
        london_city.save()

        cities = CitySearch.objects.all()
        self.assertEqual(cities.count(), 2)
        self.assertEqual(cities.first().city, "Москва")
        self.assertEqual(cities.last().session_key, "lajknoeicbuiabclekcndhbcaklcie")

    def test_city_field_max_length(self):
        long_city_name = "a" * 101
        city = CitySearch(
            city=long_city_name,
            session_key="skmsclke1",
            user_agent="agent",
            ip_address="127.0.0.1",
        )
        with self.assertRaises(ValidationError):
            city.full_clean()

    def test_blank_required_fields(self):
        city = CitySearch(city="", session_key="", user_agent="", ip_address="")
        with self.assertRaises(ValidationError):
            city.full_clean()


class WeatherURLsTets(SimpleTestCase):
    def test_mainpage_url_name(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_root_url_resolves_to_homepage_view(self):
        found = resolve("/")
        self.assertEqual(found.func, index)


class WeatherTemplateTest(SimpleTestCase):

    def setUp(self):
        url = reverse("index")
        self.response = self.client.get(url)

    def test_mainpage_template(self):
        self.assertTemplateUsed(self.response, "weather/index.html")
        self.assertTemplateUsed(self.response, "base.html")

class MockResponse:
    def __init__(self, json_data, status_code):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data

class WeatherIndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("index")
        cache.clear()

    @patch("weather.views.http.get")
    def test_city_search_and_database_entry(self, mock_http_get):
        moscow_tz = pytz.timezone("Europe/Moscow")
        now = datetime.now(moscow_tz).replace(minute=0, second=0, microsecond=0)
        target_time = now.replace(tzinfo=None).isoformat(timespec="minutes")

        mock_http_get.side_effect = [
            MockResponse(
                {
                    "results": [
                        {
                            "latitude": 55.75,
                            "longitude": 37.62,
                            "timezone": "Europe/Moscow",
                        }
                    ]
                },
                200,
            ),
            MockResponse(
                {
                    "hourly": {
                        "time": [target_time],
                        "temperature_2m": [20],
                        "apparent_temperature": [18],
                        "wind_speed_10m": [3.4],
                        "pressure_msl": [1012],
                        "precipitation": [0.0],
                        "weathercode": [1],
                        "relativehumidity_2m": [50],
                    }
                },
                200,
            ),
        ]
        response = self.client.get(self.url, {"location": "Москва"})
        self.assertEqual(response.status_code, 200)

        self.assertTrue(CitySearch.objects.filter(city="Москва").exists())



        self.assertIn("weather", response.context)
        self.assertIn("temperature", response.context["weather"])

    @patch("weather.views.http.get", side_effect=Exception("API down"))
    def test_external_api_failure(self, mock_get):
        response = self.client.get(self.url, {"location": "Москва"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("error", response.context["weather"])

    def test_cache_key_is_used(self):
        cache.set("weather:москва", {"temperature": 123}, timeout=60 * 5)
        response = self.client.get(self.url, {"location": "Москва"})
        self.assertEqual(response.context["weather"]["temperature"], 123)
