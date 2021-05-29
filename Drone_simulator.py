####
# 드론의 데이터를 서버에 전송하기 위한 시뮬레이터입니다.
# 존재하는 모듈은 실제 데이터를 받고, 존재하지 않는 모듈은 가상화를 하여 전송하게 됩니다.
####

import time
import threading

batteryInfo = {     # 배터리 종류, 버전 등에 대한 데몬정보
    "name" : "Demon_1.0",
    "version" : "1.0",
    "charge" : 100,
    "offcharging" : 0.05,
    "oncharging" : 0.5
}

gpsInfo = {         # GPS에 대한 데몬 정보
    # 신구대학교 위치 37.44904171317658, 127.16785865546673, 0.0002
    "lat" : 37.44904171317658,
    "lng" : 127.16785865546673
}

droneInfo = {       # 드론에 대한 데몬정보
    "OS" : "Demon",
    "firmware" : "0.0.1",
    "hash key" : None,
    "Descript" : "This Drone is Demon"
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
            self.os = "Demon"
            self.firmware = "0.0.1"
            self.hash = None
            self.descript = ""
        else:
            self.os = dict['OS']
            self.firmware = dict['firmware']
            self.hash = dict['hash key']
            self.descript = dict['Descript']
    
    def getOS(self):
        return self.os
    
    def getFirmware(self):
        return self.firmware
    
    def getHash(self):
        return self.hash
    
    def getDescript(self):
        return self.descript


if __name__ == "__main__":
    bt = BatteryDemon(batteryInfo)
    gps = GpsDemon(droneInfo)
    info = DroneDemon(droneInfo)