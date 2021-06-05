/*****************
현재 페이지에 관한 데이터를 담고 있는 내용입니다.
*****************/

// 현재 페이지 정보
var page_state = "page_loading";

// 페이지 목록
page_list = ["page_loading", "page_login", "page_join", "page_main", "page_information", "page_rent", "page_map", "page_camera"]

// 페이지를 새로고침 할 때, 이전 페이지를 안보이게 만들고 다음 페이지를 보이게 만듭니다. 그 후 현재 페이지 정보를 고칩니다.
function refresh(str){
    document.getElementById(page_state).style.display="none";
    document.getElementById(str).style.display="block";
    page_state = str
}

// 현재 페이지를 로딩 페이지로 바꿉니다.
refresh(page_list[0])



/*****************
REST API에 대해 사전 설정하는 내용입니다.
*****************/
// 동작 별 접근 주소에 대한 내용입니다.
var uris = {
    drone_gps : "/drone/gps/",
    client : "/client/",
    client_gps : "/client/gps/",
    client_log : "/client/log/",
    client_login : "/client/login/",
    client_logout : "/client/logout/",
    client_rent : "/client/rent/"
}

// 스트링 파싱
function parsing(str){
    var string = String(str).split('\n')

    for(var i; i > string.length(); i++){
        console.log(string[i])
    }

    return string
}

// REST API 실행하는 내용
function restful(json){
    /*
        json으로 넘겨받습니다.
        json = {
            uri = "/uri/ 데이터",
            json = "전달해 줄 json",
            REST = GET / POST 등등 입니다
            success = 성공 시 실행할 함수입니다.
            failed = 실패시 실행할 함수 입니다.
        }

    */
    var url = json['uri'] + JSON.stringify(json['json']);
    console.log("url : " + url)
    // XMLHttpRequest 객체의 인스턴스를 생성합니다.
    var xhr = new XMLHttpRequest();

    xhr.onload = function () {
        // xhr 객체의 status 값을 검사한다.
        if (xhr.status === 200) {
            console.log(xhr.responseText)
            return_json = JSON.parse(xhr.responseText)
            console.log(return_json)
            if(return_json.error == false){
                json['success'](return_json)
            }
            else if(return_json.error == true){
                json['failed'](return_json)
            }
            else {
                console.log('알려지지 않은 오류!')
            }
        }
    }

    // open() 메서드는 요청을 준비하는 메서드입니다. (http 메서드, 데이터를 받아올 URL 경로, 비동기 여부)
    xhr.open(json['REST'], url, true);

    // send() 메서드는 준비된 요청을 서버로 전송하는 메서드입니다. (서버에 전달될 정보)
    xhr.send("");
}

/*
쿠키 제어하는 함수입니다.
getCookie(name) -> name의 이름을 가진 쿠키의 값을 가져옵니다.
setCookie(name, value) name의 이름에 value의 값을 넣은 쿠키를 저장합니다.
delCookie([name1, name2, name3]) 각 이름의 쿠키를 지웁니다.
*/
function getCookie(name) {
    var value = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return value? value[2] : null;
}

function setCookie(name, value) {
    document.cookie = name + "=" + value
}

function delCookie(arr){
    for(i = 0; i < arr.length; i++){
        document.cookie = arr[i] + '=; expires=Thu, 01 Jan 1999 00:00:10 GMT;'
    }
}


