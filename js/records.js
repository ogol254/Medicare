const table  = document.querySelector('table');
const form  = document.querySelector('form');
const showalert = document.getElementById('alertarea');


// const uri = "";

$( document ).ready(function() {
    fetchData(`https://medicarea.herokuapp.com/api/v1/records`)
        .then(response => showrecords(response))       
});

function searchrecord() {
    var id  = document.getElementById('searid_num').value;
    var url = `https://medicarea.herokuapp.com/api/v1/records/search/${id}`
    fetchData(url)
        .then(response => showrecords(response))
}

function showrecords (response){
        const records = Object.values(response.records)
        if (records.length === 0){
            var html = `<div class="card well well-sm">No records so far</div>`
            $('#data').html(html)
        }else{
            // console.log(records)
            let html = `
            <thead>
            <tr>
                <th>Record #</th>
                <th>Name </th>
                <th>Days</th>
                <th>Facility</th>
                <th>Status</th>
                <th>Action</th>
            </tr>
            </thead> 
            <tbody>`
            records.forEach((single) => {
            html += ` 
            <tr>
                <td>${single.record_id}</td>
                <td>${single.name}</td>
                <td>${single.created_on}</td>
                <td>${single.facility_id}</td>
                <td>${single.status}</td>
                <td>
                    <a href="view_record.html?record_id=${single.record_id}"><i class="fa fa-edit"></i> </a>
                </td>
            </tr> 
            `
            })
            html += `</tbody> `
            table.innerHTML = html
        }
}

form.addEventListener('submit', showrecords);