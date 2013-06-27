from plone import api
from zope import schema
from zope import interface
from zope.formlib import form
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import \
        ViewPageTemplateFile
from collective.portlet.mailman import MailmanMessageFactory as _
from five import grok
from plone.directives import form as ploneform
from z3c.form import button
from Products.validation import validation


class IMailmanPortlet(IPortletDataProvider):
    header = schema.TextLine(
        title=_(u"Header"),
        description=_(u"Header of the portlet"),
        required=True,
    )

    name = schema.TextLine(
        title=_(u"List name"),
        description=_(u"Descriptive name of the list"),
        required=False,
    )

    address = schema.TextLine(
        title=_(u"Mailman address"),
        description=_(u"Address used to subscribe to the list"),
        required=True,
    )

    subj = schema.Text(
        title=_(u"Description of mailinglist"),
        description=_(u"Descriptive text shown in the portlet"),
        required=False,
    )
    message = schema.Text(
        title=_(u"Subscription message"),
        description=_(u"Message displayed after subscribing"),
        required=False,
    )


class Assignment(base.Assignment):
    interface.implements(IMailmanPortlet)

    header = u""
    name = u""
    address = u""
    subj = u""
    message = u""

    def __init__(
        self, header=u"", name=u"", address=u"", subj=u"", message=u""
    ):
        self.header = header
        self.name = name
        self.address = address
        self.subj = subj
        self.message = message

    @property
    def title(self):
        return self.header or _(u'mailman portlet')


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('mailman.pt')
    showform = True

    @property
    def available(self):
        return True

    def form(self):
        if self.showform:
            raw_form = SubscriptionForm(self.context, self.request)
            raw_form.update()
            return raw_form


class AddForm(base.AddForm):
    form_fields = form.Fields(IMailmanPortlet)
    label = _(u"Add Mailman Portlet")
    descriptioin = _(u"This portlet displays a mailman subscription form.")

    def create(self, data):
        assignment = Assignment()
        form.applyChanges(assignment, self.form_fields, data)
        return assignment


class EditForm(base.EditForm):
    form_fields = form.Fields(IMailmanPortlet)
    label = _(u"Edit Mailman Portlet")
    description = _(u"This portlet displays a mailman subscription form.")


# the subscription form

def validateEmail(value):
    validator = validation.validatorFor('isEmail')
    if validator(str(value)) != 1:
        raise interface.Invalid(_(u"Email address is invalid"))
    return True


class ISubscription(ploneform.Schema):
    email = schema.TextLine(
        title=_(u"E-mail address"),
        description=_(u"E-mail address you wish to subscribe."),
        required=True,
        constraint=validateEmail,
    )


class SubscriptionForm(ploneform.SchemaForm):
    grok.name('subscription-form')
    grok.require('zope2.View')

    schema = ISubscription
    ignoreContext = True

    @button.buttonAndHandler(_(u'Subscribe'))
    def handle_subscribe_action(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        api.portal.send_email(
            recipient=self.context.data.address,
            sender=data.get('email'),
            subject='subscribe',
            body='subscribe %s' % data.get('email'),
        )
        self.status = self.context.data.message




#EOF
