from flask import Flask, render_template
from flask_restx import Api, Resource
import json
import mariadb_master
import sys


with open('/json/mariaDB.json', 'r') as f:
    json_data = json.load(f)
print(json.dumps(json_data))

maria = mariadb_master.Mariadb(json_data)

app = Flask("Drone Server")  # Flask 객체 선언, 파라미터로 어플리케이션 패키지의 이름을 넣어줌.
api = Api(app)  # Flask 객체에 Api 객체 등록

@api.route('/hello')  # 데코레이터 이용, '/hello' 경로에 클래스 등록
class HelloWorld(Resource):
    def get(self):  # GET 요청시 리턴 값에 해당 하는 dict를 JSON 형태로 반환
        return {"hello": "world!"}

@api.route('/drone/gps/<string:data>')
class DroneGPS(Resource):
    def get(self, data):
        try:
            result = json.loads(data)
            id = result['id']
            ql = maria.getGPS(id, 'drone')
            print(ql)
            return json.dumps(ql)
        except:
            pass
    def post(self, data):
        result = json.loads(data)
        dict = {
            "kind" : "insertDroneGPS",
            "arr" : ["id", "lat", "lng", "bat"],
            "id" : result['id'],
            "lat" : result['lat'],
            "lng" : result['lng'],
            "bat" : result['bat'],
        }
        try:
            print("request : " + str(dict))
            resultDB = maria.insert(dict)
            return json.dumps(resultDB)
        except:
            return json.dumps(resultDB)

@api.route('/client/gps/<string:data>')
class ClientGPS(Resource):
    def get(self, data):
        try:
            result = json.loads(data)
            id = result['id']
            ql = maria.getGPS(id, 'client')
            print(ql)
            return json.dumps(ql)
        except:
            pass
    def post(self, data):
        result = json.loads(data)
        try:
            id = result['id']
            lat = result['lat']
            lng = result['lng']
            print("ID : %s, lat : %s, lng : %s" % (id, lat, lng))
            resultDB = maria.insertGPS(id, lat, lng, 'client')
            return json.dumps(resultDB)
        except:
            return json.dumps(result)

@api.route('/client/<string:data>')
class Client(Resource):
    def get(self, data):
        result = json.loads(data)
        try:
            id = result['id']
            if "pw" in result:
                pw = result['pw']
                res = maria.loginClient(id, pw)
            else:
                res = maria.getClient(id)
            print(res)
            return json.dumps(res)
        except:
            pass

    def post(self, data):
        result = json.loads(data)
        try:
            id = result['id']
            password = result['pw']
            email = result['email']
            phone = result['phone']
            print("ID : %s, password : %s, email : %s, phone : %s" % (id, password, email, phone))
            resultDB = {'error' : 'True'}
            resultDB = maria.joinClient(id, password, email, phone)
            return json.dumps(resultDB)
        except:
            return json.dumps(resultDB)

@api.route('/client/log/<string:data>')
class ClientLog(Resource):
    def get(self):
        return

@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)