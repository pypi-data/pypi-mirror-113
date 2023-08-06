from django.db import models

from .models import create_multicurrency_price_model, MulticurrencyPriceModel


class MultiCurrencyPriceField:
    def contribute_to_class(self, cls, name, **kwargs):
        price_model = create_multicurrency_price_model(cls, name)
