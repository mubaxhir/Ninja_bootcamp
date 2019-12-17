import graphene
from flask import Flask, render_template , redirect,request,jsonify
from flask_graphql import GraphQLView
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] ='myFlaskApp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Models
class TodoItem(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String(name=graphene.String(default_value="todo_task"))
    description = graphene.String(required=True)
    done = graphene.Boolean(status=graphene.Boolean(default_value=False))

    def todo_tasks(self, args, context, info):
        userdata = mysql.connection.cursor()
        userdata.execute("SELECT * FROM myFlaskApp.todoApp")
        response=userdata.fetchall()
        data = [TodoItem(id=todo['id'], description=todo['description'],done=todo['done']) for todo in response]
        return data

class Query(graphene.ObjectType):
    todo_items = graphene.List(TodoItem)
    todo_item = graphene.Field(TodoItem, id=graphene.Int())

    def resolve_todo_items(self, args):
        userdata = mysql.connection.cursor()
        userdata.execute("SELECT * FROM myFlaskApp.todoApp")
        response=userdata.fetchall()
        data = [TodoItem(id=todo['id'], description=todo['description'], title=todo['title'],done=todo['done']) for todo in response]
        return data

# Schema Objects
schema = graphene.Schema(query=Query)



# @app.route('/todo/api/v1.0/tasks',methods=['GET'])
# def retrieve_list():
#     userData = mongo.db.userData
#     print(type(userData))
#     output = []
#     for q in userData.find():
#         output.append({'id' : q['id'], 'Title' : q['Title'],'Description':q['Description'],"Done":q["Done"]})
#     return jsonify({'result' : output})

# @app.route('/todo/api/v1.0/tasks/<id>',methods=['GET'])
# def retrieve(id):
#     try:
#         id = int(id)
#     except:
#         return jsonify({"not succesful":"id must be numeric"})
#     else:
#         userData = mongo.db.userData
#         result = userData.find_one({"id":id})
#         output=[]
#         output.append({'Done':result['Done'],'Description':result['Description'], 'Title' : result['Title'],'id':result['id']})
#         print(output)
#         if result:
#             return jsonify({"output":output})
#         else:
#             return jsonify({"unsuccessful":"id not found"}) 

# @app.route('/todo/api/v1.0/tasks',methods=['POST','GET'])
# def create():
#     data = request.json
#     data = dict(data)
#     try:
#         data["id"] = int(data["id"])
#     except:
#         return jsonify({"not succesful":"id must be numeric"})
#     else:
#         userData = mongo.db.userData
#         result = userData.find_one({"id":data["id"]})
#         if result:
#             return jsonify({"Not succesful":"id must be unique and numeric"}) 
#         else:
#             userData.insert_one(data)
#             return jsonify({"success":True})

# @app.route('/todo/api/v1.0/tasks/<id>',methods=['PUT'])
# def update(id):
#     data = dict(request.json)
#     try:
#         id = int(id)
#     except:
#         return jsonify({"not succesful":"id must be numeric"})
#     userData = mongo.db.userData
#     result = userData.find_one({"id":id})
#     if result:
#         userData.delete_one({"id": data["id"]})
#         userData.insert_one(data)
#         return jsonify({"success":True})
#     else:
#         return jsonify({"id not found":True})
 
# @app.route('/todo/api/v1.0/tasks/<id>',methods =['DELETE'])
# def delete(id):
#     userData = mongo.db.userData
#     result = userData.find_one({"id":id})
#     if id == result["id"]:
#         userData.delete_one({"id": id})
#         return jsonify({"deleted":True})
#     else:
#         return jsonify({"deleted":False})
app.add_url_rule('/', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

@app.route('/hello')
def hello():
    return "I am here for real"

if __name__ == '__main__':
     app.run(debug=True)