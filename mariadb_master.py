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
            value += "'" + str(dict[arr[i]]) + "'"
            if i < len(arr) - 1:
                key += ", "
                value += ", "
        sql += key + ") VALUES (" + value + ");"
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
        rows = self.connecter(sql)
        rsp = rows[0]
        rsp['error'] = False
        return rsp

    def getClient(self, id):
        c_db = self.DroneDB.cursor(pymysql.cursors.DictCursor)
        sql = None
        sql = ("select * from Client_information where Client_id='%s' order by _id desc limit 1" % id)

        if sql != None:
            print(sql)
            c_db.execute(sql)
            try:
                rows = c_db.fetchall()
                print(rows)
                dt = {'id' : rows[0]['client_id'],'password' : rows[0]['password'],'email' : rows[0]['email'], 'phone' : rows[0]['phone'], 'error':'False'}
                # print(dt)
                print(c_db.fetchall())
                return dt
            except:
                return {'error' : 'True', 'message' : '정보가 일치하지 않습니다.'}


    def loginClient(self, id, pw):
        c_db = self.DroneDB.cursor(pymysql.cursors.DictCursor)
        sql = None
        sql = ("select * from Client_information where Client_id='%s' order by _id desc limit 1" % id)

        if sql != None:
            print(sql)
            c_db.execute(sql)
            try:
                rows = c_db.fetchall()
                print(rows)
                sha = hashlib.new('sha256')
                sha.update(pw.encode('utf-8'))
                print("pw : %s, hash : %s" % (sha.hexdigest, rows[0]['password']))
                if sha.hexdigest() == rows[0]['password']:
                    return {'error' : 'False', 'message' : '정보가 일치합니다.'}
                else:
                    return {'error' : 'True', 'message' : '정보가 일치하지 않습니다.'}
            except:
                return {'error' : 'True', 'message' : '정보가 일치하지 않습니다.'}


    #select SEQUENCE from TABLE_NAME order by SEQUENCE desc limit 1;  // 마지막 행
    def getGPS(self, id, kind):
        # c_db = self.DroneDB.cursor(prepared=True)
        c_db = self.DroneDB.cursor(pymysql.cursors.DictCursor)
        sql = None
        if kind == 'drone':
            sql = ("select * from Drone_location where _id='%s' order by _id desc limit 1" % id)
        elif kind == 'client':
            sql = ("select * from Client_location where _id='%s' order by _id desc limit 1" % id)

        if sql != None:
            print(sql)
            c_db.execute(sql)
            try:
                rows = c_db.fetchall()
                print(rows)
                dt = {'id' : rows[0]['_id'],'lat' : rows[0]['lat'],'lng' : rows[0]['lng'], 'error' : False}
                print(c_db.fetchall())
                # print(dt)
                return dt
            except:
                return {'error' : True, 'message' : '조회에 실패했습니다.'}

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
                rows['error'] = False
                print(rows)
                # dt = {'id' : rows[0]['_id'],'client_id' : rows[0]['client_id'],'num_drone' : rows[0]['num_drone'], 'time_start' : rows[0]['time_start'], 'time_end' : rows[0]['time_end'], 'error':'False'}
                # cursor 가 dict를 return하기 때문에 rows 자체를 돌려줘도 무방할듯
                # error 전해주려면 수정해야함
                # RE : Rows에 직접 추가하면 가능할듯
                return rows
            except:
                return {'error' : True, 'message' : '정보가 일치하지 않습니다.'}

## Table : Client_login_logs (GET)
    def getClientLoginLogs(self, clientId):
        c_db = self.DroneDB.cursor(pymysql.cursors.DictCursor)
        sql = None
        sql = ("select * from Client_login_logs where client_id='%s' order by _id desc limit 1" % clientId)

        if sql != None:
            print(sql)
            c_db.execute(sql)
            try:
                rows = c_db.fetchall()
                rows['error'] = False
                print(rows)
                # dt = {'id' : rows[0]['_id'],'client_id' : rows[0]['client_id'],'login_hash' : rows[0]['login_hash'], 'now_login' : rows[0]['now_login'], 'error':'False'}
                # cursor 가 dict를 return하기 때문에 rows 자체를 돌려줘도 무방할듯
                # error 전해주려면 수정해야함
                return rows
            except:
                return {'error' : True, 'message' : '정보가 일치하지 않습니다.'}

## Table : logs_picture (GET)
    def getLogsPicture(self, clientId):
        c_db = self.DroneDB.cursor(pymysql.cursors.DictCursor)
        sql = None
        sql = ("select * from logs_picture where client_id='%s' order by _id desc limit 1" % clientId)

        if sql != None:
            print(sql)
            c_db.execute(sql)
            try:
                rows = c_db.fetchall()
                rows['error'] = False
                print(rows)
                # dt = {'id' : rows[0]['_id'],'client_id' : rows[0]['client_id'],'url' : rows[0]['url'], 'time' : rows[0]['time'], 'error':'False'}
                # cursor 가 dict를 return하기 때문에 rows 자체를 돌려줘도 무방할듯
                # error 전해주려면 수정해야함
                return rows
            except:
                return {'error' : True, 'message' : '정보가 일치하지 않습니다.'}