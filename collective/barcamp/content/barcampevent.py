"""Definition of the BarcampEvent content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from collective.barcamp.interfaces import IBarcampEvent
from collective.barcamp.config import PROJECTNAME
from DateTime import DateTime

from Products.CMFCore.permissions import ModifyPortalContent, View

BarcampEventSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.TextField('text',
        required=False,
        searchable=True,
        storage = atapi.AnnotationStorage(),
        allowable_content_types=(
            'text/plain', 'text/structured', 'text/html',
            'application/msword',
        ),
        validators = ('isTidyHtmlWithCleanup',),
        #validators = ('isTidyHtml',),
        default_output_type = 'text/html',
        widget = atapi.RichWidget(
            description = '',
            label = u'Body Text',
            rows = 25,
            allow_file_upload = False
        )
    ),

    atapi.DateTimeField('startDate',
                  required=True,
                  searchable=False,
                  storage=atapi.AnnotationStorage(),
                  default_method=DateTime,
                  widget = atapi.CalendarWidget(
                        description= '',
                        label=u'Event Starts'
                        )),

    atapi.DateTimeField('endDate',
                  required=True,
                  searchable=False,
                  storage=atapi.AnnotationStorage(),
                  default_method=DateTime,
                  widget = atapi.CalendarWidget(
                        description = '',
                        label=u'Event Ends'
                        )),

    atapi.StringField('location_url',
                searchable=True,
                storage=atapi.AnnotationStorage(),
                widget = atapi.StringWidget(
                    description = '',
                    label = u'URL link to location (website/map)'
                )),
))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

BarcampEventSchema['title'].storage = atapi.AnnotationStorage()
BarcampEventSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    BarcampEventSchema,
    folderish=True,
    moveDiscussion=False
)

BarcampEventSchema.changeSchemataForField('location', 'default')
BarcampEventSchema.moveField('location', before='startDate')
BarcampEventSchema.moveField('location_url', after='location')


class BarcampEvent(folder.ATFolder):
    """A Barcamp Event"""
    implements(IBarcampEvent)

    meta_type = "BarcampEvent"
    schema = BarcampEventSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    text = atapi.ATFieldProperty('text')
    startDate = atapi.ATFieldProperty('startDate')
    endDate = atapi.ATFieldProperty('endDate')
    location_url = atapi.ATFieldProperty('location_url')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(BarcampEvent, PROJECTNAME)
