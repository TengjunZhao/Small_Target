from django.core.management.base import BaseCommand
from project_management.models import create_demo_data

class Command(BaseCommand):
    help = 'Initialize project management demo data'
    
    def handle(self, *args, **options):
        self.stdout.write('Creating demo project data...')
        try:
            project = create_demo_data()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created project: {project.name}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating demo data: {str(e)}')
            )