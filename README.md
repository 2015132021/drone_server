# 드론 서버
이 서버는 파이썬3의 Flask기반 서버입니다.


## mariaDB 연동
``` python
with open('/json/mariaDB.json', 'r') as f:
    json_data = json.load(f)
print(json.dumps(json_data))
maria = mariadb_master.Mariadb(json_data)
```
/json/mariaDB.json 파일을 읽기 전용으로 읽어옵니다.
읽어온 파일은 딕셔너리로 저장되며, Mariadb 클래스 생성자 호출 시 사용되어집니다.

## Flask의 REST 호출
### /hello
GET : 서버가 살아있는지 확인하기 위한 호출

### /drone/gps/<string:data>
GET : json string {id} 을 전달받고, 해당 id를 가진 드론의  GPS(lat, lng)를 반환  
POST : json string {id, lat, lng} 을 전달받고, 현재 시간과 함께 DB에 저장

### /client/gps/<string:data>
GET : json string {id}을 전달받고, 해당 id를 가진 Client의  GPS(lat, lng)를 반환
POST : json string {id, lat, lng} 을 전달받고, 현재 시간과 함께 DB에 저장

### /client/<string:data>
GET : json string {id, pw} 을 전달받고, 해당 id의 Client의 pw hash가 전달받은 pw의 hash와 일치하는지 비교하여 결과를 반환  
POST : json string {id, pw, email, phone}을 전달받고, DB에 저장하며, 동일한 Unique key 입력 시 error:Ture 반환 