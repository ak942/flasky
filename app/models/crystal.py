from app import db 

class Crystal(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)
    color = db.Column(db.String)
    powers = db.Column(db.String)
    healer_id = db.Column(db.Integer, db.ForeignKey("healer.id"))
    healer = db.relationship("Healer", back_populates = "crystals")



    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "powers": self.powers
        }
    #it is self because it is calling itself 

    #this is a decorator so the function can be called on the class itself not on the atrributes
    #can call it like Crystal.function() instead of calling the function on the instance of the class (object)
    @classmethod
    def from_dict(cls, crystal_data):
        new_crystal = Crystal(
            name = crystal_data["name"],
            color = crystal_data["color"],
            powers = crystal_data["powers"]
        ) 
        return new_crystal
    #no id because it also gets passed it
    #can use Crystal or cls in the from_dict function