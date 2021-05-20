// XMLHttpRequest 객체의 생성
const xhr = new XMLHttpRequest();
// 비동기 방식으로 Request를 오픈한다
var url = '/drone/gps/';
var json = {id:"1"};
url = url + JSON.stringify(json);
console.log(url)
xhr.open('GET', encodeURI(url), true);  // form태그안에 어트리뷰트 써준거와 같다.
xhr.onreadystatechange = function() {
    if(xhr.readyState == 4 && xhr.status == 200){
        console.log(xhr.responseText);
    }
}

xhr.send();

if(xhr.status === 200) {       // 성공
    console.log(xhr.responseText);   // responseText -> response body안에 들어있는 값이 text로 들어있다.
    }
else {                      // response 실패
    console.log('Error!');
    }