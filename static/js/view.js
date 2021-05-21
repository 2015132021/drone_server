var page = 0;

page = ["page_loading", "page_login", "page_join", "page_main", "page_information", "page_rent", "page_map", "page_camera"]

for(var i = 0; i > page.length; i++){
    document.getElementById(page[i]).style.display="none";
}

function refresh(){
    switch(page){
        case 0:
            document.getElementById("page_loading").style.display="block";
    }
}