const table  = document.querySelector('table');
const form  = document.querySelector('form');
    
fetch(`https://medicarea.herokuapp.com/api/v1/incidents`, getconfig)
    .then((response) => {
        response.json().then(data => {
            const users = Object.values(data.incidents)
            // console.log(users)
            let html = `
            <table id="example23" class="display nowrap table table-hover table-striped table-bordered" cellspacing="0" width="100%">
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
            html += `</tbody> </table>`
            $('#content').html(html)
        })
    })

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
form.addEventListener('submit', Addincident);



