import time
import threading
import requests
import json
import options

is_quit = False

####
# 드론의 데이터를 서버에 전송하기 위한 시뮬레이터입니다.
# 존재하는 모듈은 실제 데이터를 받고, 존재하지 않는 모듈은 가상화를 하여 전송하게 됩니다.
####
droneInfo = {       # 드론에 대한 데몬정보
    "OS" : "Demon",
    "firmware" : "0.0.1",
    "Descript" : "This Drone is Demon"
}
gpsInfo = {         # GPS에 대한 데몬 정보
    # 신구대학교 위치 37.44904171317658, 127.16785865546673, 0.0002
    "lat" : 37.44904171317658,
    "lng" : 127.16785865546673
}
batteryInfo = {     # 배터리 종류, 버전 등에 대한 데몬정보
    "name" : "Demon_1.0",
    "version" : "1.0",
    "charge" : 100,
    "offcharging" : 0.05,
    "oncharging" : 0.5
}


class BatteryDemon:         # 배터리 모듈이 존재하지 않을때 사용하는 시뮬레이터 입니다.
    def __init__(self, dict) -> None:
        if dict == None:
            self.name = "Noname"
            self.version = "1.0"
            self.charge = 100
            self.offcharging = 0.05
            self.oncharging = 0.5
        else :
            self.name = dict['name']
            self.version = dict['version']
            self.charge = dict['charge']
            self.offcharging = dict['offcharging']
            self.oncharging = dict['oncharging']
        self.onoff = False
        th = threading.Thread(target=self.battery_level, args=())
        th.start()

    def battery_level(self):    # 배터리 잔량을 시간에 따라 조정해주는 스레드 함수
        while True:

            # 배터리가 충전중인지 아닌지에 대한 체크입니다.
            if self.onoff == False:
                self.charge -= self.offcharging
            elif self.onoff == True:
                self.charge += self.oncharging

            # 배터리의 최대와 최소를 체크합니다.
            if self.charge > 100:
                self.charge = 100
            elif self.charge < 0:
                self.charge = 0

            self.charge = round(self.charge, 2)         # 주의, 이 줄은 부동소수점 특유의 오류를 개선하기 위한 코드입니다.

            # 아래 주석은 디버그용 코드
            # print("Level : %f, Name : %s, Version : %s, isCharging? : %r, offValue : %f, onValue : %f" % (self.charge, self.name, self.version, self.onoff, self.offcharging, self.oncharging))

            time.sleep(1)
            if is_quit == True:
                return None

    def charging(self, tf):
        if tf == None:
            self.onoff = not self.onoff
        if str(type(tf)) == "<class 'int'>":
            self.charge = tf
        if str(type(tf)) == "<class 'bool'>":
            self.onoff = tf

    def getLevel(self):
        return self.charge
    
    def ischarging(self):
        return self.onoff

    def getName(self):
        return self.name

    def getVersion(self):
        return self.version

class GpsDemon:
    def __init__(self, dict) -> None:
        if dict == None:
            self.dict = droneInfo
        else :
            self.dict = dict

    def getLoction(self):
        return self.dict
    
    def setLocation(self, dict):
        self.dict = dict

class DroneDemon:
    def __init__(self, dict) -> None:
        if dict == None:
            self.id = "1"
            self.os = "Demon"
            self.firmware = "0.0.1"
            self.descript = ""
        else:
            self.id = dict['id']
            self.os = dict['OS']
            self.firmware = dict['firmware']
            self.descript = dict['Descript']
    
    def getOS(self):
        return self.os
    
    def getFirmware(self):
        return self.firmware
    
    def getHash(self):
        return self.hash
    
    def getDescript(self):
        return self.descript

class movement:
    def __init__(self) -> None:
        pass

class request:
    ### 참고 https://velog.io/@dmstj907/Python-REST-API-%EC%8B%A4%EC%8A%B5
    ### REST GET
    # import requests
    # import json

    # url_items = "http://localhost:3000/todos/1"
    # response = requests.get(url_items)

    # print(response.text)
    # print(response.json()["content"])

    ### REST POST
    # import requests
    # import json

    # url_items = "http://localhost:3000/todos"
    # #response = requests.get(url_items)

    # newItem = {
    #     "id": 4,
    #     "content": "Python",
    #     "completed": True
    #     }
    # response = requests.post(url_items, data=newItem)

    # print(response.text)

    def __init__(self) -> None:
        self.url = "http://project-geek.cc"
        pass

    def get(self, arr):
        self.uri = arr['uri']
        self.json = json.dumps(arr['dict'])

        req = self.url + self.uri + self.json
        rsp = requests.get(req)
        print(rsp.text)
        return json.loads(rsp.text)

    def post(self, arr):
        self.uri = arr['uri']
        dict = arr['dict']
        json_dict = json.dumps(dict)
        req = self.url + self.uri + json_dict
        print("req : %s" % req)
        rsp = requests.post(req, data=None)
        print(rsp.text)
        return json.loads(rsp.text)

    def put(self, arr):
        self.uri = arr['uri']
        dict = arr['dict']
        json_dict = json.dumps(dict)
        req = self.url + self.uri + json_dict
        rsp = requests.put(req, data=arr['dict'])
        print(rsp.text)
        return json.loads(rsp.text)

## 초기 실행
if __name__ == "__main__":
    req = request()
    
    id = int(input("Drone id : "))
    return_json = req.get({
        "uri" : "/drone/",
        "dict" : {
            "id" : id
        }
    })
    droneInfo['id'] = id
    info = DroneDemon(droneInfo)

    if(return_json['error']):
        return_json = req.post({
            "uri" : '/drone/',
            "dict" : droneInfo
        })
        print(return_json)

        if(return_json['error']):
            quit()

    bt = BatteryDemon(batteryInfo)
    gps = GpsDemon(gpsInfo)


    # 하단은 반복문
    try:
        while True:
            time.sleep(1)
            dict = {
                'uri' : '/drone/gps/'
            }
            dict['dict'] = gps.getLoction()
            dict['dict']['id'] = droneInfo['id']
            dict['dict']['bat'] = bt.getLevel()
            print(dict)
            req.post(dict)
    except KeyboardInterrupt as e:
        is_quit = True
        quit()
