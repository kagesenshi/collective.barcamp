"""Definition of the BarcampParticipant content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from collective.barcamp.interfaces import IBarcampParticipant
from collective.barcamp.config import PROJECTNAME

BarcampParticipantSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    atapi.StringField('email',
                 required=True,
                 validators=('isEmail'),
    ),

    atapi.StringField('online_presence', required=False)
))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

BarcampParticipantSchema['title'].storage = atapi.AnnotationStorage()
BarcampParticipantSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(BarcampParticipantSchema, moveDiscussion=False)


class BarcampParticipant(base.ATCTContent):
    """A participant information"""
    implements(IBarcampParticipant)

    meta_type = "BarcampParticipant"
    schema = BarcampParticipantSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(BarcampParticipant, PROJECTNAME)
