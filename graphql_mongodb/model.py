from mongoengine import Document
from mongoengine.fields import ReferenceField,StringField

class Id(Document):
    meta = {"TASK":"id"}
    name = StringField()

class TITLE(Document):
    meta = {"TASK":"title"}
    name = StringField()

class Description(Document):
    meta = {"TASK":"description"}
    name = StringField()

class Done(Document):
    meta = {"TASK":"done"}
    name = StringField()