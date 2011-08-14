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

from collective.barcamp.unrestrictor import execute_under_special_role

class IEventForm(interface.Interface):
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
    
class EventForm(form.Form):
    fields = field.Fields(IEventForm)
    ignoreContext = True # don't use context to get widget data
    label = u"Add a session"

    @button.buttonAndHandler(u'Submit')
    def handleApply(self, action):
        data, errors = self.extractData()
        typestool = getToolByName(self.context, 'portal_types')
        wftool = getToolByName(self.context, 'portal_workflow')
        identifier = queryUtility(IIDNormalizer).normalize(data['title'])
        if not self.context.has_key('sessions'):
            typestool.constructContent(
                type_name='Folder',
                container=self.context,
                id='sessions'
            )
            self.context['sessions'].setTitle('Sessions')
            wftool.doActionFor(container, 'publish')
        container = self.context['sessions']
        count = len([i for i in container.keys() if identifier in i])
        if count:
            identifier = '%s-%s' % (identifier, count-1)
        subject = list([i for i in data['subject'].split('\n') if i])
        del data['subject']
        level = data['level']
        del data['level']

        execute_under_special_role(
            self.context,
            'Manager',
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
        execute_under_special_role(
            self.context,
            'Manager',
            wftool.doActionFor,
            container[identifier], 
            'publish'
        )
        self.request.response.redirect(content.absolute_url())

EventFormView = wrap_form(EventForm)
