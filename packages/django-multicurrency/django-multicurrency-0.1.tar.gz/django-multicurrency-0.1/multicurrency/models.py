from django.conf import settings
from django.db import models
from django.utils.translation import gettext, gettext_lazy as _
import sys

from .signals import price_pre_save_signal


CURRENCIES = [(currency_title.lower(), currency_title) 
               for currency_title in settings.MULTICURRENCY_CURRENCIES]


def create_multicurrency_price_model(shared_model, related_name):
    meta = {}
    capitalized_field_name = ''.join([ s.capitalize() for s in related_name.split('_') ])

    if shared_model._meta.abstract:
        raise TypeError("Can't create MulticurrencyPriceModel for abstract class {0}".format(shared_model.__name__))

    meta['app_label'] = shared_model._meta.app_label
    meta['db_tablespace'] = shared_model._meta.db_tablespace
    meta['managed'] = shared_model._meta.managed
    meta.setdefault('db_table', f'{shared_model._meta.db_table}_{related_name}')
    meta.setdefault('default_permissions', ())

    name = str(f'{shared_model.__name__}{capitalized_field_name}')

    attrs = {}
    attrs['Meta'] = type(str('Meta'), (object,), meta)
    attrs['__module__'] = shared_model.__module__
    attrs['objects'] = models.Manager()
    attrs['master'] = models.OneToOneField(shared_model, 
                                           editable=False, 
                                           on_delete=models.CASCADE,
                                           related_name=related_name)

    # add columns for each currency
    for currency in settings.MULTICURRENCY_CURRENCIES:
        attrs[f'{currency.lower()}_amount'] = models.FloatField(
                                                    _('Amount'), 
                                                    blank=True, 
                                                    null=False)

    price_model = models.base.ModelBase(name, (MulticurrencyPriceModel,), attrs)

    mod = sys.modules[shared_model.__module__]
    setattr(mod, name, price_model)
    models.signals.pre_save.connect(price_pre_save_signal, price_model)

    return price_model


class MulticurrencyPriceModel(models.Model, metaclass=models.base.ModelBase):
    currency = models.CharField(_('Currency'),
                                max_length=3,
                                choices=CURRENCIES,
                                db_index=True)

    class Meta:
        abstract = True
        default_permissions = ()

