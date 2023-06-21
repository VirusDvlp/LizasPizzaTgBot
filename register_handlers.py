from Handlers import *


def register_handlers(dp):
    register_handlers_reg(dp)
    register_menu_handlers(dp)
    register_order_handlers(dp)
    register_basket_handlers(dp)
    register_admin_handlers(dp)
