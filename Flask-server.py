from flask import Flask, render_template
from flask_restx import Api, Resource
import json
import mariadb_master
import sys


maria = mariadb_master.Mariadb(None)

app = Flask("Drone Server")  # Flask 객체 선언, 파라미터로 어플리케이션 패키지의 이름을 넣어줌.
api = Api(app)  # Flask 객체에 Api 객체 등록

@api.route('/hello')  # 데코레이터 이용, '/hello' 경로에 클래스 등록
class HelloWorld(Resource):
    def get(self):  # GET 요청시 리턴 값에 해당 하는 dict를 JSON 형태로 반환
        return {"hello": "world!"}

@api.route('/drone/gps/<string:data>')
class DroneGPS(Resource):
    def get(self, data):
        result = json.loads(data)
        id = result['id']
        ql = maria.getGPS(id, 'drone')
        print(ql)
        return ql
    def post(self, data):
        result = json.loads(data)
        id = result['id']
        lat = result['lat']
        lng = result['lng']
        print("ID : %s, lat : %s, lng : %s" % (id, lat, lng))
        result = maria.insertGPS(id, lat, lng, 'drone')
        return result

@api.route('/client/gps/<string:data>')
class ClientGPS(Resource):
    def get(self, data):
        result = json.loads(data)
        id = result['id']
        ql = maria.getGPS(id, 'client')
        print(ql)
        return ql
    def post(self, data):
        result = json.loads(data)
        id = result['id']
        lat = result['lat']
        lng = result['lng']
        print("ID : %s, lat : %s, lng : %s" % (id, lat, lng))
        result = maria.insertGPS(id, lat, lng, 'client')
        return result

@api.route('/client/<string:data>')
class Client(Resource):
    def get(self, data):
        result = json.loads(data)
        id = result['id']
        res = maria.getClient(id)
        print(res)
        return res
    def post(self, data):
        result = json.loads(data)
        id = result['id']
        password = result['pw']
        email = result['email']
        phone = result['phone']
        print("ID : %s, password : %s, email : %s, phone : %s" % (id, password, email, phone))
        result = maria.joinClient(id, password, email, phone)
        return result

@api.route('/client/log/<string:data>')
class ClientLog(Resource):
    def get(self):
        return

@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)