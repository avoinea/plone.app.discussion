import unittest

from zope.component import createObject

from Products.PloneTestCase.ptc import PloneTestCase
from plone.app.discussion.tests.layer import DiscussionLayer

from plone.app.discussion.interfaces import IComment, IConversation, IReplies

class CommentTest(PloneTestCase):

    layer = DiscussionLayer

    def afterSetUp(self):
        # First we need to create some content.
        self.loginAsPortalOwner()
        typetool = self.portal.portal_types
        typetool.constructContent('Document', self.portal, 'doc1')

    def test_factory(self):
        comment1 = createObject('plone.Comment')
        self.assert_(IComment.providedBy(comment1))

    def test_id(self):
        comment1 = createObject('plone.Comment')
        comment1.comment_id = 123
        self.assertEquals('123', comment1.id)
        self.assertEquals('123', comment1.getId())
        self.assertEquals(u'123', comment1.__name__)

    def test_title(self):
        comment1 = createObject('plone.Comment')
        comment1.title = "New title"
        self.assertEquals("New title", comment1.Title())

    def test_creator(self):
        comment1 = createObject('plone.Comment')
        comment1.creator = "Jim"
        self.assertEquals("Jim", comment1.Creator())

    def test_traversal(self):
        # make sure comments are traversable, have an id, absolute_url and physical path

        conversation = IConversation(self.portal.doc1).__of__(self.portal.doc1)

        comment1 = createObject('plone.Comment')
        comment1.title = 'Comment 1'
        comment1.text = 'Comment text'

        new_comment1_id = conversation.addComment(comment1)

        comment = self.portal.doc1.restrictedTraverse('++conversation++default/%s' % new_comment1_id)
        self.assert_(IComment.providedBy(comment))
        self.assertEquals('Comment 1', comment.title)

        self.assertEquals(('', 'plone', 'doc1', '++conversation++default', str(new_comment1_id)), comment.getPhysicalPath())
        self.assertEquals('plone/doc1/%2B%2Bconversation%2B%2Bdefault/' + str(new_comment1_id), comment.absolute_url())

    def test_workflow(self):
        self.portal.portal_workflow.setChainForPortalTypes(('Discussion Item',), ('simple_publication_workflow,'))

        conversation = IConversation(self.portal.doc1).__of__(self.portal.doc1)
        comment1 = createObject('plone.Comment')
        new_comment1_id = conversation.addComment(comment1)

        comment = conversation[new_comment1_id]

        chain = self.portal.portal_workflow.getChainFor(comment)
        self.assertEquals(('simple_publication_workflow',), chain)

        # ensure the initial state was entered and recorded
        self.assertEquals(1, len(comment.workflow_history['simple_publication_workflow']))
        self.assertEquals(None, comment.workflow_history['simple_publication_workflow'][0]['action'])

        self.assertEquals('private', self.portal.portal_workflow.getInfoFor(comment, 'review_state'))

    def test_fti(self):
        # test that we can look up an FTI for Discussion Item

        self.assert_("Discussion Item" in self.portal.portal_types.objectIds())

        comment1 = createObject('plone.Comment')

        fti = self.portal.portal_types.getTypeInfo(comment1)
        self.assertEquals('Discussion Item', fti.getTypeInfo(comment1).getId())

class RepliesTest(PloneTestCase):

    # test the IReplies adapter on a comment

    layer = DiscussionLayer

    def afterSetUp(self):
        # First we need to create some content.
        self.loginAsPortalOwner()
        typetool = self.portal.portal_types
        typetool.constructContent('Document', self.portal, 'doc1')

    def test_add_comment(self):
        # Add comments to a CommentReplies adapter

        # Create a conversation. In this case we doesn't assign it to an
        # object, as we just want to check the Conversation object API.
        conversation = IConversation(self.portal.doc1)

        # Pretend that we have traversed to the comment by aq wrapping it.
        conversation = conversation.__of__(self.portal.doc1)

        # Add a comment to the conversation
        replies = IReplies(conversation)

        comment = createObject('plone.Comment')
        comment.title = 'Comment 1'
        comment.text = 'Comment text'

        new_id = replies.addComment(comment)

        # Add a reply to the CommentReplies adapter of the first comment
        re_comment = createObject('plone.Comment')
        re_comment.title = 'Re: Comment 1'
        re_comment.text = 'Comment text'

        replies = IReplies(comment)

        new_re_id = replies.addComment(re_comment)

        # check that replies provides the IReplies interface
        self.assert_(IReplies.providedBy(replies))

        # Make sure our comment was added
        self.failUnless(new_re_id in replies)

        # Make sure it is also reflected in the conversation
        self.failUnless(new_re_id in conversation)

        # Make sure the conversation has the correct comment id
        self.assertEquals(conversation[new_re_id].comment_id, new_re_id)

    def test_delete_comment(self):
        pass

    def test_dict_api(self):
        # ensure all operations use only top-level comments
        pass

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)