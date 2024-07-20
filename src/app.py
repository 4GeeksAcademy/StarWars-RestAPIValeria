"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Film, Starship, Vehicle, Species, Planet, Character, favorites

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/users', methods=['POST'])  
def create_new_user():  
    try: 
        data = request.json  
        if not data:  
            return jsonify({'error': 'No data provided'}), 400  
        if 'email' not in data:  
            return jsonify({'error': 'Email is required'}), 400  

        if 'username' not in data: 
            return jsonify({'error': 'Username is required'}), 400  

        if 'password' not in data: 
            return jsonify({'error': 'Password is required'}), 400  

        existing_user = User.query.filter_by(email=data['email']).first() 
        if existing_user: 
            return jsonify({'error': 'Email already exists.'}), 409  

        existing_username = User.query.filter_by(username=data['username']).first() 
        if existing_username: 
            return jsonify({'error': 'Username already exists.'}), 409  

        new_user = User(email=data['email'], password=data['password'], name=data.get('name'), last_name=data.get('last_name'), username=data.get('username'))  

        db.session.add(new_user)  
        db.session.commit() 
        return jsonify({'message': 'New user created successfully', 'user_id': new_user.id}), 201  
   
    except Exception as e: 
        return jsonify({'error': 'Error in user creation: ' + str(e)}), 500  
    

@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        if not users:
            return jsonify({'message': 'No users found'}), 404
        
        response_body = [user.serialize() for user in users]
        return jsonify(response_body), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/favorites', methods=['GET'])
def get_favorites():
    try:
        favorites = favorites.query.all()
        
        serialized_favorites = [favorito.serialize() for favorito in favorites]
        
        return jsonify(serialized_favorites), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/users/favorites', methods=['GET'])  
def get_user_favorites(): 
    try:  

        user_id = request.args.get('user_id') 
        if not user_id: 
            return jsonify({'message': 'User ID is required'}), 400  

        user = User.query.get(user_id)  
        if not user: 
            return jsonify({'message': 'User not found'}), 404  
        favorites = user.favorites  
        serialized_favorites = [favorito.serialize() for favorito in favorites]  
        return jsonify(serialized_favorites), 200  
    except Exception as e:  
        return jsonify({'error': str(e)}), 500  

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])  
def add_favorite_planet(planet_id): 
    try:  
        data = request.json  
        if not data:  
            return jsonify({'error': 'No data provided'}), 400  

        user_id = data.get('user_id')  
        if not user_id:  
            return jsonify({'error': 'User ID is required'}), 400  

        user = User.query.get(user_id) 
        if not user:  
            return jsonify({'error': 'User not found'}), 404 

        planet = Planet.query.get(planet_id)
        if not planet:
            return jsonify({'error': 'Planet not found'}), 404  
        new_favorite = favorites(user_id = user_id, planet_id = planet_id)
        db.session.add(new_favorite)
        db.session.commit()  

        return jsonify({'message': 'Planet added to favorites'}), 201  
    except Exception as e:  
        return jsonify({'error': str(e)}), 500 

@app.route('/favorite/character/<int:character_id>', methods=['POST'])  
def add_favorite_character(character_id): 
    try:  
        data = request.json  
        if not data:  
            return jsonify({'error': 'No data provided'}), 400  

        user_id = data.get('user_id')  
        if not user_id:  
            return jsonify({'error': 'User ID is required'}), 400 

        user = User.query.get(user_id) 
        if not user: 
            return jsonify({'error': 'User not found'}), 404  

        character = Character.query.get(character_id) 
        if not character: 
            return jsonify({'error': 'character not found'}), 404 

        new_favorite = favorites(user_id = user_id, character_id = character_id)
        db.session.add(new_favorite)
        db.session.commit()  

        return jsonify({'message': 'character added to favorites'}), 201  
    except Exception as e:  
        return jsonify({'error': str(e)}), 500  


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(planet_id):
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        user_id = data.get('user_id')
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400

        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        favorite = favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()
        if not favorite:
            return jsonify({'error': 'Favorite not found'}), 404

        db.session.delete(favorite)
        db.session.commit()

        return jsonify({'message': 'Favorite planet removed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def remove_favorite_character(character_id):
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        user_id = data.get('user_id')
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400

        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        favorite = favorites.query.filter_by(user_id=user_id, character_id=character_id).first()
        if not favorite:
            return jsonify({'error': 'Favorite not found'}), 404

        db.session.delete(favorite)
        db.session.commit()

        return jsonify({'message': 'Favorite character removed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    serialized_characters = [character.serialize() for character in characters]
    return jsonify(serialized_characters)


@app.route('/character/<int:character_id>', methods=['GET'])  
def get_character(character_id):  
    character = Character.query.get(character_id) 
    if not character: 
        return jsonify({'error': 'Character not found'}), 404 
    return jsonify(character.serialize())  



@app.route('/characters', methods=['POST'])  
def add_character(): 
    data = request.json 
    if not data: 
        return jsonify({'error': 'No data provided'}), 400  

    character = Character() 
    for key, value in data.items():  
        if hasattr(character, key): 
            setattr(character, key, value)  

    db.session.add(character)  
    db.session.commit() \

    return jsonify({'message': 'Character created successfully', 'character_id': character.id}), 201 


@app.route('/character/<int:character_id>', methods=['PUT'])  
def update_character(character_id):  
    character = Character.query.get(character_id)
    if not character: 
        return jsonify({'error': 'Character not found'}), 404

    data = request.json  
    if not data:  
        return jsonify({'error': 'No data provided'}), 400 

    for key, value in data.items():
        if hasattr(character, key):
            setattr(character, key, value) 

    db.session.commit()
    return jsonify({'message': 'Character updated successfully'})


@app.route('/character/<int:character_id>', methods=['DELETE']) 
def delete_character(character_id):  
    character = Character.query.get(character_id)  
    if not character: 
        return jsonify({'error': 'Character not found'}), 404  

    db.session.delete(character) 
    db.session.commit() 
    return jsonify({'message': 'Character deleted successfully'})



@app.route('/planets', methods=['GET'])  
def get_planets(): 
    planets = Planet.query.all()  
    serialized_planets = [planet.serialize() for planet in planets] 
    return jsonify(serialized_planets)  


@app.route('/planet/<int:planet_id>', methods=['GET']) 
def get_planet(planet_id):
    planet = Planet.query.get(planet_id) 
    if not planet: 
        return jsonify({'error': 'Planet not found'}), 404  
    return jsonify(planet.serialize()) 



@app.route('/planets', methods=['POST']) 
def add_planet():  
    data = request.json  
    if not data:  
        return jsonify({'error': 'No data provided'}), 400  

    planet = Planet() 
    for key, value in data.items(): 
        if hasattr(planet, key):
            setattr(planet, key, value) 

    db.session.add(planet) 
    db.session.commit()  

    return jsonify({'message': 'Planet created successfully', 'planet_id': planet.id}), 201

@app.route('/planet/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    planet = Planet.query.get(planet_id) 
    if not planet: 
        return jsonify({'error': 'Planet not found'}), 404 

    data = request.json 
    if not data:  
        return jsonify({'error': 'No data provided'}), 400  

    for key, value in data.items():
       
        if hasattr(planet, key): 
            setattr(planet, key, value)

    db.session.commit()  
    return jsonify({'message': 'Planet updated successfully'})  


@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id): 
    planet = Planet.query.get(planet_id) 
    if not planet:  
        return jsonify({'error': 'Planet not found'}), 404 

    db.session.delete(planet)  
    db.session.commit() 
    return jsonify({'message': 'Planet deleted successfully'})  




if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)