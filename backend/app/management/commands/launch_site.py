"""
Django management command launch_site
"""

import platform
import subprocess

from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    """
    Custom django-admin command to launch the local website
    """

    help = "Custom django-admin command to launch the local website"

    def handle(self, *args, **options):
        on_windows = platform.system() == "Windows"
        frontend_cmd = [f"npm{'.cmd' if on_windows else ''}", "run", "start"]
        with subprocess.Popen(frontend_cmd) as frontend:
            call_command("runserver")
            frontend.kill()
