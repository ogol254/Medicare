

const uri = `https://medicarea.herokuapp.com/api/v1/users/${queryString}`



$(document).ready(function() {

	


	fetchData(uri)
		.then(dataq => {
			
			const data = Object.values(dataq)
			console.log(data[0])
			$('#idno').html(data.id_number)
			console.log(data.id_number)
		}) 	

}); 


function fetchData (url) {
    return fetch(url, getconfig)
        // .then(checkstatus)
        .then(res => res.json())
        .catch(err => console.log('Looks there was a proble', err))
	}




// fetchData('https://dog.ceo/api/breeds/image/random')
//     .then(data => imagehelper(data.message))



// ------------------------------------------
//  HELPER FUNCTIONS
// ------------------------------------------
// function checkstatus(response) {
//     if (response.ok) {
//         return Promise.resolve(response);
//     }else{
//         return Promise.reject(new Error(response.statusText));
//     }
// }


