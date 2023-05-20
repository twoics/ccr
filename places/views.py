from django.core.files import File
from django.http import HttpResponse
from openpyxl.reader.excel import load_workbook
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from .models import Places
from .serializers import PlaceSerializer
from .services import create_places, export_weather


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


@api_view(['GET'])
def weather_xlsx(request):
    path = export_weather()
    file = open(path, 'rb')
    response = HttpResponse(File(file), content_type='application/xlsx')
    response['Content-Disposition'] = 'attachment; filename="%s"' % 'weather.xlsx'
    return response
