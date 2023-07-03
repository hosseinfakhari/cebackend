import csv

from rest_framework import serializers
from .models import ActivityDataFile, ActivityData


class ActivityDateFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityDataFile
        fields = ('file', 'uploaded_at',)

    def validate_file(self, value):
        try:
            csv_file = csv.reader(value.read().decode('utf-8').splitlines())
        except Exception as e:
            raise serializers.ValidationError('Invalid CSV file: %s' % e)
        return value


class ActivityDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActivityData
        fields = ('id', 'activity', 'co2e', 'scope', 'category')
