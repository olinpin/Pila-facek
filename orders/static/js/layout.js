function increase(by) {
    // increment the counter on the screen 
    counter += by
    last_balik += by
    document.querySelector("#c_done").innerHTML = counter;
    document.querySelector("#last_balik").innerHTML = last_balik;
    count()
    count_baliky(false)
}

function decrease(by) {
    // decrement the counter on the screen
    counter -= by
    last_balik -= by
    document.querySelector("#c_done").innerHTML = counter;
    document.querySelector("#last_balik").innerHTML = last_balik;
    count()
    count_baliky(false)
}

function count() {
    // Give the current counter value to the server
    
    $.ajax({
        type: 'POST',
        url: URLc,
        data:{
        id:id,
        table:table,
        counter: counter,
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function(data){
        // alert(data)
        }
    })
}

function count_baliky(d) {
    // Give the current counter value to the server
    $.ajax({
        type: 'POST',
        url: URLcb,
        data:{
        id:id,
        table:table,
        baliky: last_balik,
        d: d,
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function(data){
        // alert(data)
        }
    })

}

function done() {
    // give the id of the order to the server
    
    $.ajax({
        type: 'POST',
        url: URLd,
        data:{
        id:id,
        table:table,
        counter:counter,
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function(data){
        }
    })
    // change the number of ks and change the hotovo to green checkmark
    document.querySelector("#hotovo").innerHTML = '<i style="color:green" class="bi bi-check-circle-fill">'
    if (document.querySelector("#c_done").innerHTML == 0){
        document.querySelector("#c_done").innerHTML = ks;
        counter = ks;
    }
}

// these functions are used for changing the material and odvoz fields in the table
function material() {
    $.ajax({
        type: 'POST',
        url: URLnm,
        data:{
        order_id:id,
        table:table,
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function(data){
            // if succesfull, change the red cross to a green checkmark
            document.querySelector("#get_material").innerHTML = '<i style="color:green" class="bi bi-check-circle-fill">'
        }
    })
}

function odvoz() {
$.ajax({
    type: 'POST',
    url: URLno,
    data:{
    order_id:id,
    table:table,
    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
    },
    success: function(data){
        // if succesfull, change the red cross to a green checkmark
        document.querySelector("#get_odvoz").innerHTML = '<i style="color:green" class="bi bi-check-circle-fill">'
    }
})
}

function odpad() {
    $.ajax({
        type: 'POST',
        url: URLo,
        data:{
        order_id:id,
        table:table,
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function(data){
            // if succesfull, change the red cross to a green checkmark
            document.querySelector("#get_odpad").innerHTML = '<i style="color:green" class="bi bi-check-circle-fill">'
        }
    })
}

function balik() {
    count_baliky(true)
    last_balik = 0
    document.querySelector("#last_balik").innerHTML = last_balik;
    baliky_celkem += 1
    document.querySelector("#baliky_celkem").innerHTML = baliky_celkem;
}
