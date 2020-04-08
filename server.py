from flask import Flask, request, make_response
from flask_cors import CORS
import handler


app = Flask(__name__)
CORS(app)

@app.route('/api/v1/solarpanel', methods=['GET'])
def solarpanel_calculation_result():
    lat = request.args.get('latitude')
    lon = request.args.get('longitude')
    lat = float(lat)
    lon = float(lon)
    resp = make_response(handler.getAllInfo(lat,lon))
    resp.mimetype = "application/json"
    return resp

if __name__ == '__main__':
    print('Maid cafe running at port 7500')
    app.run(threaded=True, host='0.0.0.0', port=7500)