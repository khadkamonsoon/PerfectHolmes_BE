from rest_framework import generics, status
from rest_framework.response import Response
import os, requests, json, environ
from django.conf import settings
from .serializers import ApartmentSerializer, FacilityDistanceSerializer
from .models import Apartment
from facility.models import Facility
from geopy.distance import distance


class ApartmentSearchAPI(generics.GenericAPIView):
    queryset = Apartment.objects.all()

    def post(self, request):
        facilities_data = request.data.get("facility", [])
        if not facilities_data:
            return Response(
                {"error": "No facilities data provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        valid_facilities = FacilityDistanceSerializer(data=facilities_data, many=True)
        if not valid_facilities.is_valid():
            return Response(valid_facilities.errors, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        apartment_filters = data.get("apartment", {})
        apartments = Apartment.objects.all()

        if "room_count" in apartment_filters:
            apartments = apartments.filter(room_count=apartment_filters["room_count"])

        if "area" in apartment_filters:
            min_area = apartment_filters["area"]["min"]
            max_area = apartment_filters["area"]["max"]
            apartments = apartments.filter(area__gte=min_area, area__lte=max_area)

        if "built_year" in apartment_filters:
            min_year = apartment_filters["built_year"]["min"]
            max_year = apartment_filters["built_year"]["max"]
            apartments = apartments.filter(
                built_year__gte=min_year, built_year__lte=max_year
            )

        if "price" in apartment_filters:
            min_price = apartment_filters["price"]["min"]
            max_price = apartment_filters["price"]["max"]
            apartments = apartments.filter(price__gte=min_price, price__lte=max_price)

        facility_filters = data.get("facility", [])
        valid_apartments = []

        for apartment in apartments:
            valid = True
            for facility_filter in facility_filters:
                facility_type = facility_filter["type"]
                max_distance = facility_filter["distance"]
                unit = facility_filter["unit"]

                if unit == "m":
                    max_distance /= 1000.0  # Convert to kilometers

                facilities = Facility.objects.filter(type=facility_type)
                within_distance = any(
                    distance(
                        (apartment.lat, apartment.lng), (facility.lat, facility.lng)
                    ).km
                    <= max_distance
                    for facility in facilities
                )

                if not within_distance:
                    valid = False
                    break

            if valid:
                valid_apartments.append(apartment)

        serializer = ApartmentSerializer(valid_apartments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class GPTApartmentSearchAPI(generics.GenericAPIView):
    def post(self, request):
        question = request.data.get("question")
        environ.Env.read_env(os.path.join(settings.BASE_DIR, ".env"))
        OPEN_AI_KEY = settings.OPEN_AI_KEY
        OPEN_AI_PROMPT = settings.OPEN_AI_PROMPT
        GPT_MODEL = settings.GPT_MODEL

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPEN_AI_KEY}",
        }
        body = {
            "model": GPT_MODEL,
            "messages": [
                {"role": "system", "content": OPEN_AI_PROMPT},
                {"role": "user", "content": question},
            ],
        }
        try:
            res = requests.post(url, headers=headers, data=json.dumps(body))
            data = res.json()["choices"][0]["message"]["content"]
            apartment_filters = json.loads(data)["apartment"]
            apartments = Apartment.objects.all()

            if "room_count" in apartment_filters:
                apartments = apartments.filter(
                    room_count=apartment_filters["room_count"]
                )

            if "area" in apartment_filters:
                min_area = apartment_filters["area"].get("min", 0)
                max_area = apartment_filters["area"].get("max", 5200)
                apartments = apartments.filter(area__gte=min_area, area__lte=max_area)

            if "built_year" in apartment_filters:
                min_year = apartment_filters["built_year"].get("min",1024)
                max_year = apartment_filters["built_year"].get("max", 2024)
                apartments = apartments.filter(
                    built_year__gte=min_year, built_year__lte=max_year
                )

            if "price" in apartment_filters:
                min_price = apartment_filters["price"].get("min",0)
                max_price = apartment_filters["price"].get("max", 2000000024)
                apartments = apartments.filter(
                    price__gte=min_price, price__lte=max_price
                )

            facility_filters = json.loads(data).get("facility", [])
            valid_apartments = []

            for apartment in apartments:
                valid = True
                for facility_filter in facility_filters:
                    facility_type = facility_filter["type"]
                    max_distance = facility_filter["distance"]
                    unit = facility_filter["unit"]

                    if unit == "m":
                        max_distance /= 1000.0  # Convert to kilometers

                    facilities = Facility.objects.filter(type=facility_type)
                    within_distance = any(
                        distance(
                            (apartment.lat, apartment.lng), (facility.lat, facility.lng)
                        ).km
                        <= max_distance
                        for facility in facilities
                    )

                    if not within_distance:
                        valid = False
                        break

                if valid:
                    valid_apartments.append(apartment)

            serializer = ApartmentSerializer(valid_apartments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("Request Exception:", e) 
            return Response(status=status.HTTP_400_BAD_REQUEST)
