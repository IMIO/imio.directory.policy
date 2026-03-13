# -*- coding: utf-8 -*-

from imio.directory.policy.utils import remove_unused_contents
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide unwanted profiles from site-creation and quickinstaller."""
        return [
            "imio.smartweb.common:default",
            "imio.directory.core:default",
            "imio.directory.policy:uninstall",
            "imio.directory.policy:demo",
        ]

    def getNonInstallableProducts(self):
        """Hide unwanted products from site-creation and quickinstaller."""
        return [
            "imio.smartweb.common",
            "imio.directory.core",
            "imio.directory.policy.upgrades",
        ]


def post_install(context):
    """Post install script"""
    portal = api.portal.get()
    remove_unused_contents(portal)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def create_demo_content(context):
    """Create demo entities and contacts."""
    from zope.globalrequest import getRequest
    from zope.globalrequest import setRequest
    from zope.publisher.browser import TestRequest

    _cleanup_request = False
    if getRequest() is None:
        setRequest(
            TestRequest(
                environ={
                    "SERVER_NAME": "nohost",
                    "SERVER_PORT": "80",
                    "HTTP_HOST": "nohost",
                }
            )
        )
        _cleanup_request = True

    try:
        _create_demo_content_inner()
    finally:
        if _cleanup_request:
            setRequest(None)


def _create_demo_content_inner():
    portal = api.portal.get()

    # --- Entity 1: Commune de Namur ---
    entity1 = api.content.create(
        container=portal,
        type="imio.directory.Entity",
        title="Commune de Namur",
        description="Administration communale de la ville de Namur.",
    )
    try:
        api.content.transition(obj=entity1, transition="publish")
    except Exception:
        pass

    # Contact 1-1: Administration communale (organization)
    contact1_1 = api.content.create(
        container=entity1,
        type="imio.directory.Contact",
        title="Administration communale de Namur",
        subtitle="Hôtel de Ville",
        description="Guichet principal de l'administration communale de Namur.",
    )
    contact1_1.type = "organization"
    contact1_1.street = "Esplanade de l'Hôtel de Ville"
    contact1_1.number = "1"
    contact1_1.zipcode = 5000
    contact1_1.city = "Namur"
    contact1_1.country = "be"
    contact1_1.phones = [
        {"label": "Accueil", "type": "work", "number": "+3281246111"},
        {"label": "Fax", "type": "fax", "number": "+3281246112"},
    ]
    contact1_1.mails = [
        {"label": "Contact général", "type": "work", "mail_address": "info@namur.be"},
    ]
    contact1_1.urls = [
        {"type": "website", "url": "https://www.namur.be"},
        {"type": "facebook", "url": "https://www.facebook.com/VilledeNamur"},
    ]
    contact1_1.reindexObject()
    try:
        api.content.transition(obj=contact1_1, transition="publish")
    except Exception:
        pass

    # Contact 1-2: Bourgmestre (position)
    contact1_2 = api.content.create(
        container=entity1,
        type="imio.directory.Contact",
        title="Bourgmestre",
        subtitle="Maxime Prévot",
        description="Cabinet du Bourgmestre de la Ville de Namur.",
    )
    contact1_2.type = "position"
    contact1_2.street = "Esplanade de l'Hôtel de Ville"
    contact1_2.number = "1"
    contact1_2.zipcode = 5000
    contact1_2.city = "Namur"
    contact1_2.country = "be"
    contact1_2.phones = [
        {"label": "Secrétariat", "type": "work", "number": "+3281246200"},
    ]
    contact1_2.mails = [
        {"label": "Cabinet", "type": "work", "mail_address": "bourgmestre@namur.be"},
    ]
    contact1_2.urls = [
        {"type": "website", "url": "https://www.namur.be/bourgmestre"},
    ]
    contact1_2.reindexObject()
    try:
        api.content.transition(obj=contact1_2, transition="publish")
    except Exception:
        pass

    # Contact 1-3: Service Urbanisme (organization)
    contact1_3 = api.content.create(
        container=entity1,
        type="imio.directory.Contact",
        title="Service Urbanisme",
        subtitle="Département aménagement du territoire",
        description=(
            "Le service urbanisme instruit les demandes de permis d'urbanisme "
            "et veille à l'application des règles d'aménagement du territoire."
        ),
    )
    contact1_3.type = "organization"
    contact1_3.street = "Rue de Fer"
    contact1_3.number = "42"
    contact1_3.zipcode = 5000
    contact1_3.city = "Namur"
    contact1_3.country = "be"
    contact1_3.phones = [
        {"label": "Guichet", "type": "work", "number": "+3281246300"},
    ]
    contact1_3.mails = [
        {
            "label": "Demandes permis",
            "type": "work",
            "mail_address": "urbanisme@namur.be",
        },
    ]
    contact1_3.urls = [
        {"type": "website", "url": "https://www.namur.be/urbanisme"},
    ]
    contact1_3.vat_number = "BE0207.717.225"
    contact1_3.reindexObject()
    try:
        api.content.transition(obj=contact1_3, transition="publish")
    except Exception:
        pass

    # --- Entity 2: CPAS de Liège ---
    entity2 = api.content.create(
        container=portal,
        type="imio.directory.Entity",
        title="CPAS de Liège",
        description=(
            "Le Centre Public d'Action Sociale de Liège accompagne les personnes "
            "en difficulté et leur garantit un accès aux droits fondamentaux."
        ),
    )
    try:
        api.content.transition(obj=entity2, transition="publish")
    except Exception:
        pass

    # Contact 2-1: Accueil central (organization)
    contact2_1 = api.content.create(
        container=entity2,
        type="imio.directory.Contact",
        title="CPAS de Liège - Accueil central",
        subtitle="Siège administratif",
        description="Point d'accueil principal du CPAS de Liège.",
    )
    contact2_1.type = "organization"
    contact2_1.street = "Rue Hors-Château"
    contact2_1.number = "11"
    contact2_1.zipcode = 4000
    contact2_1.city = "Liège"
    contact2_1.country = "be"
    contact2_1.phones = [
        {"label": "Accueil", "type": "work", "number": "+3242506111"},
        {"label": "Urgences sociales", "type": "cell", "number": "+32476123456"},
        {"label": "Fax", "type": "fax", "number": "+3242506119"},
    ]
    contact2_1.mails = [
        {"label": "Accueil", "type": "work", "mail_address": "accueil@cpas.liege.be"},
        {"label": "Courrier", "type": "work", "mail_address": "courrier@cpas.liege.be"},
    ]
    contact2_1.urls = [
        {"type": "website", "url": "https://www.cpasdeliege.be"},
        {"type": "facebook", "url": "https://www.facebook.com/CPASdeLiege"},
        {"type": "linkedin", "url": "https://www.linkedin.com/company/cpas-liege"},
    ]
    contact2_1.vat_number = "BE0212.573.346"
    contact2_1.reindexObject()
    try:
        api.content.transition(obj=contact2_1, transition="publish")
    except Exception:
        pass

    # Contact 2-2: Directeur général (position)
    contact2_2 = api.content.create(
        container=entity2,
        type="imio.directory.Contact",
        title="Directeur général",
        subtitle="Direction générale",
        description="Direction générale du CPAS de Liège.",
    )
    contact2_2.type = "position"
    contact2_2.street = "Rue Hors-Château"
    contact2_2.number = "11"
    contact2_2.zipcode = 4000
    contact2_2.city = "Liège"
    contact2_2.country = "be"
    contact2_2.phones = [
        {"label": "Secrétariat", "type": "work", "number": "+3242506200"},
    ]
    contact2_2.mails = [
        {
            "label": "Direction",
            "type": "work",
            "mail_address": "direction@cpas.liege.be",
        },
    ]
    contact2_2.reindexObject()
    try:
        api.content.transition(obj=contact2_2, transition="publish")
    except Exception:
        pass

    # Contact 2-3: Permanence sociale (mission)
    contact2_3 = api.content.create(
        container=entity2,
        type="imio.directory.Contact",
        title="Permanence sociale",
        subtitle="Aide sociale d'urgence",
        description=(
            "La permanence sociale assure une aide immédiate aux personnes "
            "en situation d'urgence sociale, 7j/7."
        ),
    )
    contact2_3.type = "mission"
    contact2_3.street = "Rue Hors-Château"
    contact2_3.number = "11"
    contact2_3.zipcode = 4000
    contact2_3.city = "Liège"
    contact2_3.country = "be"
    contact2_3.phones = [
        {"label": "Urgence 24h/24", "type": "cell", "number": "+32477999888"},
        {"label": "Bureau", "type": "work", "number": "+3242506300"},
    ]
    contact2_3.mails = [
        {
            "label": "Contact",
            "type": "work",
            "mail_address": "permanence@cpas.liege.be",
        },
    ]
    contact2_3.urls = [
        {"type": "website", "url": "https://www.cpasdeliege.be/permanence"},
    ]
    contact2_3.reindexObject()
    try:
        api.content.transition(obj=contact2_3, transition="publish")
    except Exception:
        pass
