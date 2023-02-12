from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
import json
from model.foods import Food, Ingredient
from types import SimpleNamespace as Namespace

jpFood_api = Blueprint('jpFood_api', __name__,
                   url_prefix='/api/jpFood')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(jpFood_api)

class jpFoodAPI:        
    class _SaveRecipe(Resource):
        def post(self):
            print(request.json)
            ''' Read data for json body '''
            body = request.get_json()
            
            rec = Food.getRecipeByName(body["name"])
            iIngreds = body["ingredients"]
            ingredients = []
            foodId = rec.id if rec != None else  0
            for ing in iIngreds:
                x = ing["type"]
                print(x)
                ingredients.append(Ingredient( foodId, type=ing["type"], amount=int(ing["amount"]), unit=ing["unit"]))
            
            if (rec == None):
                rec = Food(body["name"], body["directions"])
                rec.ingredients = ingredients
                rec.directions = body["directions"]
                rec.create()
                print('Create new recipe')
            else:
                rec.ingredients = ingredients
                rec.directions = body["directions"]
                rec.description = body["description"]
                rec.update()
                print("Update existing recipe") 
            print(rec)
           

            ''' Avoid garbage in, error checking '''
            # validate name
            foodName = body.get('name')
            if foodName is None:
                return {'message': f'Food is missing, please select a food.'}, 210
            # validate uid
            
            return rec.read()

    class _Read(Resource):
        def get(self):
            foods = Food.query.all()    # read/extract all users from database
            json_ready = [food.read() for food in foods]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    class _Delete(Resource): 
        def post(self):
            print(request.json)
            body = request.get_json()
            
            rec = Food.getRecipeByName(body["name"])
            if rec == None:
                return {
                    'message': f"'{body['name']}' location does not exist."
                }
            else:
                rec.delete()
                return True


    # building RESTapi endpoint
    api.add_resource(_SaveRecipe, '/')
    api.add_resource(_Read, '/')
    api.add_resource(_Delete, '/delete')