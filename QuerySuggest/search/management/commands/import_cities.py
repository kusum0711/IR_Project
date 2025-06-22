# import os
# from django.core.management.base import BaseCommand
# from search.models import City  

# class Command(BaseCommand):
#     help = 'Import city names from filenames in the data folder and store them in the city model'

#     def handle(self, *args, **kwargs):
#         # Define the path to your data folder (update if the path is different)
#         data_folder_path = os.path.join(os.getcwd(), '../data')  # Assuming 'data' is in the root directory

#         # List all files in the data folder
#         filenames = os.listdir(data_folder_path)

#         # Iterate over the filenames and process only .txt files
#         for filename in filenames:
#             if filename.endswith('.txt'):
#                 # Remove the .txt extension from the filename to get the city name
#                 city_name = filename[:-4]

#                 # Check if the city already exists in the database, avoid duplicates
#                 if not City.objects.filter(name=city_name).exists():
#                     # Save the city name to the database
#                     City.objects.create(name=city_name)
#                     self.stdout.write(self.style.SUCCESS(f'Successfully added city: {city_name}'))
#                 else:
#                     self.stdout.write(self.style.WARNING(f'city {city_name} already exists, skipping...'))
import os
from django.core.management.base import BaseCommand
from search.models import City
from PyPDF2 import PdfReader  # Import PyPDF2 for PDF parsing

class Command(BaseCommand):
    help = 'Import city names from filenames in the data folder and store them in the City model'

    def handle(self, *args, **kwargs):
        # Define the path to your data folder (update if the path is different)
        data_folder_path = os.path.join(os.getcwd(), '../data')  # Adjust path if necessary

        # Check if the data folder exists
        if not os.path.exists(data_folder_path):
            self.stdout.write(self.style.ERROR(f"Data folder '{data_folder_path}' does not exist."))
            return

        # List all files in the data folder
        filenames = os.listdir(data_folder_path)

        # Iterate over the filenames and process .txt and .pdf files
        for filename in filenames:
            file_path = os.path.join(data_folder_path, filename)

            # Skip non-files
            if not os.path.isfile(file_path):
                continue

            # Process .txt files
            if filename.endswith('.txt'):
                city_name = filename[:-4]  # Remove the .txt extension

            # Process .pdf files
            elif filename.endswith('.pdf'):
                city_name = filename[:-4]  # Remove the .pdf extension
                try:
                    # Attempt to read the PDF content (optional if you need content validation)
                    reader = PdfReader(file_path)
                    content = ""
                    for page in reader.pages:
                        content += page.extract_text()

                    # You can add content validation here if required
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error reading PDF file '{filename}': {e}"))
                    continue

            # Skip unsupported file types
            else:
                continue

            # Check if the city already exists in the database, avoid duplicates
            if not City.objects.filter(name=city_name).exists():
                # Save the city name to the database
                City.objects.create(name=city_name)
                self.stdout.write(self.style.SUCCESS(f"Successfully added city: {city_name}"))
            else:
                self.stdout.write(self.style.WARNING(f"City {city_name} already exists, skipping..."))
