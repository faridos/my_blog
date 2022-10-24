import os
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.views import APIView


class PullDataFromMS(APIView):
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        print(kwargs)
# data = json.loads(json.dumps(serializer.data))
# for item, values in data.items():
# return Response({"units": new_data})
