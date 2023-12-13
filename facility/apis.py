from rest_framework import generics
from .serializers import FacilitySerializer
from .models import Facility
from api.exceptions import CustomValidationError
from haversine import haversine


class FacilityListAPI(generics.ListAPIView):
    serializer_class = FacilitySerializer
    queryset = Facility.objects.all()


class AroundFacilityListAPI(generics.ListAPIView):
    serializer_class = FacilitySerializer
    queryset = Facility.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        lat = self.request.query_params.get("lat", None)
        lng = self.request.query_params.get("lng", None)
        if not lat and lng:
            raise CustomValidationError({"data": "lat, lng 를 모두 입력하세요"})

        try:
            lat = float(lat)
            lng = float(lng)
        except ValueError:
            raise CustomValidationError({"error": "lat, lng는 유효한 숫자여야 합니다"})

        print(lat, lng)

        facilities_within_500m = []

        for facility in queryset:
            distance = haversine((lat, lng), (facility.lat, facility.lng))
            if distance <= 0.5:  # 500m 이내의 시설
                facilities_within_500m.append(facility)

        return facilities_within_500m
