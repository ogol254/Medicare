const table  = document.querySelector('table');
const form  = document.querySelector('form');
const showalert = document.getElementById('alertarea');

$( document ).ready(function() {

    
    
    fetch(`https://medicarea.herokuapp.com/api/v1/users`, getconfig)
        .then((response) => {
            response.json().then(data => {
                const users = Object.values(data.users)
                // console.log(users)
                let html = `
                <thead>
                <tr>
                    <th>ID Number</th>
                    <th>First Name </th>
                    <th>Last Name</th>
                    <th>Address</th>
                    <th>Tell</th>
                    <th>Action</th>
                </tr>
                </thead>
                <tbody>`
                users.forEach((single) => {
                html += ` 
                <tr>
                    <td>${single.id_number}</td>
                    <td>${single.first_name}</td>
                    <td>${single.last_name}</td>
                    <td>${single.address}</td>
                    <td>${single.tell}</td>
                    <td>
                        <a href="/profile.html?id=${single.id_number}"><i class="fa fa-edit"></i> </a>
                        <a href="/profile.html?id=${single.id_number}"><i class="fa fa-snowflake-o"></i> </a>
                    </td>
                </tr> 
                 `
                })
                html += `</tbody> `
                table.innerHTML = html
            })
        })
        
});

form.addEventListener('submit', PostUser);

function PostUser(e){
    e.preventDefault();
    
    const id_number = document.getElementById('val-id-num').value;
    const last_name = document.getElementById('val-lname').value;
    const first_name = document.getElementById('val-fname').value;
    const password = document.getElementById('val-password').value;
    const tell = document.getElementById('val-phoneus').value;
    const role = document.getElementById('val-role').value;
    const address = document.getElementById('val-address').value;

    const configpost = {
        method: 'POST',
        headers: header,
        body: JSON.stringify({
            "id_number": parseInt(id_number),
            "first_name": first_name,
            "last_name": last_name,
            "address": address,
            "tell": tell,
            "role": role,
            "password": password
        })
    }

    fetch(`https://medicarea.herokuapp.com/api/v1/users`, configpost)
        .then(response => response.json())
        .then(data => successalert(data.message))
}

function successalert(response) {
    const alert = `
    <div class="alert alert-primary alert-dismissible fade show">
        <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <strong>Holy guacamole!</strong> ${response}.
    </div>`
    showalert.innerHTML = alert  
}