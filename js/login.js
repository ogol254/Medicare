const form = document.querySelector('form');
const errorplace = document.getElementById('error')
form.addEventListener('submit', LoginUser);

function LoginUser (e) {
    e.preventDefault();

    const id = document.getElementById('id_number').value;
    const password = document.getElementById('password').value;

    const config = {
        method: 'POST',
        headers: {
            'Content-type' : 'application/json'
        },
        body: JSON.stringify({
            "id_number" : parseInt(id),
            "password" : password
        })
    }

    fetch(`https://medicarea.herokuapp.com/api/v1/auth/signin`, config)
        // .then(checkstatus)
        .then(res => res.json())
        .then(data => {
            if (data.message === "Success") {
                localStorage.setItem("AuthToken", data.AuthToken);
                redirect: window.location.replace("home.html") 
            }else{
                handleerrors(data.message)
                console.log(data.message)
            }
        })
        .catch(err => console.log('Something is wrong', err))

}

function handleerrors (error) {
    const html = `
    <div class="alert alert-danger" role="alert">${error}</div>
    `
    errorplace.innerHTML = html
}
