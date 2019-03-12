const uri = `https://medicarea.herokuapp.com/api/v1/incidents/${incident_id}`;
const select = document.getElementById('assign');

fetchData(uri)
	.then(data => presentData(data.incidents[0]))

fetchData(`https://medicarea.herokuapp.com/api/v1/users`)
    .then((response) => genereteOptions(response))


function presentData(response) {
	$('#name').html(response.reported_by)
	$('#phone').html(response.tell)
	$('#date').html(response.created_on)
	$('#location').html(response.location)
	$('#description').html(response.description)
	$('#type').html(response.type)
	$('#status').html(response.status)

	if (response.comment === null){
		$('#comment').html("None")
	}else{
		$('#comment').html(response.comment)
	}
	if (response.assigned_to === null){
		$('#assign').html("None")
	}else{
		$('#assign').html(response.assigned_to)
	}
}

function genereteOptions (object) {
	const data = Object.values(object['users'])
	var html = `<option value=''>Select a user to be ssigned</option>`
	data.forEach((single) => {
		html += `<option value='${single.id_number}'>${single.first_name +' '+ single.last_name}</option>`
	})
    $('#assign_to').html(html)
}


function IncidentUpdate(config_d) {
	return fetch(uri, config_d)
		.then(checkstatus)
        .then(res => res.json())
        .catch(err => dangeralert('Looks there was a problem:', err))
}

function UpdateAssign(val) {
	// e.preventDefault();
	const config_update = {
		method: 'PUT',
		headers: header,
		body: JSON.stringify({"assigned_to": val})
		}
		
	IncidentUpdate(config_update)
		.then(data => successalert(data.message))
}

function UpdateComment(val) {
	// e.preventDefault();
	const config_update = {
		method: 'PUT',
		headers: header,
		body: JSON.stringify({"comment": val})
		}
		
	IncidentUpdate(config_update)
		.then(data => successalert(data.message))
}

function UpdateStatus(val) {
	// e.preventDefault();
	const config_update = {
		method: 'PUT',
		headers: header,
		body: JSON.stringify({"status": val})
		}
		
	IncidentUpdate(config_update)
		.then(data => successalert(data.message))
}

