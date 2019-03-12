const table  = document.querySelector('table');
const form  = document.querySelector('form');
const showalert = document.getElementById('alertarea');

// const uri = "";

$( document ).ready(function() {

    
    fetch(`https://medicarea.herokuapp.com/api/v1/incidents`, getconfig)
        .then((response) => {
            response.json().then(data => {
                const users = Object.values(data.incidents)
                // console.log(users)
                let html = `
                <thead>
                <tr>
                    <th>Incident #</th>
                    <th>Reporter </th>
                    <th>Tell</th>
                    <th>Address</th>
                    <th>Status</th>
                    <th>Action</th>
                </tr>
                </thead> 
                <tbody>`
                users.forEach((single) => {
                html += ` 
                <tr>
                    <td>${single.incident_id}</td>
                    <td>${single.reported_by}</td>
                    <td>${single.tell}</td>
                    <td>${single.location}</td>
                    <td>${single.status}</td>
                    <td>
                        <a href="view-incident.html?incident_id=${single.incident_id}"><i class="fa fa-edit"></i> </a>
                    </td>
                </tr> 
                 `
                })
                html += `</tbody> `
                table.innerHTML = html
            })
        })
        
});

form.addEventListener('submit', Addincident);

function Addincident(e){
    e.preventDefault();
    
    const name = document.getElementById('val-name').value;
    const description = document.getElementById('val-description').value;
    const tell = document.getElementById('val-phoneus').value;
    const type = document.getElementById('val-type').value;
    const location = document.getElementById('val-address').value;

    const configpost = {
        method: 'POST',
        headers: header,
        body: JSON.stringify({
            "name": name,
            "location": location,
            "tell": tell,
            "type": type,
            "description": description
        })
    }

    fetch(`https://medicarea.herokuapp.com/api/v1/incidents`, configpost)
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

// -------------------------------------------------
// Viewing specific incidents
// -------------------------------------------------

// console.log(incident_id)



