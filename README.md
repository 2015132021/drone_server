README
===

# Server - Flask (Python3)
이 서버는 파이썬3의 Flask기반 서버입니다.
2015132021
해당 서버는 project-geek.cc로 서비스되고 있습니다.

## Flask의 REST 호출

### /hello
GET : 서버가 살아있는지 확인하기 위한 호출

### /drone/gps/<string:data>
GET : json string {id} 을 전달받고, 해당 id를 가진 드론의  GPS(lat, lng)를 반환  
POST : json string {id, lat, lng} 을 전달받고, 현재 시간과 함께 DB에 저장

### /client/<string:data>
GET : json string {id, pw} 을 전달받고, 해당 id의 Client의 pw hash가 전달받은 pw의 hash와 일치하는지 비교하여 결과를 반환  
POST : json string {id, pw, email, phone}을 전달받고, DB에 저장하며, 동일한 Unique key 입력 시 error:Ture 반환 

### /client/gps/<string:data>
GET : json string {id}을 전달받고, 해당 id를 가진 Client의  GPS(lat, lng)를 반환
POST : json string {id, lat, lng} 을 전달받고, 현재 시간과 함께 DB에 저장

### /client/log/<string:data>
GET : json string {id} 을 전달받고, 해당 id를 가진 Client의 Logs를 반환

## mariaDB 연동
``` python
with open('/json/mariaDB.json', 'r') as f:
    json_data = json.load(f)
print(json.dumps(json_data))
maria = mariadb_master.Mariadb(json_data)
```
보안 상 문제가 있을 수 있으므로, 해당 부분은 외부 파일로 대체합니다.
/json/mariaDB.json 파일을 읽기 전용으로 읽어옵니다.
읽어온 파일은 딕셔너리로 저장되며, Mariadb 클래스 생성자 호출 시 사용되어집니다.
Mariadb 클래스는 import된 mariadb_master.py 파일 내 있습니다.

## HTML파일 제공
### /index
/index URI에서 index.html 파일을 제공함. 해당 파일은 templates/ 에 존재
HTML파일에서 호출하는 css와 js파일은 static/ 에 존재


# Android - Java
Java기반 안드로이드 어플리케이션입니다.

## activity
레이아웃 파일에 대한 내용입니다.

### loading.xml
어플리케이션 초기 설정을 로딩하는 단계 
- 로컬에 저장된 해시 파일을 읽어옵니다.
    - 저장된 파일이 없다면 login.xml로 이동합니다.
    - 저장된 파일이 있다면 해시를 읽고 서버로 전송하여 자동 로그인을 시도합니다.
        - 일치한다면 main.xml로 이동합니다.
        - 일치하지 않다면 login.xml로 이동합니다.

### login.xml
로그인 단계
- 서버로 로그인을 시도합니다.
    - 올바르지 않은 시도라면 실패합니다.
    - 올바른 시도라면 서버에서 전달받은 해시를 로컬에 저장한 후, main.xml로 이동합니다.
- Join을 눌러 가입 페이지로 이동합니다.

### join.xml
가입 단계
- ID, PW, email, phone number를 전달받아 서버로 전송하여 가입을 시도합니다.
    - ID, email에 중복 데이터가 있을 경우, 가입이 실패합니다. ( email 인증은 미구현 )
    - 가입이 성공한 경우 login.xml로 이동합니다.

### main.xml
메인 페이지
- Rent 항목
    - rent.xml로 이동합니다.
- my information 항목
    - myinfo.xml로 이동합니다.
- 사용 로그 항목
    - loglist.xml로 이동합니다.

### rent.xml
드론 대여 시도 단계
- 이 단계에서부터 서버에 자신의 GPS 위치를 지속적으로 전송합니다.
- 또한, 서버에 가용 드론 배치를 요청합니다.
    - 요청이 수락되면 map.xml로 넘어갑니다.
    - 요청이 반려되면 실패 메시지를 띄운 후, main.xml로 돌아갈 수 있게 합니다.

### 