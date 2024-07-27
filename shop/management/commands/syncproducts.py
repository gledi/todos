from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Synchronizes product data with stripe'

    def handle(self, *args, **options):
        print("syncing products ...")
