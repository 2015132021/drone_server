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
            
    def insertGPS(self, id, lat, lng, kind):
        # c_db = self.DroneDB.cursor(prepared=True)
        c_db = self.DroneDB.cursor(pymysql.cursors.DictCursor)
        sql = None
        if kind == 'drone':
            sql = ("INSERT INTO Drone_location(num_drone, lat, lng) VALUES(%d, %f, %f)" % (id, lat, lng))
        elif kind == 'client':
            sql = ("INSERT INTO Client_location(client_id, lat, lng) VALUES(%d, %f, %f)" % (id, lat, lng))

        if sql != None:
            c_db.execute(sql)
            try:
                self.DroneDB.commit()
                print(c_db.fetchall())
                return {'error' : 'False'}
            except:
                return {'error' : 'True'}

    def joinClient(self, id, pw, email, phone):
        # c_db = self.DroneDB.cursor(prepared=True)
        c_db = self.DroneDB.cursor(pymysql.cursors.DictCursor)
        sql = None
        sha = hashlib.new('sha256')
        sha.update(pw.encode('utf-8'))
        sql = ("INSERT INTO Client_information(client_id, password, email, phone) VALUES('%s', '%s', '%s', '%s')" % (id, sha.hexdigest(), email, phone))
        if sql != None:
            c_db.execute(sql)
            try:
                self.DroneDB.commit()
                print(c_db.fetchall())
                return {'error' : 'False'}
            except:
                return {'error' : 'True'}
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
                dt = {'id' : rows[0]['_id'],'lat' : rows[0]['lat'],'lng' : rows[0]['lng'], 'error':'False'}
                print(c_db.fetchall())
                # print(dt)
                return dt
            except:
                return {'error' : 'True', 'message' : '조회에 실패했습니다.'}

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
                # dt = {'id' : rows[0]['_id'],'client_id' : rows[0]['client_id'],'num_drone' : rows[0]['num_drone'], 'time_start' : rows[0]['time_start'], 'time_end' : rows[0]['time_end'], 'error':'False'}
                # cursor 가 dict를 return하기 때문에 rows 자체를 돌려줘도 무방할듯
                # error 전해주려면 수정해야함
                return rows
            except:
                return {'error' : 'True', 'message' : '정보가 일치하지 않습니다.'}

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
                print(rows)
                # dt = {'id' : rows[0]['_id'],'client_id' : rows[0]['client_id'],'login_hash' : rows[0]['login_hash'], 'now_login' : rows[0]['now_login'], 'error':'False'}
                # cursor 가 dict를 return하기 때문에 rows 자체를 돌려줘도 무방할듯
                # error 전해주려면 수정해야함
                return rows
            except:
                return {'error' : 'True', 'message' : '정보가 일치하지 않습니다.'}

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
                print(rows)
                # dt = {'id' : rows[0]['_id'],'client_id' : rows[0]['client_id'],'url' : rows[0]['url'], 'time' : rows[0]['time'], 'error':'False'}
                # cursor 가 dict를 return하기 때문에 rows 자체를 돌려줘도 무방할듯
                # error 전해주려면 수정해야함
                return rows
            except:
                return {'error' : 'True', 'message' : '정보가 일치하지 않습니다.'}