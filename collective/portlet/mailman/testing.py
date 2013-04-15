
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting, FunctionalTesting
from zope.configuration import xmlconfig


class PortletMailman(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.portlet.mailman
        xmlconfig.file('configure.zcml',
                       collective.portlet.mailman,
                       context=configurationContext)


PORTLET_MAILMAN_FIXTURE = PortletMailman()
PORTLET_MAILMAN_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PORTLET_MAILMAN_FIXTURE,),
    name="MailmanPortlet:Integration")
PORTLET_MAILMAN_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PORTLET_MAILMAN_FIXTURE,),
    name="MailmanPortlet:Functional")
