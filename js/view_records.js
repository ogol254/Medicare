const uri = `https://medicarea.herokuapp.com/api/v1/records/${record_id}`;
const commenturi = `https://medicarea.herokuapp.com/api/v1/records/${record_id}/comment/`;
const form  = document.querySelector('form');


fetchData(uri)
	.then(data => {
        presentData( data['records'][0])
        showcoment(data['comments'])
    })

function presentData(response) {
    $('#name').html(response.name)
    $('#record_id').html(response.record_id)
	$('#xk').html(response.record_id)
	$('#date').html(response.created_on)
	$('#location').html(response.location)
	$('#description').html(response.description)
    $('#type').html(response.type)
    $('#assign').html(response.created_by)
	$('#status').html(response.status)
}

function imagehelper(data) {
    const htmll = `<img src="${data}" alt="user" width="40" height="40" class="img-circle" /> `;
    $('.sl-left').html(htmll)
}

function showcoment(response){
    if (typeof(response) === "string" && response === "No comments exists"){
        var html = `<div class="card well well-sm">No Comments</div>`
        $('#.profiletimeline').html(html)
    }else{
        // console.log(response[0])
        var html = ``
        response.forEach((res) => {
            fetch(`https://dog.ceo/api/breeds/image/random`)
                .then(response => response.json())
                .then(data => imagehelper(data.message))
            
            html += `
            <div class="sl-item">
                <div class="sl-left"> </div>
                <div class="sl-right">
                    <div><a href="#" class="link">${res.created_by}</a> <span class="sl-date">${res.created_on}</span>
                        <p class="m-t-10">${res.comment}</p>
                    </div>
                </div>
            </div>
            <hr>
            `
        })
        $('.profiletimeline').html(html)
    }
}

function PostComment(e) {
    e.preventDefault();
    
    var comment = document.getElementById('comment');
	var config_post = {
		method: 'POST',
		headers: header,
		body: JSON.stringify({
			"comment" : comment.value
		   })
        }
        
		
    fetch(commenturi, config_post)
		.then(checkstatus)
        .then(res => res.json())
        .then(data => {
            $('.profiletimeline').fadeOut(800, function(){
                fetchData(uri)
                    .then(data => {
                        presentData( data['records'][0])
                        showcoment(data['comments'])
                    }) 
            
            });
            $('.profiletimeline').fadeIn().delay(2000);
            form.reset();
            successalert(data.message);
        })
        .catch(err => dangeralert('Looks there was a problem', err))		
}

form.addEventListener('submit', PostComment);