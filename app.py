from flask import Flask, render_template , redirect,request,jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://mubi:1234@cluster001-avto2.mongodb.net/test?retryWrites=true&w=majority"
mongo = PyMongo(app)

@app.route('/retrieve_list',methods=['GET'])
def retrieve_list():
    userData = mongo.db.userData
    print(type(userData))
    output = []
    for q in userData.find():
        output.append({'id' : q['id'], 'Title' : q['Title'],'Description':q['Description']})
    return jsonify({'result' : output})

@app.route('/retrieve',methods=['POST','GET'])
def retrieve():
    data = dict(request.json)
    try:
        data["id"] = int(data["id"])
    except:
        return jsonify({"not succesful":"id must be numeric"})
    else:
        userData = mongo.db.userData
        result = userData.find_one({"id":data["id"]})
        output=[]
        output.append({'Description':result['Description'], 'Title' : result['Title'],'id':result['id']})
        print(output)
        if result:
            return jsonify({"output":output})
        else:
            return jsonify({"unsuccessful":"id not found"}) 

@app.route('/create',methods=['GET','POST'])
def create():
    data = request.json
    data = dict(data)
    try:
        data["id"] = int(data["id"])
    except:
        return jsonify({"not succesful":"id must be numeric"})
    else:
        userData = mongo.db.userData
        result = userData.find_one({"id":data["id"]})
        if result:
            return jsonify({"Not succesful":"id must be unique and numeric"}) 
        else:
            userData.insert_one(data)
            return jsonify({"success":True})

@app.route('/update',methods=['POST','PUT'])
def update():
    data = dict(request.json)
    userData = mongo.db.userData
    result = userData.find_one({"id":data["id"]})
    if result:
        userData.delete_one({"id": data["id"]})
        userData.insert_one(data)
        return jsonify({"success":True})
    else:
        return jsonify({"id not found":True})
 
@app.route('/delete',methods =['POST','DELETE'])
def delete():
    data = dict(request.json)
    userData = mongo.db.userData
    result = userData.find_one({"id":data["id"]})
    if data["id"] == result["id"]:
        userData.delete_one({"id": data["id"]})
        return jsonify({"deleted":True})
    else:
        return jsonify({"deleted":False})

if __name__ ==  "__main__":
    app.run(debug=True)



# Task 1 DONE!!!!