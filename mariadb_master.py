# import mysql.connector
import json
import socket 
import datetime
from _thread import *
import pymysql
import hashlib

def timenow():
    now = datetime.datetime.now()
    return now

class Mariadb:
    def __init__(self, dict) -> None:
        if dict != None:
            self.DroneDB = pymysql.connect(
                user = dict['user'],
                passwd= dict['passwd'],
                host = dict['host'],
                db= dict['db'],
                charset= 'utf8'
            )
            print("use json file")

        self.insertDict = {
            "insertDroneGPS" : {
                "table" : "Drone_location",
                "id" : "num_drone",
                "lat" : "lat",
                "lng" : "lng",
                "bat" : "battery"
            },
            "insertClientGPS" : {
                "table" : "Client_location",
                "id" : "client_id",
                "lat" : "lat",
                "lng" : "lng",
            },
            "joinClient" : {
                "table" : "Client_information",
                "id" : "client_id",
                "pw" : "password",
                "email" : "email",
                "phone" : "phone"
            },
            "login_hash" : {
                "table" : "Client_login_logs",
                "id" : "client_id",
                "hash" : "login_hash",
                "tf" : "now_login"
            },
            "logout" : {
                "table" : "Client_login_logs",
                "id" : "client_id",
                "tf" : "now_login"
            }
        }

        self.selectDict = {
            "selectDroneGPS" : {
                "table" : "Drone_location",
                "id" : "num_drone"
            },
            "selectClientGPS" : {
                "table" : "Client_location",
                "id" : "client_id"
            },
            "selectClient" : {
                "table" : "Client_information",
                "id" : "client_id"
            },
            "login_hash" : {
                "table" : "Client_login_logs",
                "id" : "client_id"
            }
        }

    def connecter(self, sql):
        # DB에 접속하는 부분입니다.
        c_db = self.DroneDB.cursor(pymysql.cursors.DictCursor)
        if sql != None:
            print("sql : %s" % sql)
            c_db.execute(sql)
            self.DroneDB.commit()
            rows = c_db.fetchall()
            return rows

    def insert(self, dict):
        ### dict의 내용에 관한 설명입니다.
        # dict 는 kind, arr, 값으로 나뉩니다.
        # kind는 해당 딕셔너리가 어떤 값에 대한것인지 종류를 나타냅니다.
        # arr는 해당 키 속성을 담고 있는 리스트 입니다.
        # 이외 모든 값은 arr 리스트에 있는 키값에 담겨있습니다.
        # for문으로 arr를 받아올것입니다.
        kind = dict['kind']     # insert의 kind를 설정. 이는 대상 table을 변화시킴
        arr = dict['arr']
        dict_key = self.insertDict[kind]
        sql = "INSERT INTO " + dict_key['table'] + "("
        key = ""
        value = ""
        for i in range(0, len(arr)):
            key += str(dict_key[arr[i]])
            if(type(value) != 'boolean'):
                value += "'" + int(dict[arr[i]]) + "'"
            else:
                value += "'" + str(dict[arr[i]]) + "'"

            if i < len(arr) - 1:
                key += ", "
                value += ", "
                print("value : %s, typeof : %s" % (value, type(value)))
        sql += key + ") VALUES (" + value + ");"
        print("sql : %s" % sql)
        try:
            self.connecter(sql)
            rsp = {
                'error' : False
            }
            return rsp
        except:
            rsp = {
                'error' : True,
                'message' : 'Error'
            }
            return rsp
        

    def select(self, dict):
        ### dict의 내용에 관한 설명입니다.
        # dict 는 kind, arr, 값으로 나뉩니다.
        # kind는 해당 딕셔너리가 어떤 값에 대한것인지 종류를 나타냅니다.
        # arr는 해당 키 속성을 담고 있는 리스트 입니다.
        # 이외 모든 값은 arr 리스트에 있는 키값에 담겨있습니다.
        # for문으로 arr를 받아올것입니다.
        kind = dict['kind']     # select의 kind를 설정. 이는 대상 table을 변화시킴
        arr = dict['arr']
        dict_key = self.selectDict[kind]
        sql = "select * from " + dict_key['table'] + " where "
        key = ""
        value = ""
        key += str(dict_key[arr[0]])
        value += str(dict[arr[0]])
        sql += key + "='" + value + "' order by _id desc limit 1;"
        print("sql : %s" % sql)
        rows = self.connecter(sql)
        rsp = rows[0]
        rsp['error'] = False
        if 'time' in rsp:
            rsp['time'] = str(rsp['time'])
        return rsp

        
### 2021-05-29 추가
## Table : Client_logs (GET) 
    def getClientLogs(self, clientId):
        c_db = self.DroneDB.cursor(pymysql.cursors.DictCursor)
        sql = None
        sql = ("select * from Client_logs where client_id='%s' order by _id desc limit 1" % clientId)

        if sql != None:
            print(sql)
            c_db.execute(sql)
            try:
                rows = c_db.fetchall()
                
                print(rows)
                cnt = 0
                res = {}
                for i in range(0, len(rows)):
                    res[str(i)] = rows[i]
                    res['end'] = i
                res['error'] = False
                return res
            except:
                return {'error' : True, 'message' : '정보가 일치하지 않습니다.'}