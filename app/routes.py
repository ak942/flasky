from flask import Blueprint, jsonify

class Crystal:
    def __init__(self, id, name, color, powers):
        self.id = id
        self.name = name
        self.color = color 
        self.powers = powers 

#create instances
crystals = [
    Crystal(1,"Amethyst", "Purple", "Infinite knowledge and wisdom"),
    Crystal(2, "Tiger's Eye", "Gold", "Confidence"),
    Crystal(3, "Rose Quartz", "Pink", "Love")
]
#Create a bluprint, the end of the routes are all going to have crystals
#"crystals is the resource name"
crystal_bp = Blueprint("crystals",__name__,url_prefix = "/crystals")

#register the Blueprint into the app/init file

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
    return jsonify(crystal_response)
