const table  = document.querySelector('tbody');
$( document ).ready(function() {

    const config = {
        method: 'GET',
        headers: {
            "Content-type" : "application/json",
            "Authorization" : `Bearer ${token}`
        }
    }
    
    fetch(`https://medicarea.herokuapp.com/api/v1/users`, config)
        .then((response) => {
            response.json().then(data => {
                const users = Object.values(data.message)
                console.log(users)
                // users.forEach((single) => {
                //     console.log(single.id_number)
                // })
            })
        })
        
    

    // function showusers (data) {
    //     const options  = data.map(item => 
    //         `
    //         <tr>
    //                 <td>${item}</td>
    //                 <td>Customer Support</td>
    //                 <td>New York</td>
    //                 <td>27</td>
    //                 <td>2011/01/25</td>
    //                 <td>$112,000</td>
    //             </tr>  
    //         `
    //         );
    //     // table.innerHTML = options;
    //     console.log(item['id_number']);
    // }

    // function showusers (data) {
    //     for (var i=0; i<data.length; i += 1 ) {
    //         // var user = JSON.parse(data); 
    //         const statusHtml = `
    //             <tr>
    //                 <td>${data.length}</td>
    //                 <td>Customer Support</td>
    //                 <td>New York</td>
    //                 <td>27</td>
    //                 <td>2011/01/25</td>
    //                 <td>$112,000</td>
    //             </tr> 
            
    //         `
    //         table.innerHTML = statusHtml

    //         // if (rooms[i].available === true) {
    //         //     statusHtml += '<li class="empty">';
    //         // }
    //         // else if (rooms[i].available === false) {
    //         //     statusHtml += '<li class="full">';
    //         // }
    //         // statusHtml += rooms[i].room;
    //         // statusHtml += '</li>';
    //     }
    // }

});