from io import StringIO
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .models import ActivityData, EmissionFactor, ActivityDataFile, EmissionFactorFile
from .serializers import ActivityDataSerializer
from .views import ActivityDataViewSet
from django.contrib.auth.models import User


class LoadFactorsCsvTest(TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def test_load_factors_csv(self, mock_stdout):
        # Create a mock CSV file in memory
        csv_content = (
            'Activity,Lookup identifiers,Unit,CO2e,Scope,Category\n'
            'Activity1,ABC123,kg,1515.0,3,1\n'
            'Activity2,DEF456,kg,2020.0,2,1'
        )
        csv_file = SimpleUploadedFile('test.csv', csv_content.encode())

        # Run the command
        call_command('load_factors_csv', csv_file.path)

        # Check that the data was loaded correctly
        self.assertEqual(EmissionFactor.objects.count(), 2)
        self.assertEqual(EmissionFactor.objects.first().activity, 'Activity1')

        # Check the command's output
        self.assertIn('All emission factor data deleted from database.', mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_load_factors_csv_replace(self, mock_stdout):
        # First, create some existing data
        EmissionFactor.objects.create(activity='ExistingActivity', lookup_identifiers='XYZ', unit='kg', co2e=1000.0,
                                      scope=1, category=1)

        # Then, run the command with --replace
        csv_content = 'Activity,Lookup identifiers,Unit,CO2e,Scope,Category\nActivity1,ABC123,kg,1515.0,3,1'
        csv_file = SimpleUploadedFile('test.csv', csv_content.encode())
        call_command('load_factors_csv', csv_file.path, '--replace')

        # Check that the existing data was deleted and new data was loaded
        self.assertEqual(EmissionFactor.objects.count(), 1)
        self.assertEqual(EmissionFactor.objects.first().activity, 'Activity1')

        # Check the command's output
        self.assertIn('All emission factor data deleted from database.', mock_stdout.getvalue())


class ActivityDataFileModelTest(TestCase):
    def test_file_upload(self):
        uploaded_file = SimpleUploadedFile('file.txt', b'file_content')
        file = ActivityDataFile.objects.create(file=uploaded_file)
        self.assertIsNotNone(file.file)
        self.assertIsNotNone(file.uploaded_at)


class EmissionFactorFileModelTest(TestCase):
    @patch('django.core.management.call_command')
    def test_file_upload_and_command_call(self, mock_call_command):
        uploaded_file = SimpleUploadedFile('file.txt', b'file_content')
        file = EmissionFactorFile.objects.create(file=uploaded_file, update_factors=True)
        self.assertIsNotNone(file.file)
        mock_call_command.assert_called_once_with('load_factors_csv', file.file.path)


class EmissionFactorModelTest(TestCase):
    def setUp(self):
        EmissionFactor.objects.create(
            activity="Manufacturing",
            lookup_identifiers="ABC123",
            unit="kg",
            co2e=1515.0,
            scope=3,
            category=1,
            active=True,
        )

    def test_emission_factor_content(self):
        emission_factor = EmissionFactor.objects.get(id=1)
        expected_activity = f'{emission_factor.activity}'
        expected_lookup_identifiers = f'{emission_factor.lookup_identifiers}'
        expected_unit = f'{emission_factor.unit}'
        expected_co2e = f'{emission_factor.co2e}'
        expected_scope = f'{emission_factor.scope}'
        expected_category = f'{emission_factor.category}'
        expected_active = f'{emission_factor.active}'
        self.assertEqual(expected_activity, 'Manufacturing')
        self.assertEqual(expected_lookup_identifiers, 'ABC123')
        self.assertEqual(expected_unit, 'kg')
        self.assertEqual(expected_co2e, '1515.0')
        self.assertEqual(expected_scope, '3')
        self.assertEqual(expected_category, '1')
        self.assertEqual(expected_active, 'True')

    def test_created_updated_fields(self):
        emission_factor = EmissionFactor.objects.get(id=1)
        self.assertIsNotNone(emission_factor.created)
        self.assertIsNotNone(emission_factor.updated)


class ActivityDataModelTest(TestCase):
    def setUp(self):
        ActivityData.objects.create(
            activity="Purchased Goods and Services",
            co2e=1515.0,
            scope=3,
            category=1
        )

    def test_activity_data_content(self):
        activity_data = ActivityData.objects.get(id=1)
        expected_activity = f'{activity_data.activity}'
        expected_co2e = f'{activity_data.co2e}'
        expected_scope = f'{activity_data.scope}'
        expected_category = f'{activity_data.category}'
        self.assertEqual(expected_activity, 'Purchased Goods and Services')
        self.assertEqual(expected_co2e, '1515.0')
        self.assertEqual(expected_scope, '3')
        self.assertEqual(expected_category, '1')


class ActivityDataViewSetTestCase(TestCase):
    def setUp(self):
        # Set up data for the tests
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='test', password='test')
        self.view = ActivityDataViewSet.as_view({'get': 'list'})

    def test_get_all_activity_data(self):
        # Create a request and pass it to the view
        request = self.factory.get(reverse('activitydata-list'))
        force_authenticate(request, user=self.user)
        response = self.view(request)

        # Check that the response has a 200 status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response contains the correct data
        expected_data = ActivityDataSerializer(ActivityData.objects.all(), many=True).data
        self.assertEqual(response.data, expected_data)

    def test_get_filtered_activity_data(self):
        # Create a request with a filter and pass it to the view
        request = self.factory.get(reverse('activitydata-list'), {'scope': 2})
        force_authenticate(request, user=self.user)
        response = self.view(request)

        # Check that the response has a 200 status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response contains the correct data
        expected_data = ActivityDataSerializer(ActivityData.objects.filter(scope=2), many=True).data
        self.assertEqual(response.data, expected_data)
