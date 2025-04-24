from typing import List

from aiogram import Router

from . import captcha_cant_click
from . import captcha_generate
from . import captcha_confirm
from . import captcha_click


routers: List[Router] = [
    captcha_cant_click.router,
    captcha_generate.router,
    captcha_confirm.router,
    captcha_click.router,
]
