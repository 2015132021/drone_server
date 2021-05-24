var page_state = "page_loading";

page_list = ["page_loading", "page_login", "page_join", "page_main", "page_information", "page_rent", "page_map", "page_camera"]

function refresh(str){
    document.getElementById(page_state).style.display="none";
    document.getElementById(str).style.display="block";
    page_state = str
}

function join(){
    id = document.getElementById("join_id").value
    pw = document.getElementById("join_pw").value
    email = document.getElementById("join_email").value
    phone = document.getElementById("join_phone").value
    json = {
        "id" : id,
        "pw" : pw,
        "email" : email,
        "phone" : phone
    }
    alert(json)

    restful(uris['client'], json, "POST");
}

function login(){

}

function loading(){
    refresh(page_list[1])
}

refresh(page_list[0])