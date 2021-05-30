
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

function restful(uri, json, REST){
    const xhr = new XMLHttpRequest();
    //var url = '/drone/gps/';
    var url = uri + JSON.stringify(json);
    console.log(url)
    xhr.open(REST, encodeURI(url), true);  // form태그안에 어트리뷰트 써준거와 같다.
    xhr.onreadystatechange = function() {
        if(xhr.readyState == 4 && xhr.status == 200){
            console.log(xhr.responseText.replace("'", "\""));
        }
    }
    xhr.send();
    if(xhr.status === 200) {       // 성공
        console.log(xhr.responseText);   // responseText -> response body안에 들어있는 값이 text로 들어있다.
        console.log(xhr.responseType)
        parsing(xhr.responseText)
        return xhr.responseText
        }
    else {                      // response 실패
        console.log('Error!');
        console.log(xhr.responseText);
        }
}