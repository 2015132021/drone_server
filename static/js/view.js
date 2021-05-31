//document.cookie = "user=John"; // 이름이 'user'인 쿠키의 값만 갱신함
alert(document.cookie);
var page_state = "page_loading";

page_list = ["page_loading", "page_login", "page_join", "page_main", "page_information", "page_rent", "page_map", "page_camera"]

function refresh(str){
    document.getElementById(page_state).style.display="none";
    document.getElementById(str).style.display="block";
    page_state = str
}

var uris = {
    drone_gps : "/drone/gps/",
    client_gps : "/client/gps/",
    client_log : "/client/log/",
    client_login : "/client/login/",
    client : "/client/",

}

function parsing(str){
    var string = String(str).split('\n')

    for(var i; i > string.length(); i++){
        console.log(string[i])
    }

    return string
}

function restful(uri, json, REST, a, b, c){
    var url = uri + JSON.stringify(json);
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
                a(b)
                c(json.id, json.pw)
            }
            else if(return_json.error == true){
                alert(return_json.message)
            }
            else {
                alert('알려지지 않은 오류!')
            }
        }
    }

    // open() 메서드는 요청을 준비하는 메서드입니다. (http 메서드, 데이터를 받아올 URL 경로, 비동기 여부)
    xhr.open(REST, url, true);

    // send() 메서드는 준비된 요청을 서버로 전송하는 메서드입니다. (서버에 전달될 정보)
    xhr.send("");
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

    var result = restful(uris['client'], json, "POST");
    console.log(result);
}

function login(){
    id = document.getElementById("login_id").value;
    pw = document.getElementById("login_pw").value;
    json = {
        "id" : id,
        "pw" : pw
    };
    restful(uris['client_login'], json, "GET", refresh, page_list[3], login_correct);
}
function login_correct(id, pw){
    document.cookie = "id=" + id; // 이름이 'user'인 쿠키의 값만 갱신함
    document.cookie = "pw=" + pw; // 이름이 'user'인 쿠키의 값만 갱신함
}

function loading(){
    refresh(page_list[1])
}

refresh(page_list[0])