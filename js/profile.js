const uri = `https://medicarea.herokuapp.com/api/v1/users/${queryString}`;
const uri2 = `https://medicarea.herokuapp.com/api/v1/users/${queryString}/bio`;

// FETCHING USER DATA 
fetchData(uri)
	// .then(checkvalidity(uri))
	// .then(res => res.json())
	.then(dataq => {		
		const data = Object.values(dataq.user)
		$('#idno').html("ID Number:"+' '+data[0].id_number)
		$('#tell').html("Phone:"+' '+data[0].tell)
		$('#address').html("Address:"+' '+data[0].address)
		$('#name').html(data[0].first_name + ' '+ data[0].last_name)
		// console.log(data[0])
	})

fetch(`https://dog.ceo/api/breeds/image/random`)
    .then(response => response.json())
    .then(data => imagehelper(data.message)) 


// FERCHING BIO 
fetchData(uri2 )
	.then(data => {
		const d = data.data[0]
		var today = new Date()
		const _date = new Date(String(d.date_of_birth).replace( /(\d{2})\/(\d{2})\/(\d{4})/, "$2/$1/$3") ); 
		var age = today.getFullYear() - _date.getFullYear()
		$('#age').html("Age:"+' '+ age +' '+ 'Years')
		$('#weight').html("Weight:"+' '+d.weight)
		$('#height').html("Height:"+' '+d.height)
		$('#email').html("Email:"+' '+d.email)
		$('#b_group').html("Blood Group:"+' '+d.blood_group)

	})

// FETCHING Incidents

fetchData(`https://medicarea.herokuapp.com/api/v1/users/incidents`)
	.then(data => {
		if (data.incidents === "No existing incidents assigned to you"){
			emptyrecord(data.incidents)
		}else{
			console.log(data.incidents)
			var dat = data.incidents
			let html = `
				<div class="table-responsive m-t-40">
	                <table id="example23" class="display nowrap table table-hover table-striped table-bordered" cellspacing="0" width="100%">
	                   
	                </table>
                </div>
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
                dat.forEach((single) => {
                html += ` 
                <tr>
                    <td>${single.incident_id}</td>
                    <td>${single.reported_by}</td>
                    <td>${single.tell}</td>
                    <td>${single.location}</td>
                    <td>${single.status}</td>
                    <td>
                        <a href="/view/${single.incident_id}"><i class="fa fa-edit"></i> </a>
                        <a href="/view/${single.incident_id}"><i class="fa fa-snowflake-o"></i> </a>
                    </td>
                </tr> 
                 `
                })
                html += `</tbody> `
                $('#incidents-data').html(html);

		}
	})


function emptyrecord(response) {
	const html = ` <div class="card well">${response}</div>`
	$('#incidents-data').html(html);
}

function imagehelper(data) {
    const htmll = `<img src='${data}' alt>`;
    $('.avatar').html(htmll)
}




