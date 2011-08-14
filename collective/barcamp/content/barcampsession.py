"""Definition of the BarcampSession content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from Products.ATContentTypes.content.event import ATEventSchema, ATEvent

# -*- Message Factory Imported Here -*-

from collective.barcamp.interfaces import IBarcampSession
from collective.barcamp.config import PROJECTNAME
from DateTime import DateTime

BarcampSessionSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    atapi.StringField(
        'level',
        storage=atapi.AnnotationStorage(),
        widget=atapi.SelectionWidget(
            format='select',
            label=u'Level',
        ),
        vocabulary=['beginner', 'intermediate', 'advanced']
    ),

    atapi.DateTimeField('startDate',
                  required=False,
                  searchable=False,
                  storage=atapi.AnnotationStorage(),
                  default_method=DateTime,
                  widget = atapi.CalendarWidget(
                        description= '',
                        label=u'Session Starts'
                        )),

    atapi.DateTimeField('endDate',
                  required=False,
                  searchable=False,
                  storage=atapi.AnnotationStorage(),
                  default_method=DateTime,
                  widget = atapi.CalendarWidget(
                        description = '',
                        label=u'Session Ends'
                        )),


))

BarcampSessionSchema['title'].storage = atapi.AnnotationStorage()
BarcampSessionSchema['description'].storage = atapi.AnnotationStorage()


# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

schemata.finalizeATCTSchema(BarcampSessionSchema, moveDiscussion=False)
from cioppino.twothumbs.interfaces import ILoveThumbsDontYou


class BarcampSession(base.ATCTContent):
    """A Barcamp Session"""
    implements(IBarcampSession, ILoveThumbsDontYou)

    meta_type = "BarcampSession"
    schema = BarcampSessionSchema

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    level = atapi.ATFieldProperty('level')
    startDate = atapi.ATFieldProperty('startDate')
    endDate = atapi.ATFieldProperty('endDate')


atapi.registerType(BarcampSession, PROJECTNAME)
