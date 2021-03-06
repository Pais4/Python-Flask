from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost:27017/pythonmongodb'

#Le pasamos la configuracion a PyMongo
mongo = PyMongo(app)

#POST
@app.route('/customer', methods=['POST'])
#Funcion para crear el usuario
def create_user():
    #Recibiendo datos
    name = request.json['name']
    lastName = request.json['lastName']
    identification = request.json['identification']
    birthDate = request.json['birthDate']
    city = request.json['city']
    neighborhood = request.json['neighborhood']
    phone = request.json['phone']

    #Validacion sencilla de que estamos recibiendo los datos
    if name and lastName and identification and birthDate and city and neighborhood and phone:
        #Esto retorna un id
        id = mongo.db.customers.insert(
            {
                'name' : name,
                'lastName' : lastName,
                'identification' : identification,
                'birthDate' : birthDate,
                'city' : city,
                'neighborhood' : neighborhood,
                'phone' : phone
            }
        )
        #Descripcion del nuevo dato que se ha creado
        response = {
            'id': str(id),
            'name' : name,
            'lastName' : lastName,
            'identification' : identification,
            'birthDate' : birthDate,
            'city' : city,
            'neighborhood' : neighborhood,
            'phone' : phone
        }
        return response
    else:
        return not_found()
    
    return {'message': 'received'}

#GET ALL USERS
@app.route('/customers', methods=['GET'])
def get_users():
    customers = mongo.db.customers.find()
    response = {"quotesDB": customers}
    return Response(json_util.dumps(response),  mimetype='application/json')
    # response = json_util.dumps(customers)
    # #Response es para que se vea como un json en vez de un String
    # return Response(response, mimetype='application/json')

#GET USER BY ID
@app.route('/customer/<id>', methods=['GET'])
def get_user(id):
    #Convertimos a un object id el id que nos manda el usuario
    user = mongo.db.customers.find_one({'_id': ObjectId(id)})
    #Lo convertimos a un Json
    response = json_util.dumps(user)
    return Response(response, mimetype='application/json')

#DELETE
@app.route('/customer/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.customers.delete_one({'_id': ObjectId(id)})
    response = jsonify({
        'message': 'Customer ' + id + ' was deleted successfully'
    })
    return response

#PUT
@app.route('/customer/<id>', methods=['PUT'])
def update_user(id):
    name = request.json['name']
    lastName = request.json['lastName']
    identification = request.json['identification']
    birthDate = request.json['birthDate']
    city = request.json['city']
    neighborhood = request.json['neighborhood']
    phone = request.json['phone']

    if name and lastName and identification and birthDate and city and neighborhood and phone:
        mongo.db.customers.update_one({'_id': ObjectId(id)}, {'$set': {
            'name' : name,
            'lastName' : lastName,
            'identification' : identification,
            'birthDate' : birthDate,
            'city' : city,
            'neighborhood' : neighborhood,
            'phone' : phone
        }})
        response = jsonify({
        'message': 'Customer ' + id + ' was updated successfully'
    })
    return response


#Manejador de errores
@app.errorhandler(404)
def not_found(error=None):
    #jsonify permite añadir mas propiedades
    response = jsonify({
        'message': 'Resource not found: ' + request.url,
        'status': 404
    })
    #Cambiamos el codigo de estatus
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run(debug=True)