from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.controlpanel import IMailSchema
from Products.CMFPlone.utils import safe_unicode
from collective.discussion.mentioning import _
from plone import api
from plone.registry.interfaces import IRegistry
from smtplib import SMTPException
from zope.component import queryUtility, getUtility
from zope.i18n import translate
from zope.i18nmessageid import Message
import logging
import six

logger = logging.getLogger('plone.app.discussion - collective.discussion.mentioning patch')


MAIL_NOTIFICATION_MESSAGE_MENTIONED_USER = _(
    u'mail_notification_mentioned_user',
    default=u'A comment that mentions you on "${title}" '
            u'has been posted here: ${link}\n\n'
            u'---\n'
            u'${text}\n'
    )


def get_peoples(text):
    pm = api.portal.get_tool(name='portal_membership')
    peoples = {}
    for word in text.replace('<p>', '').replace('</p>', '').split(' '):
        if word.startswith('@'):
            userid = word[1:]
            member = pm.getMemberById(userid)
            peoples[userid] = "<a href='{}/author/{}'>{}</a>".format(
                api.portal.get_navigation_root(api.portal.get()).absolute_url(),
                member.getId(),
                member.getProperty('fullname')
            )
    return peoples


def replace_user_info(text):
    peoples = get_peoples(text)
    for people in peoples:
        text = text.replace('@' + people, peoples[people])
    return text


def getText(self, targetMimetype=None):
    """
    Original getText method of class Comment taken from
    plone.app.discussion 3.0.8
    """
    # The body text of a comment.
    transforms = getToolByName(self, 'portal_transforms')

    if targetMimetype is None:
        targetMimetype = 'text/x-html-safe'

    sourceMimetype = getattr(self, 'mime_type', None)
    if sourceMimetype is None:
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IDiscussionSettings, check=False)
        sourceMimetype = settings.text_transform
    text = self.text
    if text is None:
        return ''
    if isinstance(text, six.text_type):
        text = text.encode('utf8')
    transform = transforms.convertTo(
        targetMimetype,
        text,
        context=self,
        mimetype=sourceMimetype)
    if transform:
        text = transform.getData()
        return replace_user_info(text)
    else:
        logger = logging.getLogger('plone.app.discussion')
        msg = u'Transform "{0}" => "{1}" not available. Failed to ' \
              u'transform comment "{2}".'
        logger.error(
            msg.format(
                sourceMimetype,
                targetMimetype,
                self.absolute_url(),
            ),
        )
        return text


def notify_mentions(obj, event):
    """
        Tell the mentioned people a comment was added.
    """

    mail_host = getToolByName(obj, 'MailHost')
    pm = getToolByName(obj, 'portal_membership')
    registry = getUtility(IRegistry)
    mail_settings = registry.forInterface(IMailSchema, prefix='plone')
    sender = mail_settings.email_from_address



    # Check if a sender address is available
    if not sender:
        return

    peoples_to_notify = get_peoples(obj.text)


    if not peoples_to_notify:
        return


    conversation = aq_parent(obj)
    content_object = aq_parent(conversation)

    # Compose email
    subject = translate(_(u'A comment that mentions you has been posted.'), context=obj.REQUEST)
    message = translate(
        Message(
            MAIL_NOTIFICATION_MESSAGE_MENTIONED_USER,
            mapping={
                'title': safe_unicode(content_object.title),
                'link': content_object.absolute_url() + '/view#' + obj.id,
                'text': obj.text,
            },
        ),
        context=obj.REQUEST,
    )

    # Send email
    for people in peoples_to_notify:
        member = pm.getMemberById(people)
        if not member:
            continue

        mto = member.getProperty('email')

        if not mto:
            continue

        try:
            mail_host.send(message, mto, sender, subject, charset='utf-8')
        except SMTPException as e:
            logger.error(
                'SMTP exception (%s) while trying to send an ' +
                'email notification to the comment moderator ' +
                '(from %s to %s, message: %s)',
                e,
                sender,
                mto,
                message,
            )

