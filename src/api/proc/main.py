import sys
import xmlrpc.client
from flask import Flask, jsonify, request
import sys


PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000
server = xmlrpc.client.ServerProxy('http://rpc-server:9000')
# set of all teams
# !TODO: replace by database access

app = Flask(__name__)
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
app.config["DEBUG"] = True


#receives the cty name and returns jobs availble in that city
@app.route('/api/PrimeiraRotina', methods=['GET'])
def get_Jobs_in_city():
    response = request.args.get('name')
    teste = server.PrimeiraRotina(response)

    return jsonify(teste)

#receives a rating and returns the company with the same ranting or above
@app.route('/api/SegundaRotina', methods=['GET'])
def get_Companies_by_rating():
    response = request.args.get('name')
    teste = server.SegundaRotina(response)

    return jsonify(teste)

#receives the company name and returns the jobs that company as available
@app.route('/api/TerceiraRotina', methods=['GET'])
def get_Number_of_Available_Jobs_by_Company():
    response = request.args.get('name')
    teste = server.TerceiraRotina(response)

    return jsonify(teste)

#returns a random job from the database
@app.route('/api/QuartaRotina', methods=['GET'])
def get_random_job():
    teste = server.QuartaRotina()

    return jsonify(teste)

#receives city name and returns the companies with jobs in that city
@app.route('/api/QuintaRotina', methods=['GET'])
def get_Companies_with_jobs_in_a_city():
    response = request.args.get('name')
    teste = server.QuintaRotina(response)

    return jsonify(teste)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
