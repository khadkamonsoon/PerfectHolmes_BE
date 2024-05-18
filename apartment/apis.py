from rest_framework import generics, status
from rest_framework.response import Response
import os, requests, json, environ
from django.conf import settings


class ApartmentSearchAPI(generics.GenericAPIView):
    def post(self, request):
        facility = request.data.get("facility")
        apartment = request.data.get("apartment")
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
