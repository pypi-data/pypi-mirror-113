# -*- coding: utf-8 -*-
from collective.volto.cookieconsent.interfaces import (
    ICookieConsentControlpanel,
)
from plone import api
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.controlpanels import ControlpanelSerializeToJson
from plone.restapi.serializer.converters import json_compatible
from zope.component import adapter
from zope.interface import implementer

import json

KEYS_WITH_URL = ["linkUrl", "navigationRoot", "showMoreLink"]


def serialize_data(json_data):
    if not json_data:
        return ""
    data = json.loads(json_data)
    new_data = {}
    portal = api.portal.get()
    transforms = api.portal.get_tool(name="portal_transforms")
    for key, value in data.items():
        data = transforms.convertTo(
            "text/x-html-safe", value, mimetype="text/html", context=portal,
        )
        new_data[key] = data.getData()
    return json_compatible(new_data)


@implementer(ISerializeToJson)
@adapter(ICookieConsentControlpanel)
class CookieconsentControlpanelSerializeToJson(ControlpanelSerializeToJson):
    def __call__(self):
        json_data = super(
            CookieconsentControlpanelSerializeToJson, self
        ).__call__()
        conf = json_data["data"].get("cookie_consent_configuration", "")
        if conf:
            json_data["data"]["cookie_consent_configuration"] = json.dumps(
                serialize_data(json_data=conf)
            )
        return json_data
