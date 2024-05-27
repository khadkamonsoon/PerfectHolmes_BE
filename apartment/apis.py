from rest_framework import generics, status
from rest_framework.response import Response
import os, requests, json, environ
from django.conf import settings
from .serializers import ApartmentSerializer, FacilityDistanceSerializer
from .models import Apartment
from facility.models import Facility
from geopy.distance import geodesic


class ApartmentSearchAPI(generics.GenericAPIView):
    queryset = Apartment.objects.all()

    def post(self, request):
        facilities_data = request.data.get("facilities", [])
        if not facilities_data:
            return Response(
                {"error": "No facilities data provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        valid_facilities = FacilityDistanceSerializer(data=facilities_data, many=True)
        if not valid_facilities.is_valid():
            return Response(valid_facilities.errors, status=status.HTTP_400_BAD_REQUEST)

        facilities_data = valid_facilities.validated_data

        apartment_request = request.data.get("apartment")

        queryset = self.get_queryset()

        matching_apartments = []

        for apartment in queryset:
            apartment_location = (apartment.lat, apartment.lng)
            matches_all = True

            for facility_data in facilities_data:
                facility_type = facility_data["type"]
                max_distance = facility_data["distance"]
                unit = facility_data["unit"]

                if unit.lower() == "m":
                    max_distance_km = max_distance / 1000.0  # 미터를 킬로미터로 변환
                else:
                    return Response(
                        {"error": "Unsupported unit"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                nearby_facilities = Facility.objects.filter(type=facility_type)
                facility_within_distance = False

                for facility in nearby_facilities:
                    facility_location = (facility.lat, facility.lng)
                    actual_distance_km = geodesic(
                        apartment_location, facility_location
                    ).km
                    if actual_distance_km <= max_distance_km:
                        facility_within_distance = True
                        break

                if not facility_within_distance:
                    matches_all = False
                    break

            if matches_all:
                matching_apartments.append(apartment)

        return Response(status=status.HTTP_200_OK)


class GPTApartmentSearchAPI(generics.GenericAPIView):
    def post(self, request):
        question = request.data.get("question")
        environ.Env.read_env(os.path.join(settings.BASE_DIR, ".env"))
        OPEN_AI_KEY = settings.OPEN_AI_KEY
        OPEN_AI_PROMPT = settings.OPEN_AI_PROMPT

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPEN_AI_KEY}",
        }
        body = {
            "model": "ft:gpt-3.5-turbo-1106:personal:estate-new:9O2fT1bE",
            "messages": [
                {"role": "system", "content": OPEN_AI_PROMPT},
                {"role": "user", "content": question},
            ],
        }
        try:
            res = requests.post(url, headers=headers, data=json.dumps(body))
            return Response(res.json())
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
