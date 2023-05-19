from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from openpyxl.reader.excel import load_workbook

from .serializers import PlaceSerializer
from .models import Places
from .services import create_places


class PlacesApiView(ListCreateAPIView):
    serializer_class = PlaceSerializer
    queryset = Places.objects.all()

    def post(self, request, *args, **kwargs):
        place_serializer = self.get_serializer(data=request.data)
        place_serializer.is_valid(raise_exception=True)

        serializer_data = place_serializer.validated_data
        xlsx_file = serializer_data['xlsx_file']
        workbook = load_workbook(filename=xlsx_file.file)

        worksheet = workbook.active
        places = create_places(worksheet)

        result_data = self.get_serializer(places, many=True)
        return Response(result_data.data, status=status.HTTP_201_CREATED)
