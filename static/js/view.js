var page_state = 0;

page_list = ["page_loading", "page_login", "page_join", "page_main", "page_information", "page_rent", "page_map", "page_camera"]

for(var i = 1; i < page_list.length; i++){
    console.log(page_list[i] + " is none")
    document.getElementById(page_list[i]).style.display="none";
}

function refresh(){
    for(var i = 0; i > page_list.length; i++){
        if(page_state != i){
            document.getElementById(page_list[i]).style.display="none";
        }
        else{
            document.getElementById(page_list[i]).style.display="block";
        }
    }
}