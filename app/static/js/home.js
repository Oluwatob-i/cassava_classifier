const form = document.getElementById('form');
const label = document.getElementById('label');
const reader = new FileReader();

form.onsubmit = (e)=> {
    e.preventDefault();
    const input = e.target['upload'];
    const file = (input.files[0])
    label.innerHTML= 'click to upload an image'
    if (file)  {
        sendImage(file)
      
        reader.readAsDataURL(file);
        reader.onloadend = ()=>{
            document.getElementsByTagName('label')[0].style.backgroundImage = `url(${reader.result})`;
           document.getElementsByTagName(`label`)[0].style.backgroundSize = 'cover';
        } 
    }
       
}

function sendImage(image) {
    console.log(window.location)
    fetch('/send_image/',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-CSRFToken':csrftoken,
            },
            body: image
        }
    )
    .then(e=>e.json())
    .catch(e=>'')
    .then(e=> {
        label.innerText = e
    })
    .catch(e=>'')
}