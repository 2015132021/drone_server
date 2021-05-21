var page = 0;

document.getElementsByClassName("page").style.display="none";

function refresh(){
    switch(page){
        case 0:
            document.getElementById("page_loading").style.display="block";
    }
}