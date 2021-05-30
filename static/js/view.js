var page_state = "page_loading";

page_list = ["page_loading", "page_login", "page_join", "page_main", "page_information", "page_rent", "page_map", "page_camera"]

function refresh(str){
    document.getElementById(page_state).style.display="none";
    document.getElementById(str).style.display="block";
    page_state = str
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

    var result = restful(uris['client'], json, "GET");

    console.log(typeof(result))
    var result_json = JSON.parse(result);
    if(result_json.error == 'False'){
        refresh(page_list[3])
    }
    else if(result_json.error == 'True'){
        alert(result_json.message)
    }
    else {
        alert('알려지지 않은 오류!')
    }
}

function loading(){
    refresh(page_list[1])
}

refresh(page_list[0])