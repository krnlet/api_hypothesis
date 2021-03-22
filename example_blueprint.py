from flask import Blueprint, request, jsonify

example_blueprint = Blueprint('example_blueprint', __name__)

@example_blueprint.route('/')
def index():
    return "This is an example app"


# add view function to the blueprint
@example_blueprint.route('/saludo', methods=['GET'])

 
@example_blueprint.route("/extract_terminology", methods=["POST"])
def extract_terminology():
    
    """
    to read body of a POST OR PUT
    """
    

    Corpus = request.args.get("corpus")
    Language = request.args.get("lang_in")
    print("Received:")
    print(Corpus)
    print(Language)
    

   
    return Response(json.dumps(Corpus),  mimetype="application/json")

