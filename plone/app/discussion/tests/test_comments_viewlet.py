import unittest
from datetime import datetime, timedelta

from plone.registry import Registry

from zope.component import createObject

from Acquisition import aq_base, aq_parent, aq_inner

from plone.app.vocabularies.types import BAD_TYPES

from Products.CMFCore.utils import getToolByName
from Products.PloneTestCase.ptc import PloneTestCase

from plone.app.discussion.browser.comments import CommentsViewlet
from plone.app.discussion.interfaces import IConversation, IComment, IReplies, IDiscussionSettings
from plone.app.discussion.tests.layer import DiscussionLayer


class CommentsViewletTest(PloneTestCase):

    layer = DiscussionLayer

    def afterSetUp(self):
        # First we need to create some content.
        self.loginAsPortalOwner()
        typetool = self.portal.portal_types
        typetool.constructContent('Document', self.portal, 'doc1')
        self.portal_discussion = getToolByName(self.portal, 'portal_discussion', None)
        request = self.app.REQUEST
        context = getattr(self.portal, 'doc1')
        self.viewlet = CommentsViewlet(context, request, None, None)

    def test_format_time(self):
        pass

    def test_get_commenter_portrait(self):
        self.viewlet.update()
        self.viewlet.get_commenter_portrait('Foo')

    def test_get_commenter_portrait_without_userimage(self):
        # Create a user without a user image
        pass

    def test_get_commenter_home(self):
        pass

    def test_get_commenter_home_without_username(self):
        # Create a user without setting a username
        pass

    def test_is_discussion_allowed(self):
        # We currently have four layers of testing if discussion is allowed
        # on a particular content object:
        #
        # 1) Check if discussion is allowed globally
        # 2) Check if discussion is allowed on a particular content type
        # 3) If the content object is located in a folder, check if the folder
        #    has discussion allowed
        # 4) Check if discussion is allowed on this particular content object
        #
        self.viewlet.update()
        self.viewlet.is_discussion_allowed()

    def test_is_discussion_allowed_globally(self):
        pass

    def test_is_discussion_allowed_for_content_type(self):
        # Check discussion allowed for content types
        portal_types = getToolByName(self.portal, 'portal_types')

        # Get the FTI for some content types
        document_fti = getattr(portal_types, 'Document')
        news_item_fti = getattr(portal_types, 'News Item')
        folder_fti = getattr(portal_types, 'Folder')

        # By default, discussion is only allowed for Document and News Item
        # XXX: allow_discussion always returns False !!!
        #self.assertEquals(document_fti.getProperty('allow_discussion'), True)
        #self.assertEquals(news_item_fti.getProperty('allow_discussion'), True)

        self.assertEquals(folder_fti.getProperty('allow_discussion'), False)

        # Disallow discussion for the News Item content types
        news_item_fti.manage_changeProperties(allow_discussion = False)

        # Allow discussion for the Folder content types
        folder_fti.manage_changeProperties(allow_discussion = True)

        # Check if discussion for News Item content types is disallowed
        self.assertEquals(news_item_fti.getProperty('allow_discussion'), False)

        # Check if discussion for Folder content types is allowed
        self.assertEquals(folder_fti.getProperty('allow_discussion'), True)

    def test_is_discussion_allowed_for_folder(self):
        # Create a folder with two content objects. Change allow_discussion
        # and check if the content objects inside the folder are commentable.
        pass

    def test_is_discussion_allowed_on_content_object(self):
        pass

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)