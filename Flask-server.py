from flask import Flask, render_template, jsonify
from flask_restx import Api, Resource
import json
import mariadb_master
import hashlib
import sys




with open('/json/mariaDB.json', 'r') as f:
    json_data = json.load(f)

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
        result = json.loads(data)
        dict = {
            "kind" : "selectDroneGPS",
            "arr" : ["id"],
            "id" : result['id']
        }
        try:
            resultDB = maria.select(dict)
            return resultDB
        except:
            return None
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
            resultDB = maria.insert(dict)
            return jsonify(resultDB)
        except:
            return jsonify(resultDB)

@api.route('/client/gps/<string:data>')
class ClientGPS(Resource):
    def get(self, data):
        result = json.loads(data)
        dict = {
            "kind" : "selectClientGPS",
            "arr" : ["id"],
            "id" : result['id']
        }
        try:
            resultDB = maria.select(dict)
            return jsonify(resultDB)
        except:
            return jsonify(resultDB)
    def post(self, data):
        result = json.loads(data)
        dict = {
            "kind" : "insertClientGPS",
            "arr" : ["id", "lat", "lng"],
            "id" : result['id'],
            "lat" : result['lat'],
            "lng" : result['lng']
        }
        try:
            print("request : " + str(dict))
            resultDB = maria.insert(dict)
            return jsonify(resultDB)
        except:
            return jsonify(resultDB)

@api.route('/client/<string:data>')
class Client(Resource):
    def get(self, data):
        result = json.loads(data)
        dict = {
            "kind" : "selectClient",
            "arr" : ["id"],
            "id" : result['id']
        }
        try:
            resultDB = maria.select(dict)
            return jsonify(resultDB)
        except:
            return jsonify({"error":True})

    def post(self, data):
        result = json.loads(data)
        sha = hashlib.new('sha256')
        sha.update(result['pw'].encode('utf-8'))
        dict = {
            "kind" : "joinClient",
            "arr" : ["id", "pw", "email", "phone"],
            "id" : result['id'],
            "pw" : sha.hexdigest(),
            "email" : result['email'],
            "phone" : result['phone']
        }
        try:
            resultDB = maria.insert(dict)
            return jsonify(resultDB)
        except:
            return jsonify(resultDB)

@api.route('/client/login/<string:data>')
class ClientLogin(Resource):
    def get(self, data):
        result = json.loads(data)
        print(data)
        print(result)
        if("hash" in result):
            dict = {
                "kind" : "login_hash",
                "arr" : ["id"],
                "id" : result['id']
            }
            resultDB = maria.select(dict)
            print("DB hash : %s, User hash : %s" % (resultDB['login_hash'], result.hash))
            if resultDB['login_hash'] == result.hash & resultDB['now_login'] == True:
                return jsonify({"error" : False})
            else :
                return jsonify({"error" : True, "message" : "incorrect hash"})
            print(dict)
            return jsonify({"error" : True, "message" : "incorrect information"})
        else :
            sha = hashlib.new('sha256')
            sha.update(result['pw'].encode('utf-8'))
            dict = {
                "kind" : "selectClient",
                "arr" : ["id"],
                "id" : result['id']
            }
            pw = sha.hexdigest()
            try:
                resultDB = maria.select(dict)
                if resultDB['password'] == pw:
                    print("Password correct!!")
                    dict = {
                        "kind" : "login_hash",
                        "arr" : ["id", "hash", "tf"],
                        "id" : result['id'],
                        "hash" : "fakehash",
                        "tf" : True
                    }
                    resultDB = maria.insert(dict)
                    print(resultDB.items())
                    return jsonify({"error" : False, "hash" : dict['hash']})
                else:
                    print("hash : %s, pwhash : %s" % (resultDB['password'], pw))
                    return jsonify({"error" : True, "message":"올바르지 않는 계정 정보"})
            except:
                return jsonify({"error" : True})


@api.route('/client/log/<string:data>')
class ClientLog(Resource):
    def get(self):
        return

@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)