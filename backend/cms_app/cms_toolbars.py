from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.cms_toolbars import ADMIN_MENU_IDENTIFIER


@toolbar_pool.register
class MyToolbarClass(CMSToolbar):
    [...]

    def populate(self):
        self.toolbar.add_link_item(  # or add_button(), add_modal_item(), etc
            name='Home',
            url=''
        )

        admin_menu = self.toolbar.get_menu(ADMIN_MENU_IDENTIFIER)

        admin_menu.name = "Site"
