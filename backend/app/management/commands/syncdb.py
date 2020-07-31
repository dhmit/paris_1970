"""
Django management command syncdb

Syncs local db with data from project Google Sheet

TODO(ra): link Google Sheet here
"""


from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Syncs local db with data from project Google Sheet'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Hello, world!'))
