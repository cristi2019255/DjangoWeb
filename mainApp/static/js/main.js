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

    function hide_all() {
        $('#genetic_algorithm_params').hide()
        $('#pso_algorithm_params').hide()
        $('#ga_description').hide()
        $('#pso_description').hide()
        $('#gan_description').hide()
        $('#can_description').hide()
    }

    hide_all()
    var socket = null

    let onmessage = (event)=>{
                    let data = JSON.parse(event.data);
                    document.getElementById('iteration_count').innerText = data.iteration;
                    document.getElementById('generated_image').src = "data:image/png;base64, " + data.message.split("'")[1];
    }

    $('#genetic_algorithm').on('click',()=>{
        hide_all()
        $('#ga_description').show()
        $('#genetic_algorithm_params').show()
    })

    $('#pso_algorithm').on('click',()=>{
        hide_all()
        $('#pso_description').show()
        $('#pso_algorithm_params').show()
        closeExistingSocket(socket)
    })
    $('#gan_algorithm').on('click',()=>{
        hide_all()
        $('#gan_description').show()
        closeExistingSocket(socket)
        socket = new WebSocket(`ws://${window.location.host}/ws/gan_image_consumer/`);
        socket.onmessage = onmessage
    })
    $('#can_algorithm').on('click',()=>{
        hide_all()
        $('#can_description').show()
        closeExistingSocket(socket)
        socket = new WebSocket(`ws://${window.location.host}/ws/can_image_consumer/`);
        socket.onmessage = onmessage
    })

    $('#cancel').on('click',async ()=>{
        closeExistingSocket(socket)
        hide_all()
    })

    $('#ga_algorithm_run').on('click',()=> {
        if ($("#genetic_algorithm_params").is(":visible")) {
            let max_iter = $('#ga_max_iter').val()
            let pop_size = $('#ga_pop_size').val()
            let shapes_size = $('#ga_shapes_size').val()
            let resolution = $('#ga_resolution').val()
            let elitism_rate = $('#ga_elitism_rate').val()
            let mutation_rate = $('#ga_mutation_rate').val()

            closeExistingSocket(socket)
            socket = new WebSocket(`ws://${window.location.host}/ws/genetic_image_consumer/`);
            socket.onmessage = onmessage
            socket.onopen = async (event) => {
                let file = document.getElementById('uploaded_image').files[0];
                let data = await getBase64(file)
                let object = JSON.stringify(
                    {message: data,
                           max_iter : max_iter,
                           shape:'line',
                           pop_size: pop_size,
                           shapes_size : shapes_size,
                           resolution : resolution,
                           elitism_rate : elitism_rate,
                           mutation_rate: mutation_rate
                    })
                socket.send(object)
            }
        }
    })

    $('#pso_algorithm_run').on('click',()=> {
        if ($("#pso_algorithm_params").is(":visible")) {
            let imitating_factor = $('#pso_imitation_factor').val()
            let width = $('#pso_width').val()
            let height = $('#pso_height').val()
            closeExistingSocket(socket)
            socket = new WebSocket(`ws://${window.location.host}/ws/pso_image_consumer/`);
            socket.onmessage = onmessage
            socket.onopen = async (event) => {
                let file = document.getElementById('uploaded_image').files[0];
                let data = await getBase64(file)
                let object = JSON.stringify(
                    {message: data,
                           imitating_factor : imitating_factor,
                           width : width,
                           height: height,
                    })
                socket.send(object)
            }
        }
    })
})
