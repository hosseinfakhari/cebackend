from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from emission.calculator import CalculationStrategyFactory
from emission.models import ActivityData
from emission.serializers import ActivityDateFileSerializer, ActivityDataSerializer


class EmissionCalculatorAPIView(APIView):
    parser_classes = (MultiPartParser,)

    def put(self, request):
        try:
            activity_data_serializer = ActivityDateFileSerializer(data=request.data)
        except Exception as e:
            print('Error while initializing serializer:', str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if activity_data_serializer.is_valid():
            activity_data_serializer.save()
            uploaded_file = activity_data_serializer.instance
            csv_file_path = uploaded_file.file.path
            strategy = CalculationStrategyFactory.get_strategy(csv_file_path)
            activity_data_list = strategy.calculate(csv_file_path)
            serialized_data = ActivityDataSerializer(activity_data_list, many=True)
            return Response(status=status.HTTP_201_CREATED, data=serialized_data.data)
        else:
            return Response(activity_data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivityDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityData.objects.all()
    serializer_class = ActivityDataSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['scope', 'category']
    ordering_fields = ['co2e']
