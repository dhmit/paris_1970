from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin


@plugin_pool.register_plugin
class Navbar(CMSPluginBase):
    model = CMSPlugin
    render_template = "cms_navbar.html"
    cache = False
