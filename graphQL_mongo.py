import graphene
from flask import Flask, request,jsonify,json
from flask_graphql import GraphQLView
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://mubi:1234@cluster001-avto2.mongodb.net/test?retryWrites=true&w=majority"
mongo = PyMongo(app)

class TodoItem(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String(name=graphene.String(default_value="todo_task"))
    description = graphene.String(required=True)
    done = graphene.Boolean(status=graphene.Boolean(default_value=False))

    def todo_tasks(self, args, context, info):
        userdata = mongo.db.userData
        response=userdata.find()
        data = [TodoItem(id=response['id'], title=response['title'], description=response['description'],done=response['done']) for todo in response]
        return data.json()

class Query(graphene.ObjectType):
    todo_items = graphene.List(TodoItem)
    todo_item = graphene.Field(TodoItem, id=graphene.Int())

    def resolve_todo_items(self, args):
        userdata = mongo.db.userData
        response = userdata.find()
        data = [TodoItem(id=response['id'], description=response['description'], title=response['title'],done=response['done']) for todo in response]
        return jsonify(data)

schema = graphene.Schema(query=Query)

app.add_url_rule('/', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

@app.route('/hello')
def hello():
    return "I am here for real"

if __name__ == '__main__':
     app.run(debug=True)