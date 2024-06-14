import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """ django command to pause the execution until db is ready """

    def handle(self, *args, **options):
        self.stdout.write('waiting for database ...')
        db_connection = None
        while not db_connection:
            try: 
                db_connection = connections['default']
            except OperationalError:
                self.stdout.write('database unavailable, waiting one second ...')
                time.sleep(1)
            
        self.stdout.write(self.style.SUCCESS('database is available'))