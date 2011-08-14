from zope import interface, schema
from z3c.form import form, field, button
from plone.z3cform.layout import wrap_form
from zope.component import queryUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Products.CMFCore.utils import getToolByName
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

LEVEL_VOCAB = SimpleVocabulary([
    SimpleTerm(value=u'beginner', title=u'Beginner'),
    SimpleTerm(value=u'intermediate', title=u'Intermediate'),
    SimpleTerm(value=u'advanced', title=u'Advanced')
])

from collective.barcamp.unrestrictor import unrestrictedExec

class ISessionSubmissionForm(interface.Interface):
    title = schema.TextLine(title=u"Title")
    description = schema.Text(title=u"Description", required=True)
    contact_name = schema.TextLine(title=u"Speaker", required=True)
    subject = schema.Text(
        title=u'Tags', 
        description=u'Enter one tag per line, multiple words allowed.'
    )
    level = schema.Choice(
        title=u'Level',
        vocabulary=LEVEL_VOCAB
    )
    
class SessionSubmissionForm(form.Form):
    fields = field.Fields(ISessionSubmissionForm)
    ignoreContext = True # don't use context to get widget data
    label = u"Register a session"

    @button.buttonAndHandler(u'Submit')
    def handleApply(self, action):
        data, errors = self.extractData()
        typestool = getToolByName(self.context, 'portal_types')
        wftool = getToolByName(self.context, 'portal_workflow')
        identifier = queryUtility(IIDNormalizer).normalize(data['title'])
        if not self.context.has_key('sessions'):
            unrestrictedExec(
                typestool.constructContent,
                type_name='Folder',
                container=self.context,
                id='sessions'
            )
            unrestrictedExec(
                self.context['sessions'].setTitle,
                'Sessions'
            )
            unrestrictedExec(
                wftool.doActionFor,
                self.context['sessions'],
                'publish'
            )
            self.context['sessions'].reindexObject()
        container = self.context['sessions']
        identifier = str(len(container.keys()) + 1)
        subject = list([i for i in data['subject'].split('\n') if i])
        del data['subject']
        level = data['level']
        del data['level']

        unrestrictedExec(
            typestool.constructContent,
            type_name="BarcampSession",
            container=container,
            id=identifier,
            **data
        )
        
        content = container[identifier]
        schema = content.Schema()
        schema['subject'].set(content, subject)
        schema['level'].set(content, level)
        schema['startDate'].set(content, self.context.startDate)
        schema['endDate'].set(content, self.context.endDate)
        unrestrictedExec(
            wftool.doActionFor,
            container[identifier], 
            'publish'
        )
        content.reindexObject()
        self.request.response.redirect(content.absolute_url())

SessionSubmissionView = wrap_form(SessionSubmissionForm)


class IRegistrationForm(interface.Interface):
    title = schema.TextLine(title=u"Full name")
    email = schema.TextLine(
        title=u"Email address",
        description=(u"We will not publish this." +
                    "We collect this to send confirmed details" +
                    " and a reminder just before the camp.")
    )
    description = schema.Text(
        title=u"Short Bio", 
        description=(u"Where you're from, where you work " +
                    "/ study, brief self-description"),
        required=True
    )
    online_presence = schema.TextLine(
        title=u'Online presence',
        description=u'URL to blog / website / Google+ / Twitter / Facebook / etc',
        required=False
    )

class RegistrationForm(form.Form):
    fields = field.Fields(IRegistrationForm)
    ignoreContext = True # don't use context to get widget data
    label = u"Register"

    @button.buttonAndHandler(u'Register')
    def handleApply(self, action):
        data, errors = self.extractData()
        typestool = getToolByName(self.context, 'portal_types')
        wftool = getToolByName(self.context, 'portal_workflow')
        plone_utils = getToolByName(self.context, 'plone_utils')
        if not self.context.has_key('registrations'):
            unrestrictedExec(
                typestool.constructContent,
                type_name='Folder',
                container=self.context,
                id='registrations'
            )
            unrestrictedExec(
                self.context['registrations'].setTitle,
                'Registrations'
            )
            cschema = self.context['registrations'].Schema()
            cschema['excludeFromNav'].set(
                self.context['registrations'],
                True
            )
            self.context['registrations'].reindexObject()
        container = self.context['registrations']
        identifier = str(len(container.keys()) + 1)

        unrestrictedExec(
            typestool.constructContent,
            type_name="BarcampParticipant",
            container=container,
            id=identifier,
            **data
        )
        plone_utils.addPortalMessage(
            'Thank you for your submission. You are now registered',
            'info'
        )
        self.request.response.redirect(self.context.absolute_url())

RegistrationView = wrap_form(RegistrationForm)
