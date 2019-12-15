from flask import Flask,jsonify,request
from data import initData
from flask_graphql import GraphQLView
from schema import schema
from mongoengine import connect
from model import Id,TITLE,Description,Done
from flask_pymongo import PyMongo


app = Flask(__name__)

default_query = """{
    allTodo{
        edges {
            node {
                id,
                title,
                description,
                done
            }
        }
    }
}""".strip()

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == "__main__":
    initData()
    app.run(debug=True)





