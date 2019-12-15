from mongoengine import connect
from model import Id,TITLE,Description,Done

connect(host="mongodb+srv://mubi:1234@cluster001-avto2.mongodb.net/test?retryWrites=true&w=majority")

def initData():
    id = Id(name="32452343242")
    id.save()

    title = TITLE(name= "aman")
    title.save()

    description = Description(name="abcdefghijklmnopqrstuvwxyz")
    description.save()

    done = Done(name="true")
    done.save()





