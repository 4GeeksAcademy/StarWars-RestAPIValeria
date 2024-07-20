from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)

    favorites = db.relationship("favorites", back_populates="usuarios")

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "name": self.name, 
            "last_name": self.last_name,
            "favorites": [favorite.serialize() for favorite in self.favorites]
        }
    
class favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'))
    specie_id = db.Column(db.Integer, db.ForeignKey('species.id'))
    starship_id = db.Column(db.Integer, db.ForeignKey('starship.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
        
    film = db.relationship("Film", uselist=False, back_populates="favorites")
    species = db.relationship("Species", uselist=False, back_populates="favorites")
    starship = db.relationship("Starship", uselist=False, back_populates="favorites")
    vehicle = db.relationship("Vehicle", uselist=False, back_populates="favorites")
    character = db.relationship("Character", uselist=False, back_populates="favorites")
    planet = db.relationship("Planet", uselist=False, back_populates="favorites")

    usuarios = db.relationship("User",  back_populates="favorites")

    def __repr__(self):
        return '<favorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "film": self.film.title if self.film else None,
            "species": self.species.name if self.species else None,
            "starship": self.starship.name if self.starship else None,
            "character": self.character.name if self.character else None,
            "planet": self.planet.name if self.planet else None
        }

starships_films = db.Table('starships_films',
                           db.Column('starship_id', db.Integer, db.ForeignKey('starship.id'), primary_key=True),
                           db.Column('film_id', db.Integer, db.ForeignKey('film.id'), primary_key=True)
                           )

vehicles_films = db.Table('vehicles_films',
                          db.Column('vehicle_id', db.Integer, db.ForeignKey('vehicle.id'), primary_key=True),
                          db.Column('film_id', db.Integer, db.ForeignKey('film.id'), primary_key=True)
                          )

species_films = db.Table('species_films',
                         db.Column('species_id', db.Integer, db.ForeignKey('species.id'), primary_key=True),
                         db.Column('film_id', db.Integer, db.ForeignKey('film.id'), primary_key=True)
                         )

films_planets = db.Table('films_planets',
                         db.Column('film_id', db.Integer, db.ForeignKey('film.id'), primary_key=True),
                         db.Column('planet_id', db.Integer, db.ForeignKey('planet.id'), primary_key=True)
                         )

class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    episode_id = db.Column(db.Integer, nullable=False)
    director = db.Column(db.String(255), nullable=True)
    opening_crawl = db.Column(db.Text, nullable=True)
    producer = db.Column(db.String(255), nullable=True)
    release_date = db.Column(db.Date, nullable=True)
    created = db.Column(db.DateTime, nullable=True)
    edited = db.Column(db.DateTime, nullable=True)
    url = db.Column(db.String(255), unique=True, nullable=False)

    favorites = db.relationship("favorites", back_populates="film")

    def __repr__(self):
        return '<Film %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "episode_id": self.episode_id,
            "director": self.director,
            "opening_crawl": self.opening_crawl,
            "producer": self.producer,
            "release_date": self.release_date.strftime('%Y-%m-%d'),
            "created": self.created.strftime('%Y-%m-%d'),
            "edited": self.edited.strftime('%Y-%m-%d'),
            "url": self.url
        }

class Starship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(255), nullable=True)
    starship_class = db.Column(db.String(255), nullable=True)
    manufacturer = db.Column(db.String(255), nullable=True)
    cost_in_credits = db.Column(db.String(50), nullable=True)
    length = db.Column(db.String(50), nullable=True)
    crew = db.Column(db.String(50), nullable=True)
    passengers = db.Column(db.String(50), nullable=True)
    max_atmosphering_speed = db.Column(db.String(50), nullable=True)
    hyperdrive_rating = db.Column(db.String(50), nullable=True)
    MGLT = db.Column(db.String(50), nullable=True)
    cargo_capacity = db.Column(db.String(50), nullable=True)
    consumables = db.Column(db.String(50), nullable=True)
    created = db.Column(db.DateTime, nullable=True)
    edited = db.Column(db.DateTime, nullable=True)
    url = db.Column(db.String(255), unique=True, nullable=True)

    films = db.relationship('Film', secondary=starships_films, backref=db.backref('starships', lazy=True))
    favorites = db.relationship("favorites", back_populates="starship")

    def __repr__(self):
        return '<Starship %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "starship_class": self.starship_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "hyperdrive_rating": self.hyperdrive_rating,
            "MGLT": self.MGLT,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "created": self.created.strftime('%Y-%m-%d'),
            "edited": self.edited.strftime('%Y-%m-%d'),
            "url": self.url
        }

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    vehicle_class = db.Column(db.String(255), nullable=True)
    manufacturer = db.Column(db.String(255), nullable=True)
    cost_in_credits = db.Column(db.String(50), nullable=True)
    length = db.Column(db.String(50), nullable=True)
    crew = db.Column(db.String(50), nullable=True)
    passengers = db.Column(db.String(50), nullable=False)
    max_atmosphering_speed = db.Column(db.String(50), nullable=True)
    cargo_capacity = db.Column(db.String(50), nullable=True)
    consumables = db.Column(db.String(50), nullable=True)
    created = db.Column(db.DateTime, nullable=True)
    edited = db.Column(db.DateTime, nullable=True)
    url = db.Column(db.String(255), unique=True, nullable=True)

    films = db.relationship('Film', secondary=vehicles_films, backref=db.backref('vehicles', lazy=True))
    favorites = db.relationship("favorites", back_populates="vehicle")

    def __repr__(self):
        return '<Vehicle %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "created": self.created.strftime('%Y-%m-%d'),
            "edited": self.edited.strftime('%Y-%m-%d'),
            "url": self.url
        }

