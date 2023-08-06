# -*- coding: utf-8 -*-
from collective.volto.cookieconsent.interfaces import ICookieConsentSettings
from collective.volto.cookieconsent.testing import (
    VOLTO_COOKIECONSENT_API_FUNCTIONAL_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession
from transaction import commit

import json
import unittest


class SocialSettingsControlpanelTest(unittest.TestCase):

    layer = VOLTO_COOKIECONSENT_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        self.controlpanel_url = "/@controlpanels/cookieconsent-settings"

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.page = api.content.create(
            container=self.portal, type="Document", title="A page"
        )
        commit()

    def tearDown(self):
        self.api_session.close()

    def get_record_value(self):
        record = api.portal.get_registry_record(
            "cookie_consent_configuration",
            interface=ICookieConsentSettings,
            default="",
        )
        if not record:
            return []
        return json.loads(record)

    def test_controlpanel_exists(self):
        response = self.api_session.get(self.controlpanel_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get("Content-Type"), "application/json"
        )

    def test_controlpanel_listed(self):
        response = self.api_session.get("/@controlpanels")

        titles = [x.get("title") for x in response.json()]
        self.assertIn("Cookie Consent Settings", titles)

    def test_deserializer_convert_internal_links_in_resolveuid(self):

        data = {
            "it": '<p>Text with <a href="{}">link</a></p>'.format(
                self.page.absolute_url()
            )
        }
        self.api_session.patch(
            self.controlpanel_url,
            json={"cookie_consent_configuration": json.dumps(data)},
        )
        commit()
        record = self.get_record_value()

        self.assertIn("resolveuid/{}".format(self.page.UID()), record["it"])
        self.assertNotIn(self.page.absolute_url(), record["it"])

    def test_serializer_convert_resolveuids_in_proper_links(self):

        data = {
            "it": '<p>Text with <a href="{}">link</a></p>'.format(
                self.page.absolute_url()
            )
        }
        self.api_session.patch(
            self.controlpanel_url,
            json={"cookie_consent_configuration": json.dumps(data)},
        )
        commit()

        record = self.get_record_value()
        response = self.api_session.get(self.controlpanel_url)
        res = response.json()

        self.assertIn("resolveuid/{}".format(self.page.UID()), record["it"])
        self.assertNotIn(
            "resolveuid/{}".format(self.page.UID()),
            res["data"]["cookie_consent_configuration"],
        )
        self.assertIn(
            self.page.absolute_url(),
            res["data"]["cookie_consent_configuration"],
        )
