"""Definition of the BarcampEvent content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from collective.barcamp.interfaces import IBarcampEvent
from collective.barcamp.config import PROJECTNAME

BarcampEventSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

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


class BarcampEvent(folder.ATFolder):
    """A Barcamp Event"""
    implements(IBarcampEvent)

    meta_type = "BarcampEvent"
    schema = BarcampEventSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(BarcampEvent, PROJECTNAME)
