from flask import Flask,jsonify,request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] ='myFlaskApp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/todo/api/v1.1/tasks',methods=['GET'])
def retrieve_list():
    userdata = mysql.connection.cursor()
    userdata.execute("SELECT * FROM myFlaskApp.todoApp")
    result=userdata.fetchall()
    return jsonify(result)

@app.route('/todo/api/v1.1/tasks/<id>',methods=['GET'])
def retrieve(id):
    userdata = mysql.connection.cursor()
    userdata.execute("SELECT * FROM myFlaskApp.todoApp WHERE id = "+ str(id))
    task=userdata.fetchone()
    return jsonify(task)

@app.route('/todo/api/v1.1/tasks',methods=['POST'])
def create():
    task = request.json
    userdata = mysql.connection.cursor()
    try:
        task["id"] = int(task["id"])
    except:
        return jsonify({"not succesful":"id must be numeric"})
    else:
        userdata.execute("SELECT * FROM myFlaskApp.todoApp where id = "+ str(task["id"]))
        old = userdata.fetchone()
        if old:
            return jsonify({"unsuccessful":"id must be unique"})
        else:
            id = int(task["id"])
            title = task["title"]
            description = task["description"]
            done = task["done"]
            userdata.execute("INSERT INTO myFlaskApp.todoApp (id,title,description,done) VALUES (%s , %s, %s, %s)",(str(id),title,description,done))
            mysql.connection.commit()
            result = {'task':task}
            return jsonify({"result":result})

@app.route('/todo/api/v1.1/tasks/<id>',methods=['PUT'])
def update(id):
    userdata=mysql.connection.cursor()
    task=request.json
    try:
        task["id"] = int(task["id"])
    except:
        return jsonify({"not succesful":"id must be numeric"})
    else:
        userdata.execute("SELECT * FROM myFlaskApp.todoApp where id = "+ str(task["id"]))
        old = userdata.fetchone()
        if old:
            userdata.execute("UPDATE myFlaskApp.todoApp SET title=%s, description=%s, done=%s WHERE id = %s", (task["title"],task["description"],task["done"],str(task["id"])))
            mysql.connection.commit()
            return jsonify({"task":task})
        else:
            return jsonify({"unsuccessful":"id not found to be updated"})

@app.route('/todo/api/v1.1/tasks/<id>',methods =['DELETE'])
def delete(id):
    userdata = mysql.connection.cursor()
    response=userdata.execute("Delete FROM myFlaskApp.todoApp WHERE id = "+str(id))
    if response>0:
        result={"success":"record delete"}
    else:
        result={"unsuccesful":"no record found"}
    mysql.connection.commit()
    return jsonify({"result":result})
    
if __name__ == "__main__":
    app.run(debug=True)

#TASK 2 DONE!!!!!!!!!!