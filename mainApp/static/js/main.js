function loadPreview(event) {
    var output = document.getElementById('target_image_preview')
    output.src = URL.createObjectURL(event.target.files[0])
    output.onload = () => {
        URL.revokeObjectURL(output.src)
    }
}

function getBase64(file) {
      return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => resolve(reader.result.split(",")[1]);
            reader.onerror = error => reject(error);
      });
}

function closeExistingSocket(socket){
    if (socket) {
            console.log(socket)
            socket.close()
    }
}


$(()=>{

    var socket = null
    let onopen = async (event)=>{
                let file = document.getElementById('uploaded_image').files[0];
                getBase64(file).then(
                  data => {
                      socket.send(JSON.stringify({message: data}))
                  })
    }

    let onmessage = (event)=>{
                    let data = JSON.parse(event.data);
                    document.getElementById('iteration_count').innerText = data.iteration;
                    document.getElementById('generated_image').src = "data:image/png;base64, " + data.message.split("'")[1];
    }

    $('#genetic_algorithm').on('click',()=>{
            closeExistingSocket(socket)
            socket = new WebSocket(`ws://${window.location.host}/ws/genetic_image_consumer/`);
            socket.onopen = onopen
            socket.onmessage = onmessage
    })

    $('#pso_algorithm').on('click',()=>{
        closeExistingSocket(socket)
        socket = new WebSocket(`ws://${window.location.host}/ws/pso_image_consumer/`);
        socket.onopen = onopen
        socket.onmessage = onmessage
    })
    $('#gan_algorithm').on('click',()=>{
        closeExistingSocket(socket)
        socket = new WebSocket(`ws://${window.location.host}/ws/gan_image_consumer/`);
        socket.onmessage = onmessage
    })
    $('#can_algorithm').on('click',()=>{
        closeExistingSocket(socket)
        socket = new WebSocket(`ws://${window.location.host}/ws/can_image_consumer/`);
        socket.onmessage = onmessage
    })

    $('#cancel').on('click',async ()=>{
        closeExistingSocket(socket)
    })

})