/*
각 페이지 별, 동작 별 실행하는 함수에 관한 내용입니다.
AJAX로 넘겨줄 restful()의 인자 json은 아래와 같습니다.

json으로 넘겨받습니다.
json = {
    uri = "/uri/ 데이터",
    json = "전달해 줄 json",
    REST = GET / POST 등등 입니다
    success = 성공 시 실행할 함수입니다.
    failed = 실패시 실행할 함수 입니다.
}

최종적으로, 기본적인 함수의 폼은 아래와 같습니다.
function func(){
    json = {
        "key" : value,

    }
    restjson = {
        "uri" : uris[uri_name],
        "json" : json,
        "REST" : "GET" / "POST",
        "success" : function(return_json){
            //success function
        },
        "failed" : function(return_json){
            console.log("error!")
        }
    }

    var result = restful(restjson);
    console.log(result);
}

*/
function loading(){
    if(getCookie('id') != null & getCookie('hash') != null){
        json = {
            "id" : getCookie('id'),
            "hash" : getCookie('hash')
        }
        restjson = {
            "uri" : uris['client_login'],
            "json" : json,
            "REST" : "GET",
            "success" : function(return_json){
                refresh(page_list[3])
            },
            "failed" : function(return_json){
                console.log("error!")
                refresh(page_list[1])
            }
        }
        console.log(json)
        restful(restjson);
    }
    else{
        refresh(page_list[1])
    }
}

function login(){
    id = document.getElementById("login_id").value;
    pw = document.getElementById("login_pw").value;
    json = {
        "id" : id,
        "pw" : pw
    }

    restjson = {
        "uri" : uris['client_login'],
        "json" : json,
        "REST" : "GET",
        "success" : function(return_json){
            console.log("login")
            setCookie('id', return_json['id'])
            setCookie('hash', return_json['hash'])
            refresh(page_list[3])
        },
        "failed" : function(return_json){
            console.log("error!")
        }
    }
    restful(restjson);
}

function join(){
    id = document.getElementById("join_id").value;
    pw = document.getElementById("join_pw").value;
    email = document.getElementById("join_email").value;
    phone = document.getElementById("join_phone").value;
    json = {
        "id" : id,
        "pw" : pw,
        "email" : email,
        "phone" : phone
    };
    
    restjson = {
        "uri" : uris['client'],
        "json" : json,
        "REST" : "POST",
        "success" : function(return_json){
            console.log("success!")
            refresh(page_list[1])
        },
        "failed" : function(return_json){
            console.log("error!")
        }
    }

    var result = restful(restjson);
    console.log(result);
}

// gps 전송 루프
var gps_stop = false
var gps_isrun = false

function rent(){
    refresh(page_list[5])
    document.getElementById("rent_stat").innerHTML="서칭중..."
    
    json = {
        "id" : getCookie('id'),
        "hash" : getCookie('hash')
    };
    
    restjson = {
        "uri" : uris['client'],
        "json" : json,
        "REST" : "GET",
        "success" : function(return_json){
            console.log("success!")
            refresh(page_list[6])

            if(gps_isrun == false){
                gps_isrun = true
                setInterval(function(){
                    console.log("123")
                    getLocation();
                }, 1000)
            }
        },
        "failed" : function(return_json){
            console.log("error!")
        }
    }
    restful(restjson);
}

function getLocation() {
    if (/*navigator.geolocation*/ false) { // GPS를 지원하면
      navigator.geolocation.getCurrentPosition(function(position) {
        alert(position.coords.latitude + ' ' + position.coords.longitude);
      }, function(error) {
        console.error(error);
      }, {
        enableHighAccuracy: false,
        maximumAge: 0,
        timeout: Infinity
      });
    } else {
      console.log('GPS를 지원하지 않습니다');
    }
  }


function myinfo(){
    json = {
        "id" : getCookie('id')
    }
    restjson = {
        "uri" : uris['client'],
        "json" : json,
        "REST" : "GET",
        "success" : function(return_json){
            console.log(JSON.stringify(return_json))
            refresh(page_list[4])
        },
        "failed" : function(return_json){
            console.log("error!")
        }
    }

    var result = restful(restjson);
    console.log(result);
}

function mylogs(){

}

function logout(){
    json = {
        "id" : getCookie('id')
    }
    restjson = {
        "uri" : uris['client_logout'],
        "json" : json,
        "REST" : "GET",
        "success" : function(return_json){
            delCookie["id", "pw", "hash"]
            refresh(page_list[1])
        },
        "failed" : function(return_json){
            console.log("error!")
        }
    }
    restful(restjson);
}


function tomain(){
    refresh(page_list[3])
}