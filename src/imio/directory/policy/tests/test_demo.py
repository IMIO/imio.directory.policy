# -*- coding: utf-8 -*-
"""Tests for the demo profile content."""

from imio.directory.policy.testing import (
    IMIO_DIRECTORY_POLICY_DEMO_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class TestDemoContent(unittest.TestCase):
    """Test that the demo profile creates the expected entities and contacts."""

    layer = IMIO_DIRECTORY_POLICY_DEMO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    # --- Entities ---

    def test_two_entities_created(self):
        entities = api.content.find(portal_type="imio.directory.Entity")
        self.assertEqual(len(entities), 2)

    def test_entity_namur_exists(self):
        results = api.content.find(
            portal_type="imio.directory.Entity",
            Title="Commune de Namur",
        )
        self.assertEqual(len(results), 1)

    def test_entity_liege_exists(self):
        results = api.content.find(
            portal_type="imio.directory.Entity",
            Title="CPAS de Liège",
        )
        self.assertEqual(len(results), 1)

    def test_entities_are_published(self):
        entities = api.content.find(portal_type="imio.directory.Entity")
        for brain in entities:
            self.assertEqual(
                brain.review_state,
                "published",
                f"Entity '{brain.Title}' is not published",
            )

    # --- Contacts count ---

    def test_namur_has_three_contacts(self):
        entity = api.content.find(
            portal_type="imio.directory.Entity",
            Title="Commune de Namur",
        )[0].getObject()
        contacts = api.content.find(
            context=entity,
            portal_type="imio.directory.Contact",
        )
        self.assertEqual(len(contacts), 3)

    def test_liege_has_three_contacts(self):
        entity = api.content.find(
            portal_type="imio.directory.Entity",
            Title="CPAS de Liège",
        )[0].getObject()
        contacts = api.content.find(
            context=entity,
            portal_type="imio.directory.Contact",
        )
        self.assertEqual(len(contacts), 3)

    def test_all_contacts_are_published(self):
        contacts = api.content.find(portal_type="imio.directory.Contact")
        for brain in contacts:
            self.assertEqual(
                brain.review_state,
                "published",
                f"Contact '{brain.Title}' is not published",
            )

    # --- Namur contacts ---

    def _get_namur_contact(self, title):
        entity = api.content.find(
            portal_type="imio.directory.Entity",
            Title="Commune de Namur",
        )[0].getObject()
        results = api.content.find(
            context=entity,
            portal_type="imio.directory.Contact",
            Title=title,
        )
        self.assertEqual(
            len(results), 1, f"Contact '{title}' not found in Namur entity"
        )
        return results[0].getObject()

    def test_namur_contact_administration_type(self):
        contact = self._get_namur_contact("Administration communale de Namur")
        self.assertEqual(contact.type, "organization")

    def test_namur_contact_administration_address(self):
        contact = self._get_namur_contact("Administration communale de Namur")
        self.assertEqual(contact.zipcode, 5000)
        self.assertEqual(contact.city, "Namur")
        self.assertEqual(contact.country, "be")

    def test_namur_contact_administration_phones(self):
        contact = self._get_namur_contact("Administration communale de Namur")
        self.assertEqual(len(contact.phones), 2)
        phone_types = {p["type"] for p in contact.phones}
        self.assertIn("work", phone_types)
        self.assertIn("fax", phone_types)

    def test_namur_contact_administration_mails(self):
        contact = self._get_namur_contact("Administration communale de Namur")
        self.assertEqual(len(contact.mails), 1)
        self.assertEqual(contact.mails[0]["mail_address"], "info@namur.be")

    def test_namur_contact_administration_urls(self):
        contact = self._get_namur_contact("Administration communale de Namur")
        self.assertEqual(len(contact.urls), 2)
        url_types = {u["type"] for u in contact.urls}
        self.assertIn("website", url_types)
        self.assertIn("facebook", url_types)

    def test_namur_contact_bourgmestre_type(self):
        contact = self._get_namur_contact("Bourgmestre")
        self.assertEqual(contact.type, "position")

    def test_namur_contact_urbanisme_type(self):
        contact = self._get_namur_contact("Service Urbanisme")
        self.assertEqual(contact.type, "organization")

    def test_namur_contact_urbanisme_vat(self):
        contact = self._get_namur_contact("Service Urbanisme")
        self.assertEqual(contact.vat_number, "BE0207.717.225")

    # --- Liège contacts ---

    def _get_liege_contact(self, title):
        entity = api.content.find(
            portal_type="imio.directory.Entity",
            Title="CPAS de Liège",
        )[0].getObject()
        results = api.content.find(
            context=entity,
            portal_type="imio.directory.Contact",
            Title=title,
        )
        self.assertEqual(
            len(results), 1, f"Contact '{title}' not found in Liège entity"
        )
        return results[0].getObject()

    def test_liege_contact_accueil_type(self):
        contact = self._get_liege_contact("CPAS de Liège - Accueil central")
        self.assertEqual(contact.type, "organization")

    def test_liege_contact_accueil_address(self):
        contact = self._get_liege_contact("CPAS de Liège - Accueil central")
        self.assertEqual(contact.zipcode, 4000)
        self.assertEqual(contact.city, "Liège")
        self.assertEqual(contact.country, "be")

    def test_liege_contact_accueil_three_phones(self):
        contact = self._get_liege_contact("CPAS de Liège - Accueil central")
        self.assertEqual(len(contact.phones), 3)
        phone_types = {p["type"] for p in contact.phones}
        self.assertIn("work", phone_types)
        self.assertIn("cell", phone_types)
        self.assertIn("fax", phone_types)

    def test_liege_contact_accueil_two_mails(self):
        contact = self._get_liege_contact("CPAS de Liège - Accueil central")
        self.assertEqual(len(contact.mails), 2)

    def test_liege_contact_accueil_three_urls(self):
        contact = self._get_liege_contact("CPAS de Liège - Accueil central")
        self.assertEqual(len(contact.urls), 3)
        url_types = {u["type"] for u in contact.urls}
        self.assertIn("website", url_types)
        self.assertIn("facebook", url_types)
        self.assertIn("linkedin", url_types)

    def test_liege_contact_directeur_type(self):
        contact = self._get_liege_contact("Directeur général")
        self.assertEqual(contact.type, "position")

    def test_liege_contact_permanence_type(self):
        contact = self._get_liege_contact("Permanence sociale")
        self.assertEqual(contact.type, "mission")

    def test_liege_contact_permanence_two_phones(self):
        contact = self._get_liege_contact("Permanence sociale")
        self.assertEqual(len(contact.phones), 2)
        phone_types = {p["type"] for p in contact.phones}
        self.assertIn("cell", phone_types)
        self.assertIn("work", phone_types)
