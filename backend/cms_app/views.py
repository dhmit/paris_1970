"""
These view functions and classes implement API endpoints
"""
from django.shortcuts import render
from cms.models import Title, Placeholder, Page


def get_page_text(page, slot='content'):
    """
    Function used to get all the text of a specified placeholder slot from a page
    :param page: Django cms Title instance
    :param slot: The name of the placeholder slot to pull text from
    :return: string of concatenated raw html from TextPlugins in the specified placeholder slot
    """
    placeholders = Placeholder.objects.filter(page__id=page.page_id)
    text = ''
    for placeholder in placeholders:
        if placeholder.slot != slot:
            continue
        # Sort plugins into the order they appear on the page
        sorted_plugins = sorted(placeholder.get_plugins(), key=lambda plgn: plgn.position)
        for plugin in sorted_plugins:
            # Ignore plugin types other than text in the specified slot type
            if plugin.plugin_type != 'TextPlugin':
                continue
            text += plugin.djangocms_text_ckeditor_text.body
    return text


# app views
def index(request):
    """
    Home page
    """
    pages = []
    for page in Title.objects.filter(publisher_is_draft=0, published=1):
        # Assumes all relevant text is in page's content slot (ignore navbar slot)
        text = get_page_text(page, slot='content')
        pages.append({
            'title': page.title,
            'url': Page.objects.get(id=page.page_id).get_absolute_url(),
            'content': text
        })
    context = {
        'website_pages': pages
    }
    return render(request, 'cms_index.html', context)
