$( document ).ready(function() {
    $('#header-area').load('headers.html');
    $('#sidebar').load('sidebar.html');

});

const token = localStorage.getItem("AuthToken");
if (token === null){
    redirect: window.location.replace("index.html") 
}else{
    const config = {
        method: 'POST',
        headers: {
            "Content-type" : "application/json",
            "Authorization" : `Bearer ${token}`
        }
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

