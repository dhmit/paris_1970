"""
Miscellaneous utility functions useful throughout the system
"""
from textwrap import dedent

from django.shortcuts import render


def render_react_view(request, component_name=None, **url_props):
    """
    A view function to render views that are entirely managed
    in the frontend by a single React component. This lets us use
    Django url routing with React components.

    :param request: Django request object to pass through
    :param component_name: name of the React component to render into the 'root' div
                           of backend/templates/index.html
    :param url_props: props to pass into the React component, consumed from Django's url parser
    :return:
    """
    template = 'index.html'
    context = {
        'component_name': component_name,
        'props': url_props,
    }
    return render(request, template, context)


def print_header(header_str):
    """
    Print a header -- mostly for our command line tools.
    """
    print(dedent(f'''
        ################################################################################
        # {header_str}
        ################################################################################'''))
