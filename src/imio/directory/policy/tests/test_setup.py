# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from imio.directory.policy.testing import IMIO_DIRECTORY_POLICY_INTEGRATION_TESTING
from imio.directory.policy.utils import setup_multilingual_site
from plone import api
from plone.app.multilingual.api import is_translatable
from plone.app.testing import setRoles, TEST_USER_ID
from Products.CMFPlone.interfaces import ILanguage
from Products.CMFPlone.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):
    """Test that imio.directory.policy is properly installed."""

    layer = IMIO_DIRECTORY_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if imio.directory.policy is installed."""
        self.assertTrue(self.installer.is_product_installed("imio.directory.policy"))

    def test_browserlayer(self):
        """Test that IImioDirectoryPolicyLayer is registered."""
        from imio.directory.policy.interfaces import IImioDirectoryPolicyLayer
        from plone.browserlayer import utils

        self.assertIn(IImioDirectoryPolicyLayer, utils.registered_layers())

    def test_multilingual(self):
        self.assertIn("fr", self.portal.objectIds())
        self.assertIn("nl", self.portal.objectIds())

        # no LIF folders
        self.assertEqual(len(self.portal.fr.objectIds()), 0)
        self.assertEqual(len(self.portal.nl.objectIds()), 0)

        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        entity = api.content.create(
            container=self.portal,
            type="imio.directory.Entity",
            id="entity",
        )
        api.content.create(
            container=entity,
            type="imio.directory.Contact",
            id="contact",
        )
        setup_multilingual_site(self.portal)
        self.assertNotIn("entity", self.portal.objectIds())
        self.assertIn("entity", self.portal.fr.objectIds())
        entity = self.portal.fr.entity
        self.assertIn("contact", entity.objectIds())
        contact = entity.contact
        self.assertTrue(is_translatable(contact))
        self.assertEquals(ILanguage(contact).get_language(), "fr")


class TestUninstall(unittest.TestCase):

    layer = IMIO_DIRECTORY_POLICY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("imio.directory.policy")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if imio.directory.policy is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("imio.directory.policy"))

    def test_browserlayer_removed(self):
        """Test that IImioDirectoryPolicyLayer is removed."""
        from imio.directory.policy.interfaces import IImioDirectoryPolicyLayer
        from plone.browserlayer import utils

        self.assertNotIn(IImioDirectoryPolicyLayer, utils.registered_layers())
