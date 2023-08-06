# -*- coding: utf-8 -*-
from collective.volto.cookieconsent.interfaces import (
    ICookieConsentControlpanel,
)
from plone.restapi.deserializer import json_body
from plone.restapi.deserializer.controlpanels import (
    ControlpanelDeserializeFromJson,
)
from plone.restapi.deserializer.blocks import path2uid
from plone.restapi.interfaces import IDeserializeFromJson
from Products.CMFPlone.utils import safe_unicode
from zExceptions import BadRequest
from zope.component import adapter
from zope.interface import implementer

import json
import lxml


@implementer(IDeserializeFromJson)
@adapter(ICookieConsentControlpanel)
class CookieconsentControlpanelDeserializeFromJson(
    ControlpanelDeserializeFromJson
):
    def __call__(self):
        req = json_body(self.controlpanel.request)
        proxy = self.registry.forInterface(
            self.schema, prefix=self.schema_prefix
        )
        errors = []

        configurations = req.get("cookie_consent_configuration", {})
        if not configurations:
            errors.append(
                {
                    "message": "Missing data",
                    "field": "cookie_consent_configuration",
                }
            )
            raise BadRequest(errors)
        try:
            value = self.fix_urls(json.loads(configurations))
            setattr(proxy, "cookie_consent_configuration", json.dumps(value))
        except ValueError as e:
            errors.append(
                {
                    "message": str(e),
                    "field": "cookie_consent_configuration",
                    "error": e,
                }
            )

        if errors:
            raise BadRequest(errors)

    def fix_urls(self, data):
        new_data = {}
        for key, value in data.items():
            new_data[key] = self.convert_internal_links(html=value)
        return new_data

    def convert_internal_links(self, html):
        root = lxml.html.fromstring(html)

        # fix links
        for link in root.xpath("//a"):
            link.set(
                "href", path2uid(context=self.context, link=link.get("href"))
            )

        return safe_unicode(lxml.html.tostring(root))
