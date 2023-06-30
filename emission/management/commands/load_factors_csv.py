import os
from csv import DictReader
from django.core.management import BaseCommand
from emission.models import EmissionFactor

ALREADY_LOADED_ERROR_MESSAGE = """
If you need to reload the emission factor data from the CSV file, run the command with `--replace`
Run `python manage.py load_factors_csv --replace`"""


def load_csv_to_db(csv_file_name, replace):
    if replace:
        EmissionFactor.objects.all().delete()
    reader = DictReader(open(csv_file_name))
    header = reader.fieldnames
    required_columns = ['Activity', 'Lookup identifiers', 'Unit', 'CO2e', 'Scope', 'Category']
    if not set(required_columns).issubset(header):
        raise ValueError("Some required columns are missing. not a valid emission factors csv file!")
    for row in reader:
        emission_factor = EmissionFactor(activity=row['Activity'], lookup_identifiers=row['Lookup identifiers'],
                                         unit=row['Unit'], co2e=row['CO2e'], scope=row['Scope'],
                                         category=row['Category'] if row['Category'] else None)
        emission_factor.save()


class Command(BaseCommand):
    help = "Loads emission factor data from csv"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", nargs='?', default='', type=str)
        parser.add_argument(
            "--replace",
            action="store_true",
            help="Delete emission factor data from db",
        )

    def handle(self, *args, **options):
        csv_file_name = options['csv_file']
        if not csv_file_name:
            self.stdout.write(self.style.ERROR("Please provide a CSV file name"))
            return

        if not os.path.isfile(csv_file_name):
            self.stdout.write(self.style.ERROR(f"File '{csv_file_name}' does not exist"))
            return

        if EmissionFactor.objects.exists():
            self.stdout.write(self.style.ERROR('Emission factor data already loaded...exiting.'))
            self.stdout.write(self.style.SUCCESS(ALREADY_LOADED_ERROR_MESSAGE))
            return
        if options["replace"]:
            self.stdout.write(self.style.SUCCESS('All emission factor data deleted from database.'))
        load_csv_to_db(csv_file_name, options["replace"])
