from rest_framework import generics
from .serializers import FacilitySerializer


class FacilityListAPI(generics.ListAPIView):
    serializer_class = FacilitySerializer
