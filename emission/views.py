from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from emission.calculator import CalculationStrategyFactory
from emission.serializers import ActivityDateFileSerializer


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
            result = strategy.calculate(csv_file_path)
            return Response(status=status.HTTP_201_CREATED, data={'result': result})
        else:
            return Response(activity_data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
