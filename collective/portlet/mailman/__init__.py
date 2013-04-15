from Products.CMFCore.permissions import setDefaultRoles
from zope.i18nmessageid import MessageFactory

MailmanMessageFactory = MessageFactory('collective.portlet.mailman')

setDefaultRoles('collective.portlet.mailman: Add Mailman portlet',
                ('Manager', 'Site Administrator', 'Owner', ))
#EOF
