from flask import Flask, request, Response
import mariadb
import json
import sys

from werkzeug.wrappers import response

app = Flask(__name__)



@app.route('/api')
def home():
    return 'Hello World'

@app.route('api//fruits', methods=['GET', 'POST', 'PATCH'])
def fruit_page():
    fruit_name = "kiwi"
    if request.method == 'GET':
        resp = {
            "fruitname" : fruit_name
        }
        return Response(json.dumps(resp, default=str),
                            mimetype="application/json",
                            status=200)
    elif request.method == 'POST':
        data = request.json
        print(data)
        if(data.get("fruitname") != None):
            #default response value
            resp = "Wrong fruit"
            code = 400

            if(data.get("fruitname") == fruit_name):
                resp = "Correct fruit"
                code = 201

            return Response(resp, 
                            mimetype="text/plain",
                            status=code)
        else:
            return Response("ERROR, MISSING ARGUMENT",
                            mimetype="text/plain",
                            status=400)
    elif request.method == 'PATCH':
        return Response("Endpoint under maintenece",
                        mimetype="text/plain",
                        status=503)

if(len(sys.argv) > 1):
    # print(sys.argv[1])
    mode = sys.argv[1]
    if(mode == "production"):
        import bjoern
        host = "0.0.0.0"
        port = 5000
        print("server is running in production code")
        bjoern.run(app,host, port )
    elif(mode == "testing"):
        from flask_cors import CORS
        CORS(app)
        print("server is running in testing mode, switch to production when needed")
        app.run(debug=True)
    else:
        print("invalid mode arguments, exiting")
        exit()
else:
    print("There was no argument provided")
    exit()
