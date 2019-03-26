const table  = document.querySelector('table');
const form  = document.querySelector('form');
const showalert = document.getElementById('alertarea');

fetchData(`https://medicarea.herokuapp.com/api/v1/facilities`)
        .then(res => {
            var data = res.facilities
            if (data.length === 0){
                var html = `<div class="card well well-sm">No facilities so far</div>`
                $('#data').html(html)
            }else{
                var html = `
                <thead>
                <tr>
                    <th>Facility ID#</th>
                    <th>Name </th>
                    <th>Level</th>
                    <th>Location</th>
                    <th>Action</th>
                </tr>
                </thead> 
                <tbody>`
            data.forEach((single) => {
            html += ` 
            <tr>
                <td>${single.facility_id}</td>
                <td>${single.name}</td>
                <td>${single.level}</td>
                <td>${single.location}</td>
                <td>
                    <a href="view_facilty.html?record_id=${single.record_id}"><i class="fa fa-edit"></i> </a>
                </td>
            </tr> 
            `
            })
            html += `</tbody> `
            table.innerHTML = html
            }
        })



function PostFacility(e){
    e.preventDefault();
    
    const name = document.getElementById('val-fname').value;
    const tell = document.getElementById('val-phoneus').value;
    const location = document.getElementById('val-address').value;
    const level =  document.getElementById('val-role').value;

    const configpost = {
        method: 'POST',
        headers: header,
        body: JSON.stringify({
            "name": name,
            "location": location,
            "contact": tell, 
            "level": level
        })
    }

    fetch(`https://medicarea.herokuapp.com/api/v1/facilities`, configpost)
        .then(response => response.json())
        .then(data => {
            if (data.message === "Success"){
                form.reset();
                successalert(data.message)
            }else{
                dangeralert(data.message) 
            }
            
        })
}

// successalert
form.addEventListener('submit', PostFacility);


