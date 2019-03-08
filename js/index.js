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


function fetchData (url) {
    return fetch(url, getconfig)
        .then(checkstatus)
        .then(res => res.json())
        .catch(err => console.log('Looks there was a proble', err))
    }


function checkvalidity(url) {
        fetch(url, getconfig)
            .then(response => {
                if (response.status === 404){
                    redirect: window.location.replace("404.html") 
                }else if(response.status === 401){
                    redirect: window.location.replace("401.html")
                }
            })
    
        }  

function checkstatus(response) {
    if (response.ok) {
        return Promise.resolve(response);
    }else{
        return Promise.reject(new Error(response.statusText));
    }
}       


