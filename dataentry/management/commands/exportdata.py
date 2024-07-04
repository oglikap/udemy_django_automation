import csv, datetime
from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = 'Export data from the database to a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='Model name')

    def handle(self, *args, **kwargs):
        model_name = kwargs['model_name'].capitalize()

        # search through all the registered apps for the model
        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break # stop executing one the model is found
            except LookupError:
                pass

        if not model:
            self.stderr.write(f'Model {model_name} could not be found.')
            return

        #fetch the data from the database
        data = model.objects.all()

        # generate the timestamp of current date and time
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

        #define the csv file path
        file_path = f'export/exported_{model_name}_data_{timestamp}.csv'

        # open the csv file and write the data
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)

            #write the csv header
            # print the field names of the model 
            writer.writerow([field.name for field in model._meta.fields])

            # write data rows
            for dt in data:
                writer.writerow([getattr(dt, field.name) for field in model._meta.fields])

        self.stdout.write(self.style.SUCCESS('Data exported successfully!'))