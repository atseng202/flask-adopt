from models import Pet, db
from app import app

db.drop_all()
db.create_all()

Pet.query.delete()

pet1 = Pet(name="Doggo", species="dog", age="young", notes="Nice")
pet2 = Pet(name="Kitty", species="cat", age="young", notes="Mean")

db.session.add(pet1)
db.session.add(pet2)
db.session.commit()