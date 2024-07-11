from django.core.management.base import BaseCommand, CommandError
# from dataentry.models import Student
from django.apps import apps
import csv
from django.db import DataError

class Command(BaseCommand):
    help = 'Imports data from csv file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')
        parser.add_argument('model_name', type=str, help='Name of the model')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()

        # Search for the model across all installed appps
        model = None
        for app_config in apps.get_app_configs():
            # Try to search for the model
            try:
                model = apps.get_model(app_config.label, model_name)
                break # stop searching once the model is found
            except LookupError:
                continue # model not found in this app, continue seatching in next app.

        if not model:
            raise CommandError(f"Model {model_name} not found in any app!")

        # compare csv header with model's field names

        # get all the field names of the model that we found
        model_fields = [field.name for field in model._meta.fields if field.name != 'id']

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                model.objects.create(**row)

        self.stdout.write(self.style.SUCCESS('Data imported from csv successfully!'))
