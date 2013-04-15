# -*- coding: utf-8 -*-
import unittest

import transaction
from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
from plone.app.testing import (
    TEST_USER_ID,
    TEST_USER_NAME,
    TEST_USER_PASSWORD,
    setRoles,
)
from collective.portlet.mailman.testing import \
        PORTLET_MAILMAN_FUNCTIONAL_TESTING


class PortletMailmanTest(unittest.TestCase):

    layer = PORTLET_MAILMAN_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.quick_installer = getToolByName(self.portal,
                                             'portal_quickinstaller')
        self.quick_installer.installProduct('collective.portlet.mailman')
        transaction.commit()
        self.browser = Browser(self.app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME,
                TEST_USER_PASSWORD,))

    def test_add_portlet(self):
        portal_url = self.portal.absolute_url()
        self.browser.open(portal_url + '/@@manage-portlets')
        form = self.browser.getForm(index=1)
        field = form.getControl(
            name=':action',
            index=0)
        value = '/++contextportlets++plone.leftcolumn' + \
                '/+/collective.portlet.mailman.Mailman'
        field.value = [value, ]
        form.submit()
        self.browser.getControl(
            name='form.header').value = "testlist header"
        self.browser.getControl(
            name='form.name').value = "TestList"
        self.browser.getControl(
            name='form.address').value = 'nobody@example.org'
        self.browser.getControl(
            name='form.message').value = 'Thank you for subscribing'
        self.browser.getControl(
            name='form.actions.save').click()


#EOF
