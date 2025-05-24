from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
import json

class WeatherAppTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_page_loads(self):
        """Главная страница загружается и содержит нужные элементы"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Введите название города')
        self.assertContains(response, '<input type="text" id="city-input"')

    @patch('weather_app.weather_api.get_city_coordinates')
    @patch('weather_app.weather_api.get_weather')
    def test_weather_view_valid_city(self, mock_get_weather, mock_get_coords):
        """Тест API погоды с валидным городом"""
        mock_get_coords.return_value = (55.7558, 37.6173)  # Москва
        mock_get_weather.return_value = {
            "temperature": 10,
            "windspeed": 5,
            "humidity": 80,
            "time": "2025-05-24T12:00:00Z"
        }

        response = self.client.post(
            reverse('weather_api'),
            data=json.dumps({"city": "Moscow"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['city'], 'Moscow')
        self.assertIn('temperature', data)
        self.assertIn('windspeed', data)
        self.assertIn('humidity', data)
        self.assertIn('time', data)

    def test_weather_view_missing_city(self):
        """Тест API погоды с отсутствующим параметром city"""
        response = self.client.post(
            reverse('weather_api'),
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    @patch('weather_app.weather_api.get_city_coordinates')
    def test_weather_view_city_not_found(self, mock_get_coords):
        """Тест API погоды с несуществующим городом"""
        mock_get_coords.return_value = None
        response = self.client.post(
            reverse('weather_api'),
            data=json.dumps({"city": "Nocity"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json())

    def test_weather_view_invalid_method(self):
        """Тест API погоды с GET-запросом (не POST)"""
        response = self.client.get(reverse('weather_api'))
        self.assertEqual(response.status_code, 405)
        self.assertIn('error', response.json())

    @patch('weather_app.views.requests.get')
    def test_autocomplete_view(self, mock_requests_get):
        """Тест автодополнения городов"""
        mock_response = [
            {"display_name": "Moscow, Russia"},
            {"display_name": "Moscow, Idaho, USA"},
        ]
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = mock_response

        response = self.client.get(reverse('autocomplete_api'), {'q': 'Mos'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('results', data)
        self.assertIn('Moscow', data['results'][0])

    def test_autocomplete_view_empty_query(self):
        """Тест автодополнения с пустым запросом"""
        response = self.client.get(reverse('autocomplete_api'), {'q': ''})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['results'], [])

    def test_history_view(self):
        """Тест API истории поиска"""
        from weather_app.models import SearchHistory
        SearchHistory.objects.create(city="Moscow", count=5)
        SearchHistory.objects.create(city="London", count=3)

        response = self.client.get(reverse('history_api'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('history', data)
        self.assertEqual(len(data['history']), 2)
        self.assertEqual(data['history'][0]['city'], 'Moscow')
