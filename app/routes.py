from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.crystal import Crystal
from app.models.healer import Healer

"""
#create instances
crystals = [
    Crystal(1,"Amethyst", "Purple", "Infinite knowledge and wisdom"),
    Crystal(2, "Tiger's Eye", "Gold", "Confidence"),
    Crystal(3, "Rose Quartz", "Pink", "Love")
]
#helper function single responsibility is to validate id and return instance of crystal
def validate_crystal_id(crystal_id):
    try:
        crystal_id = int(crystal_id)
    except:
        abort(make_response({"Message": f"{crystal_id} is not a valid input"},400))
    for crystal in crystals:
        if crystal_id == crystal.id:
            return crystal
    abort(make_response({"Message": f"crystal {crystal_id} does not exist"},404))
    #abort will stop the function and return it to the browser
"""

#Create a bluprint, the end of the routes are all going to have crystals
#"crystals is the resource name"
crystal_bp = Blueprint("crystals",__name__,url_prefix = "/crystals")
healer_bp = Blueprint("healers", __name__, url_prefix= "/healers")

#register the Blueprint into the app/init file    
"""
#create a blueprint decorator call and endpoint
#to get all the crystals that has crystal as an endpoint so the string is empty
@crystal_bp.route("", methods = ["GET"])
def get_call_crystals():
    crystal_response = []
    for crystal in crystals:
        crystal_response.append({
            "id": crystal.id,
            "name": crystal.name ,
            "color": crystal.color ,
            "powers": crystal.powers
        })
#create another decator with getting with id
#url: /crystals/<crystal_id>, responsible for getting representation of the crystal id
@crystal_bp.route("/<crystal_id>", methods = ["GET"])
def get_crystal_by_id(crystal_id):
    crystal= validate_crystal_id(crystal_id)
    return {
        "id": crystal.id,
        "name": crystal.name ,
        "color": crystal.color ,
        "powers": crystal.powers
    }


@crystal_bp.route("/names/<crystal_name>", methods = ["GET"])
def get_crystal_by_name(crystal_name):
    for crystal in crystals:
        if crystal_name == crystal.name:
            return{
                "id": crystal.id
            }
"""
#could go into a seperate file and import as need if there was a healer, jewlery route
#cls is a reference to any class, while cls in Crystal is a reference itself 
#so it can be in either order model_id and cls
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{model_id} is not a valid type {type(model_id)}"},400))
    
    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message": f"{cls.__name__ } {model_id} does not exists"}, 404))
    
    return model

#create a post crystal route
@crystal_bp.route("", methods = ["POST"])
def handle_crystal():
    request_body = request.get_json()

    #refactor how to get a crystal
    # new_crystal = Crystal(
    #     name = request_body['name'],
    #     color = request_body['color'],
    #     powers = request_body['powers']
    # )
    new_crystal = Crystal.from_dict(request_body)

    #add it to the db
    db.session.add(new_crystal)
    #commit it ot the database
    db.session.commit()

    return make_response({'message': f"{new_crystal.name} was successfully added"}, 201)

@crystal_bp.route("", methods = ["GET"])
def get_all_crystals():
    #filter crystal query results 
    color_query = request.args.get("color")
    power_query = request.args.get("powers")

    if color_query and power_query:
        crystals = Crystal.query.filter_by(color = color_query, powers = power_query)
        #case sensitive 
    elif power_query:
        crystals = Crystal.query.filter_by(powers = power_query)
    elif color_query:
        crystals = Crystal.query.filter_by(color = color_query)
    else:
        crystals = Crystal.query.all()

    crystals_response = []

    for crystal in crystals:
        crystals_response.append(crystal.to_dict())
    #refactor when getting dictionary answer
        #crystals_response.append({
        #     "id": crystal.id,
        #     "name": crystal.name,
        #     "color": crystal.color,
        #     "powers": crystal.powers
        # })
    
    return jsonify(crystals_response)

#can create a validation for a single crystal

@crystal_bp.route("/<crystal_id>", methods = ["GET"])
def get_one_crystal(crystal_id):
    crystal = validate_model(Crystal,crystal_id)
    
    return crystal.to_dict(), 200

@crystal_bp.route("/<crystal_id>", methods = ["PUT"])
def update_crystal(crystal_id):
    crystal = validate_model(Crystal,crystal_id)
    request_body = request.get_json()

    crystal.name = request_body["name"]
    crystal.powers = request_body["powers"]
    crystal.color = request_body["color"]

    db.session.commit()

    return crystal.to_dict(), 200

@crystal_bp.route("/<crystal_id>", methods = ["DELETE"])
def delete_one_crystal(crystal_id):
    crystal = validate_model(Crystal,crystal_id)

    db.session.delete(crystal)
    db.session.commit()

    return make_response(f"{crystal_id} was deleted")
#make response returns HTML instead of JSON without headers 

@healer_bp.route("", methods=['POST'])
# define a route for creating a crystal resource
def create_healer():
    request_body = request.get_json()
    
    new_healer = Healer(
        name=request_body["name"]
    )
    
    db.session.add(new_healer)
    db.session.commit()
    
    return jsonify(f"Yayyyy Healer {new_healer.name} successfully created!"), 201


@healer_bp.route("", methods=["GET"])
def read_all_healers():
    
    healers = Healer.query.all()
        
    healers_response = []
    
    for healer in healers:
        healers_response.append({ "name": healer.name, "id": healer.id})
    
    return jsonify(healers_response)

#crystals can be nammed whatever
#nested structure from parent class
@healer_bp.route("/<healer_id>/crystals", methods = ["POST"])
def create_crystal_by_id(healer_id):
    healer = validate_model(Healer, healer_id)
    request_body = request.get_json()

    new_crystal = Crystal(
        name = request_body["name"],
        color = request_body["color"],
        powers = request_body["powers"],
        healer= healer
    )
    db.session.add(new_crystal)
    db.session.commit()
    return jsonify(f"Crystal {new_crystal.name} owned by {new_crystal.healer.name} was successfully created"), 201

@healer_bp.route("/<healer_id>/crystals", methods = ["GET"])
def get_all_crystals_by_healer(healer_id):
    healer = validate_model(Healer, healer_id)
    crystal_response = []

    for crystal in healer.crystals:
        crystal_response.append(
            crystal.to_dict() #you can do it but it won't include anything about the healer 
        )
    return jsonify(crystal_response), 200
