const form = document.getElementById('form');
const label = document.getElementById('label');
const reader = new FileReader();
const logo2 = document.getElementById('logo2');
const loader  = document.getElementById('loader');
const diagnoseButton  = document.getElementById('diagnoseButton')

var interval;

form.onsubmit = (e)=> {
    e.preventDefault();
    const input = e.target['upload'];
    const file = (input.files[0]);
    label.innerHTML= '';
    let count = 0;
  
    if (file && 'image/jpeg, image/jpg, image/png, image/PNG, image/JPG, image/JPEG'.includes(file.type)) {
        logo2.style.display = 'none';
        loader.style.display = 'block';
        
        let counter = 1;
        diagnoseButton.innerText = 'diagnosing';
        interval = setInterval(() => {
            counter === 3?
            (counter = 1)
            :
            ++counter
            let dots = '';

            Array(counter).fill(1).forEach(e=> dots += '.')
            diagnoseButton.innerText = `diagnosing${dots}`
        }, 300);
        sendImage(file)
        
        reader.readAsDataURL(file);
        reader.onloadend = ()=>{
            document.getElementById('logo2').src= reader.result;
            //document.getElementsByTagName('label')[0].style.backgroundImage = `url(${reader.result})`;
           //document.getElementsByTagName(`label`)[0].style.backgroundSize = 'cover';
        } 
    } else {
        label.innerText = 'upload an image'
       
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
        label.innerText = e || 'upload a better image';
        logo2.style.display = 'block';
        loader.style.display = 'none';
        clearInterval(interval)
        diagnoseButton.innerText = 'diagnose';
    })
    .catch(e=>'')
}