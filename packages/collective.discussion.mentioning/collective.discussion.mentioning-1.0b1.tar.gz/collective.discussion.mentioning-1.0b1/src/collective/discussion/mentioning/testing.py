# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.discussion.mentioning


class CollectiveDiscussionMentioningLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.discussion.mentioning)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.discussion.mentioning:default')


COLLECTIVE_DISCUSSION_MENTIONING_FIXTURE = CollectiveDiscussionMentioningLayer()


COLLECTIVE_DISCUSSION_MENTIONING_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_DISCUSSION_MENTIONING_FIXTURE,),
    name='CollectiveDiscussionMentioningLayer:IntegrationTesting',
)


COLLECTIVE_DISCUSSION_MENTIONING_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_DISCUSSION_MENTIONING_FIXTURE,),
    name='CollectiveDiscussionMentioningLayer:FunctionalTesting',
)


COLLECTIVE_DISCUSSION_MENTIONING_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_DISCUSSION_MENTIONING_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveDiscussionMentioningLayer:AcceptanceTesting',
)
