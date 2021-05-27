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