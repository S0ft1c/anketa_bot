from .create_order_callback_handler import create_order_router
from .after_date_handler import after_date_router
from .after_how_many_ppl_handler import after_how_many_ppl_router
from .after_address_handler import after_address_handler_router
from .after_work_desc_handler import after_work_desc_router
from .after_payment_handler import after_payment_router
from .after_help_phone_handler import after_help_phone_router
from .after_FULL_address_handler import after_full_address_router
from .after_FULL_work_desc import after_full_work_desc_router
from .after_FULL_phones import after_FULL_phones_router
from .after_FULL_additional_info import after_full_additional_info_router
from .yes_long_time_handler import yes_long_time_router
from .no_long_time_handler import no_long_time_router
from .long_day_handler import long_day_router
from aiogram import Router

create_order_handlers_router = Router()

# include routers
create_order_handlers_router.include_routers(
    create_order_router,
    after_date_router,
    after_how_many_ppl_router,
    after_address_handler_router,
    after_work_desc_router,
    after_payment_router,
    after_help_phone_router,
    after_full_address_router,
    after_full_work_desc_router,
    after_FULL_phones_router,
    after_full_additional_info_router,
    yes_long_time_router,
    no_long_time_router,
    long_day_router

)
