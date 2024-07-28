from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Create default groups'

    def handle(self, *args, **options):
        group_names = ['Administrators', 'Editors', 'Writers', 'Subscribers']
        for group_name in group_names:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created group: {group}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Group already exists: {group}'))
