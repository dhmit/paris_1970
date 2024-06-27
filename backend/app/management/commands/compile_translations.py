"""
Django management command launch_site
"""

import io
import os
import shutil

from tqdm import tqdm
from translate_po.main import (
    recognize_po_file, read_lines,
    translate as translate_line
)

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command

def save_lines(file: str, lines: list):
    """ Save lines from memory into a file.
     :parameter file:
     :parameter lines:
     """
    with io.open(file, 'w', encoding='utf8') as infile:
        infile.write("""
msgid ""
msgstr ""
""")
        for keys, values in lines.metadata.items():
            infile.write(f'"{keys}:{values}\\n"\n')
        infile.write('\n')
        for line in lines:
            infile.write(line.__unicode__())

def translate(fro, to, src_dir, dest_dir, fuzzy=False):
    # Work around using parser-based translate_po.main.run function
    # due to conflict with Django BaseCommand parser
    class Arguments:
        def __init__(self, **kwargs):
            [setattr(self, attr, val) for attr, val in kwargs.items()]
    
    arguments = Arguments(fro=fro, to=to, src=src_dir, dest=dest_dir)
    
    for file in os.listdir(src_dir):
        if not recognize_po_file(file):
            continue
        old_file = os.path.join(arguments.dest, file)
        new_file = os.path.join(arguments.src, file)

        print(f"Translating {old_file}...")
        entries = read_lines(old_file)
        for entry in tqdm(entries):
            if entry.translated() or entry.obsolete or entry.fuzzy:
                continue
            line_parts = entry.msgid.split('\n')
            translated_line_parts = [(
                translate_line(line_part, arguments)
                if line_part.strip(" ") else line_part
            ) for line_part in line_parts]            
            entry.msgstr = '\n'.join(translated_line_parts)
            if fuzzy:
                entry.flags.append("fuzzy")

        save_lines(new_file, entries)


class Command(BaseCommand):
    """
    Custom django-admin command to build project translation

    https://testdriven.io/blog/multiple-languages-in-django/
    """

    help = "Custom django-admin command to compile translations in translation_db.py"

    def add_arguments(self, parser):
        parser.add_argument("--no_auto_trans", action="store_true")
        parser.add_argument("--rebuild", action="store_true")
        parser.add_argument(
            "--main_lang", type=str, action="store", default="en"
        )
        parser.add_argument(
            "--mark_fuzzy", action="store_true",
            help="Mark auto-translations as fuzzy"
        )

    def handle(self, *args, **options):
        no_auto_translate: bool = options.get("no_auto_trans")
        main_lang: str = options.get("main_lang")
        rebuild: bool = options.get("rebuild")
        mark_fuzzy: bool = options.get("mark_fuzzy")

        def iter_locale_paths():
            for locale_path in settings.LOCALE_PATHS:
                for language_code, _ in settings.LANGUAGES:
                    yield locale_path, language_code
        
        # Make locale paths
        for locale_path, language_code in iter_locale_paths():
            messages_path = os.path.join(locale_path, language_code)
            if rebuild and os.path.exists(messages_path):
                shutil.rmtree(messages_path)
            os.makedirs(
                messages_path,
                exist_ok=True
            )
        
        call_command("makemessages", all=True, ignore=["env"])
        if not no_auto_translate:
            for locale_path, language_code in iter_locale_paths():
                if language_code == main_lang:
                    continue
                po_dir = os.path.join(locale_path, language_code, "LC_MESSAGES")
                translate(
                    fro=main_lang, to=language_code,
                    src_dir=po_dir, dest_dir=po_dir,
                    fuzzy=mark_fuzzy
                )
        call_command("compilemessages", ignore=["env"])
