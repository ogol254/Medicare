$( document ).ready(function() {
    $('#header-area').load('headers.html');
    $('#sidebar').load('sidebar.html');   
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
                $('#profile-link').html(`<a href="/profile.html?id=${data.id_num}"><i class="ti-user"></i> Profile</a>`)
            }else{
                redirect: window.location.replace("index.html") 
            }
    
        })
}

function logout() {
        const config = {
            method: 'POST',
            headers: header
        }

        fetch(`https://medicarea.herokuapp.com/api/v1/auth/signout`, config)
        .then(checkstatus)
        .then(response => {
            if (response.status === 200){
                localStorage.removeItem("AuthToken")
                redirect: window.location.replace("index.html")
            }
        })
}



function fetchData (url) {
    return fetch(url, getconfig)
        // .then(checkpermission)
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
        
function checkpermission(response) {
    if (response.status === 404){
        redirect: window.location.replace("404.html") 
    }else if(response.status === 401){
        redirect: window.location.replace("401.html")
    }
}

function checkstatus(response) {
    if (response.ok) {
        return Promise.resolve(response);
    }else{
        return Promise.reject(new Error(response));
    }
} 

function successalert(response) {
    const alert = `
    <div class="alert alert-success alert-dismissible fade show">
        <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <strong>Well done!</strong> ${response}
    </div>`
    $('#show-alert').html(alert)  
} 

function dangeralert(response) {
    const alert = `
    <div class="alert alert-danger alert-dismissible fade show">
        <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <strong>Oh snap!</strong> ${response}
    </div>`
    $('#show-alert').html(alert)  
}




