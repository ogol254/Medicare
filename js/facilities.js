const table  = document.querySelector('table');
const form  = document.querySelector('form');
const showalert = document.getElementById('alertarea');

fetchData(`https://medicarea.herokuapp.com/api/v1/facilities`)
        .then(res => {
            // const data = res.
            console.log(res)
        })



function PostFacility(e){
    e.preventDefault();
    
    const name = document.getElementById('val-fname').value;
    const tell = document.getElementById('val-phoneus').value;
    const location = document.getElementById('val-address').value;

    const configpost = {
        method: 'POST',
        headers: header,
        body: JSON.stringify({
            "name": name,
            "location": location,
            "contact": tell
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


