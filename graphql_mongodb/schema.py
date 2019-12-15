import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField,MongoengineObjectType
from model import Id as Idmodel
from model import TITLE as Model_title
from model import Description as Modle_description
from model import Done as Model_done

class Id(MongoengineObjectType):
    class Meta:
        model = Idmodel
        interfaces = (Node,)

class TITLE(MongoengineObjectType):
    class Meta:
        model = Model_title
        interfaces = (Node,)

class Description(MongoengineObjectType):
    class Meta:
        model = Modle_description
        interfaces = (Node,)

class Done(MongoengineObjectType):
    class Meta:
        model = Model_done
        interfaces = (Node,)

class Query(graphene.ObjectType):
    node = Node.Field()
    allId = MongoengineConnectionField(Id)
    allTitle = MongoengineConnectionField(TITLE)
    allDescription = MongoengineConnectionField(Description)
    allDone = MongoengineConnectionField(Done)

schema = graphene.Schema(query=Query,types=[Id,TITLE,Description,Done])
