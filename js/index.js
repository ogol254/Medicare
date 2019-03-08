$( document ).ready(function() {
    $('#sidebar').load('sidebar.html');
    $('#header-area').load('headers.html');
    
});



const token = localStorage.getItem("AuthToken");

const header = {
    "Content-type" : "application/json",
    "Authorization" : `Bearer ${token}`
}

const getconfig = {
        method: 'GET',
        headers: header
    }

if (token === null){
    redirect: window.location.replace("index.html") 
}else{
    const config = {
        method: 'POST',
        headers: header
    }
    
    fetch(`https://medicarea.herokuapp.com/api/v1/auth/validate`, config)
        .then(res => res.json())
        .then(data => {
            if (data.message === 'Valid'){
                $('#welcome').text(data.name)
            }else{
                redirect: window.location.replace("index.html") 
            }
    
        })
}




