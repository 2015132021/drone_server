var page_state = 0;

page_list = ["page_loading", "page_login", "page_join", "page_main", "page_information", "page_rent", "page_map", "page_camera"]

function refresh(num){
    document.getElementById(page_list[page_state]).style.display="none";
    document.getElementById(page_list[num]).style.display="block";
    page_state = num
}

refresh(0)
