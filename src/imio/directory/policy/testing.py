# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from plone.testing.zope import addRequestContainer
from z3c.form.interfaces import IFormLayer
from zope.globalrequest import setRequest
from zope.interface import alsoProvides

import imio.directory.policy
import plone.restapi


class ImioDirectoryPolicyLayer(PloneSandboxLayer):
    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=imio.directory.policy)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "imio.directory.policy:default")


IMIO_DIRECTORY_POLICY_FIXTURE = ImioDirectoryPolicyLayer()


IMIO_DIRECTORY_POLICY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(IMIO_DIRECTORY_POLICY_FIXTURE,),
    name="ImioDirectoryPolicyLayer:IntegrationTesting",
)


IMIO_DIRECTORY_POLICY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(IMIO_DIRECTORY_POLICY_FIXTURE,),
    name="ImioDirectoryPolicyLayer:FunctionalTesting",
)


IMIO_DIRECTORY_POLICY_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        IMIO_DIRECTORY_POLICY_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="ImioDirectoryPolicyLayer:AcceptanceTesting",
)


class ImioDirectoryPolicyDemoLayer(PloneSandboxLayer):
    defaultBases = (IMIO_DIRECTORY_POLICY_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=imio.directory.policy)

    def setUpPloneSite(self, portal):
        # Entity creation triggers added_entity() which calls configure_faceted()
        # (needs a request for redirect) and then calls z3c.form widget adapters
        # (needs IFormLayer on the request). During setUpPloneSite the raw
        # portal.REQUEST hasn't gone through Plone traversal so browser layers
        # are missing. We create a fresh request container and manually apply
        # IFormLayer since unrestrictedTraverse does not fire IBeforeTraverseEvent.
        app = addRequestContainer(
            portal.getPhysicalRoot(),
            environ={"SERVER_NAME": "foo", "SERVER_PORT": "80"},
        )
        request = app.REQUEST
        alsoProvides(request, IFormLayer)
        setRequest(request)
        try:
            applyProfile(portal, "imio.directory.policy:demo")
        finally:
            setRequest(None)


IMIO_DIRECTORY_POLICY_DEMO_FIXTURE = ImioDirectoryPolicyDemoLayer()


IMIO_DIRECTORY_POLICY_DEMO_INTEGRATION_TESTING = IntegrationTesting(
    bases=(IMIO_DIRECTORY_POLICY_DEMO_FIXTURE,),
    name="ImioDirectoryPolicyDemoLayer:IntegrationTesting",
)
