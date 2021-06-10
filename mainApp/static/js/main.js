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
                    let prefix = $.isNumeric(data.iteration) ? "Current iteration:" : ""
                    document.getElementById('iteration_count').innerText = prefix + data.iteration;
                    document.getElementById('generated_image').src = "data:image/png;base64, " + data.message.split("'")[1];
    }

    $('#genetic_algorithm').on('click',()=>{
        hide_all()
        $('#ga_description').show()
        $('#genetic_algorithm_params').show()
        closeExistingSocket(socket)
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

    function checkRange(el,min_val,max_val,type='int'){
        let numeric_value = (type==='int') ? parseInt(el.val()):parseFloat(el.val())
        let check = numeric_value<=max_val && numeric_value>=min_val
        let color = check? '#03fc30' : 'red'
        el.css('background',color)
        return check
    }


     $('#ga_pop_size').on('change',()=>{
            let el = $('#ga_pop_size')
            checkRange(el,50,250)
     })
    $('#ga_shapes_size').on('change',()=>{
            let el = $('#ga_shapes_size')
            checkRange(el,50,500)
    })
    $('#ga_resolution').on('change',()=>{
            let el = $('#ga_resolution')
            checkRange(el,10,50)
    })
    $('#ga_max_iter').on('change',()=>{
            let el = $('#ga_max_iter')
            checkRange(el,100,50000)
    })
    $('#ga_elitism_rate').on('change',()=>{
            let el = $('#ga_elitism_rate')
            checkRange(el,0,1,'float')
    })
    $('#ga_mutation_rate').on('change',()=>{
            let el = $('#ga_mutation_rate')
            checkRange(el,0,1,'float')
    })

    $('#ga_reset_default_params').on('click',()=>{
            $('#ga_max_iter').val(1000).css('background','white')
            $('#ga_pop_size').val(100).css('background','white')
            $('#ga_shapes_size').val(300).css('background','white')
            $('#ga_resolution').val(25).css('background','white')
            $('#ga_elitism_rate').val(0.2).css('background','white')
            $('#ga_mutation_rate').val(0.3).css('background','white')
    })

    $('#ga_algorithm_run').on('click',()=> {
        if ($("#genetic_algorithm_params").is(":visible")) {

            let max_iter_el = $('#ga_max_iter')
            let pop_size_el = $('#ga_pop_size')
            let shapes_size_el = $('#ga_shapes_size')
            let resolution_el = $('#ga_resolution')
            let elitism_rate_el = $('#ga_elitism_rate')
            let mutation_rate_el = $('#ga_mutation_rate')

            let max_iter = max_iter_el.val()
            let pop_size = pop_size_el.val()
            let shapes_size = shapes_size_el.val()
            let resolution = resolution_el.val()
            let elitism_rate = elitism_rate_el.val()
            let mutation_rate = mutation_rate_el.val()

            if (checkRange(elitism_rate_el,0,1,'float') && checkRange(mutation_rate_el,0,1,'float')
                && checkRange(max_iter_el,100,50000) && checkRange(pop_size_el,50,250)
                && checkRange(shapes_size_el,50,500) && checkRange(resolution_el,10,50)
            ){
                $('#ga_error_msg').hide()
            }else{
                $('#ga_error_msg').show()
                return
            }

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



    $('#pso_imitation_factor').on('change',()=>{
        let el = $('#pso_imitation_factor')
        checkRange(el,0,1,'float')
    })
    $('#pso_width').on('change',()=>{
        let el = $('#pso_width')
        checkRange(el,64,300)
    })
    $('#pso_height').on('change',()=>{
        let el = $('#pso_height')
        checkRange(el,64,300)
    })

    $('#pso_reset_default_params').on('click',()=>{
            $('#pso_imitation_factor').val(0.8).css('background','white')
            $('#pso_width').val(128).css('background','white')
            $('#pso_height').val(128).css('background','white')
    })
    $('#pso_algorithm_run').on('click',()=> {
        if ($("#pso_algorithm_params").is(":visible")) {
            let imitating_factor_el = $('#pso_imitation_factor')
            let width_el = $('#pso_width')
            let height_el = $('#pso_height')
            let imitating_factor = imitating_factor_el.val()
            let width = width_el.val()
            let height = height_el.val()

            if (checkRange(imitating_factor_el,0,1,'float')
                && checkRange(width_el,64,300) && checkRange(height_el,64,300)){
                $('#pso_error_msg').hide()
            }else{
                $('#pso_error_msg').show()
                return
            }

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
