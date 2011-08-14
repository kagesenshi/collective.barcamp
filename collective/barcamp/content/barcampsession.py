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

BarcampSessionSchema = ATEventSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    atapi.StringField(
        'level',
        widget=atapi.SelectionWidget(
            format='select',
            label=u'Level',
        ),
        vocabulary=['beginner', 'intermediate', 'advanced']
    )

))

BarcampSessionSchema['startDate'].required = False
BarcampSessionSchema['endDate'].required = False

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

schemata.finalizeATCTSchema(BarcampSessionSchema, moveDiscussion=False)
from cioppino.twothumbs.interfaces import ILoveThumbsDontYou


class BarcampSession(ATEvent):
    """A Barcamp Session"""
    implements(IBarcampSession, ILoveThumbsDontYou)

    meta_type = "BarcampSession"
    schema = BarcampSessionSchema

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(BarcampSession, PROJECTNAME)
