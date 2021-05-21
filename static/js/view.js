var page_state = "page_loading";

page_list = ["page_loading", "page_login", "page_join", "page_main", "page_information", "page_rent", "page_map", "page_camera"]

function refresh(str){
    document.getElementById(page_state).style.display="none";
    document.getElementById(str).style.display="block";
    page_state = str
}

refresh(page_list(0))
