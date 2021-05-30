
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
            return xhr.responseText
        }
    }
    xhr.send();
    if(xhr.status === 200) {       // 성공
        return xhr.responseText
        }
    else {                      // response 실패
        console.log('Error!');
        console.log(xhr.responseText);
        }
}