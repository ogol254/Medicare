const table  = document.querySelector('table');
const form  = document.querySelector('form');
const showalert = document.getElementById('alertarea');


// const uri = "";

$( document ).ready(function() {
    fetchData(`https://medicarea.herokuapp.com/api/v1/records`)
        .then(response => showrecords(Object.values(response.records)))       
});

function searchrecord(e) {
    e.preventDefault();
    var id  = document.getElementById('searid_num').value;
    var url = `https://medicarea.herokuapp.com/api/v1/records/search/${id}`
    fetchData(url)
        .then(response => {
            var data = response.Records
            if (data === "No record(s) with that user"){
                var html = `
                    <div class="card">
                    <div class="card-body">
                        <div class="alert alert-danger alert-dismissible fade show">
                            <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                            <strong> No record(s) with that user ID </strong>
                        </div>
                    </div>
                    </div>
                `
                $('#hideafter').hide()
                $('#searchresult').html(html) 
            }else{
                let html = `
                    <div class="card"><div class="card-body"><div id="data" class="table-responsive m-t-40">
                    <table id="example23" class="display nowrap table table-hover table-striped table-bordered" cellspacing="0" width="100%">
                    <thead>
                        <tr>
                            <th>Record #</th><th>Name </th><th>Days</th><th>Facility</th><th>Status</th><th>Action</th>
                        </tr>
                    </thead> <tbody>`
                    data.forEach((i) => {
                        // console.log(i)
                    html += ` 
                    <tr>
                        <td>${i.record_id}</td><td>${i.name}</td><td>${i.created_on}</td><td>${i.facility_id}</td><td>${i.status}</td>
                        <td><a href="view_record.html?record_id=${i.record_id}"><i class="fa fa-edit"></i> </a></td>
                    </tr> `
                    })
                    html += `</tbody> </table> </div></div> </div>`
                $('#hideafter').hide()
                $('#searchresult').html(html); 
            }
        })
}

function showrecords (response){
        // const records = Object.values(response.records)
        if (response.length === 0){
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
            response.forEach((single) => {
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

form.addEventListener('submit', searchrecord);