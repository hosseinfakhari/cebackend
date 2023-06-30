from abc import ABC, abstractmethod
from csv import DictReader

from django.db.models import Q
from rest_framework import serializers

from emission.models import EmissionFactor


class EmissionCalculator(ABC):
    @abstractmethod
    def calculate(self, data):
        pass


class ElectricityActivityCalculator(EmissionCalculator):
    def calculate(self, csv_file_name):
        reader = DictReader(open(csv_file_name))
        emissions = []
        for row in reader:
            factor = EmissionFactor.objects.filter(Q(activity='Electricity') &
                                                   Q(lookup_identifiers__contains=row['Country'])).first()
            if factor:
                co2e = float(row['Electricity Usage']) * factor.co2e
                emissions.append({
                    "co2e": co2e,
                    "scope": factor.scope,
                    "category": factor.category,
                    "activity": factor.activity,
                })
        return emissions


class AirTravelActivityCalculator(EmissionCalculator):
    def calculate(self, csv_file_name):
        reader = DictReader(open(csv_file_name))
        emissions = []
        for row in reader:
            factor = EmissionFactor.objects.filter(Q(activity='Air Travel') &
                                                   Q(lookup_identifiers__contains=row['Flight range']) &
                                                   Q(lookup_identifiers__contains=row['Passenger class'])).first()
            if factor:
                co2e = float(row['Distance travelled']) * factor.co2e
                emissions.append({
                    "co2e": co2e,
                    "scope": factor.scope,
                    "category": factor.category,
                    "activity": factor.activity,
                })
        return emissions


class PurchasedGoodsActivityCalculator(EmissionCalculator):
    def calculate(self, csv_file_name):
        reader = DictReader(open(csv_file_name))
        emissions = []
        for row in reader:
            factor = EmissionFactor.objects.filter(Q(activity='Purchased Goods and Services') &
                                                   Q(lookup_identifiers__contains=row['Supplier category'])).first()
            if factor:
                co2e = float(row['Spend']) * factor.co2e
                emissions.append({
                    "co2e": co2e,
                    "scope": factor.scope,
                    "category": factor.category,
                    "activity": factor.activity,
                })
        return emissions


class CalculationStrategyFactory:
    @staticmethod
    def get_strategy(csv_file_name):
        reader = DictReader(open(csv_file_name))
        header = reader.fieldnames

        purchased_goods_columns = ['Date', 'Activity', 'Supplier category', 'Spend', 'Spend units']
        electricity_columns = ['Activity', 'Date',  'Country', 'Electricity Usage', 'Units']
        air_travel_columns = ['Date', 'Activity', 'Distance travelled', 'Distance units', 'Flight range',
                              'Passenger class']

        if set(purchased_goods_columns).issubset(header):
            return PurchasedGoodsActivityCalculator()
        elif set(electricity_columns).issubset(header):
            return ElectricityActivityCalculator()
        elif set(air_travel_columns).issubset(header):
            return AirTravelActivityCalculator()
        else:
            raise serializers.ValidationError("Not a valid activity data")
