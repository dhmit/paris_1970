"""
Django management command syncdb

Syncs local db with data from project Google Sheet
"""

import os
import camelot
import pandas as pd

from django.conf import settings
from django.core.management.base import BaseCommand


def camelot_table(pdf_path, page_range, flavor="lattice"):
    if page_range == (-1, -1):
        prange = 'all'
    else:
        start, end = page_range
        prange = f"{start}-{end}"
    camelot_df = (camelot
                  .read_pdf(pdf_path,
                            flavor=flavor,
                            suppress_stdout=True,
                            pages=prange)
                  )
    return camelot_df


def save_pdf_tables(pdf_path, page_range, mode="lattice"):
    camelot_df = camelot_table(pdf_path, page_range, mode)
    pdf_folder, ext = os.path.splitext(pdf_path)
    _, pdf_name = os.path.split(pdf_folder)
    output_folder = os.path.join(settings.ANALYSIS_DIR, f'extracted_tables/{pdf_name}')
    os.makedirs(
        output_folder,
        exist_ok=True
    )
    output_path = os.path.join(output_folder, f'{pdf_name}.csv')
    camelot_df.export(output_path, f='csv')


class Command(BaseCommand):
    """
    Custom django-admin command used to run an analysis from the app/analysis folder
    """
    help = 'Run an analysis'

    def add_arguments(self, parser):
        parser.add_argument('--pdf_name', action='store', type=str, default='all')
        parser.add_argument(
            '--page_range',
            action='store',
            type=int,
            nargs=2,
            metavar=('start', 'end'),
            default=(-1, -1),
        )
        parser.add_argument(
            '--mode',
            action='store',
            type=str,
            default="lattice",
        )

    def handle(self, *args, **options):
        pdf_name = options.get('pdf_name')
        page_range = options.get('page_range')
        pd.set_option('display.max_colwidth', None)
        arrondissements_folder = os.path.join(settings.ANALYSIS_DIR, 'source_pdfs')
        if pdf_name == 'all':
            for pdf in os.scandir(arrondissements_folder):
                save_pdf_tables(pdf.path, page_range, options.get('mode'))
        else:
            pdf_path = os.path.join(arrondissements_folder, pdf_name)
            save_pdf_tables(pdf_path, page_range, options.get('mode'))