class Species(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    classification = db.Column(db.String(255), nullable=True)
    designation = db.Column(db.String(255), nullable=True)
    average_height = db.Column(db.String(50), nullable=True)
    average_lifespan = db.Column(db.String(50), nullable=True)
    eye_colors = db.Column(db.String(255), nullable=True)
    hair_colors = db.Column(db.String(255), nullable=True)
    skin_colors = db.Column(db.String(255), nullable=True)
    language = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, nullable=True)
    edited = db.Column(db.DateTime, nullable=True)
    homeworld_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    url = db.Column(db.String(255), unique=True, nullable=True)

    homeworld = db.relationship('Planet', backref='species_homeworld', lazy=True)
    films = db.relationship('Film', secondary=species_films, backref=db.backref('species', lazy=True))
    favorites = db.relationship("favorites", back_populates="species")

    def __repr__(self):
        return '<Species %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "classification": self.classification,
            "designation": self.designation,
            "average_height": self.average_height,
            "average_lifespan": self.average_lifespan,
            "eye_colors": self.eye_colors,
            "hair_colors": self.hair_colors,
            "skin_colors": self.skin_colors,
            "language": self.language,
            "homeworld": self.homeworld.name if self.homeworld else None,
            "created": self.created.strftime('%Y-%m-%d'),
            "edited": self.edited.strftime('%Y-%m-%d'),
            "url": self.url
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    diameter = db.Column(db.String(50), nullable=True)
    rotation_period = db.Column(db.String(50), nullable=True)
    orbital_period = db.Column(db.String(50), nullable=True)
    gravity = db.Column(db.String(50), nullable=True)
    population = db.Column(db.String(50), nullable=True)
    climate = db.Column(db.String(255), nullable=True)
    terrain = db.Column(db.String(255), nullable=True)
    surface_water = db.Column(db.String(50), nullable=True)
    created = db.Column(db.DateTime, nullable=True)
    edited = db.Column(db.DateTime, nullable=True)
    url = db.Column(db.String(255), unique=True, nullable=True)

    films = db.relationship('Film', secondary=films_planets, backref=db.backref('planets', lazy=True))
    favorites = db.relationship("favorites", back_populates="planet")

    def __repr__(self):
        return '<Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "created": self.created.strftime('%Y-%m-%d') if self.created else None,
            "edited": self.edited.strftime('%Y-%m-%d') if self.edited else None,
            "url": self.url
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    eye_color = db.Column(db.String(80), nullable=True)
    skin_color = db.Column(db.String(80), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    height = db.Column(db.String(10), nullable=True)
    mass = db.Column(db.String(10), nullable=True)
    hair_color = db.Column(db.String(80), nullable=True)
    birth_year = db.Column(db.String(10), nullable=True)
    homeworld_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    url = db.Column(db.String(120), nullable=True)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    edited = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'))

    homeworld = db.relationship('Planet', backref='characters_homeworld', lazy=True)
    film = db.relationship('Film', backref=db.backref('characters', lazy=True))  
    favorites = db.relationship("favorites", back_populates="character") 

    def __repr__(self): 
        return '<Character %r>' % self.id  

    def serialize(self):  
        return {  
            "id": self.id,
            "name": self.name,
            "eye_color": self.eye_color,
            "skin_color": self.skin_color,
            "gender": self.gender,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "birth_year": self.birth_year,
            "homeworld": self.homeworld.name if self.homeworld else None,
            "url": self.url,
            "created": self.created.strftime('%Y-%m-%d'), 
            "edited": self.edited.strftime('%Y-%m-%d'),  
            "film": self.film.title if self.film else None 
        }

      