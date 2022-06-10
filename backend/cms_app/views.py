"""
These view functions and classes implement API endpoints
"""
from django.shortcuts import render


# app views
def index(request):
    """
    Home page
    """

    return render(request, 'cms_index.html')
