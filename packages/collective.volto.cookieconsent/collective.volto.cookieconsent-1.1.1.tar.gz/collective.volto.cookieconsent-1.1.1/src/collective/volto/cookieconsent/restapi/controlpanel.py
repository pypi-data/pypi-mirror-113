# -*- coding: utf-8 -*-
from collective.volto.cookieconsent.interfaces import (
    ICollectiveVoltoCookieConsentLayer,
)
from collective.volto.cookieconsent.interfaces import ICookieConsentSettings
from collective.volto.cookieconsent.interfaces import (
    ICookieConsentControlpanel,
)
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@adapter(Interface, ICollectiveVoltoCookieConsentLayer)
@implementer(ICookieConsentControlpanel)
class CookieConsentSettingsControlpanel(RegistryConfigletPanel):
    schema = ICookieConsentSettings
    configlet_id = "CookieConsentSettings"
    configlet_category_id = "plone-general"
    schema_prefix = None
