import os
import csv

from django.conf import settings
from app.models import Photographer


def format_name(name):
    name = name.title()
    x = name.split()
    result = ""

    # add all names in order but with last name at end
    for i in range(1, len(x)):
        result = result + x[i] + " "

    result = result + x[0]
    return result


def format_ville(ville):
    array = ville.split()
    ville = " ".join(array)
    if ville[:4] == "PARIS":
        return "Paris" + ville[5:]
    return ville.title()


def read_csv():
    Photographer.objects.all().delete()

    filename = os.path.join(settings.BACKEND_DIR, 'data/photographers_full.csv')

    with open(filename, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        # read header so it's not saved to database
        datareader.__next__()
        for row in datareader:
            # skip row if it doesn't start with a number
            try:
                number = int(row[0])
            except ValueError:
                continue

            name, location = format_name(row[1]), format_ville(row[3])
            Photographer.objects.create(number=number, name=name, approx_loc=location)
