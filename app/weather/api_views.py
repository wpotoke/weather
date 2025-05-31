from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from weather.models import CitySearch


class Autocomplete(APIView):
    def get(self, request):
        query = request.GET.get("query", "").strip()
        if not query:
            return Response([])
        cities = (
            CitySearch.objects.filter(city__istartswith=query)
            .values_list("city", flat=True)
            .distinct()[:10]
        )
        return Response(list(cities))


class CityStatsView(APIView):
    def get(self, request):
        stats = (
            CitySearch.objects.values("city")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        return Response(list(stats))
