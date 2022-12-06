// when document is ready, start reccuring function
// that updates Dovoz a Odvoz
$(document).ready(function() {
    setInterval(function() {
        $.ajax({
            type:'POST',
            url: URLch,
            data: {
                table:table,
                id:id,
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function(data){
                if (data.get_material == false){
                    document.querySelector("#get_material").innerHTML = '<i style="color:red" class="bi bi-x-circle-fill">';
                    document.getElementById("material").style.backgroundColor = "#0d6efd";
                }
                else {
                    document.querySelector("#get_material").innerHTML = '<i style="color:green" class="bi bi-check-circle-fill">';
                    document.getElementById("material").style.backgroundColor = "#06377e";
                }
                if (data.get_zbytek == false) {
                    document.querySelector("#get_odvoz").innerHTML = '<i style="color:red" class="bi bi-x-circle-fill">';
                    document.getElementById("odvoz").style.backgroundColor = "#6c757d";
                }
                else {
                    document.querySelector("#get_odvoz").innerHTML = '<i style="color:green" class="bi bi-check-circle-fill">';
                    document.getElementById("odvoz").style.backgroundColor = "#202325";
                }
                if (data.odpad == false) {
                    document.querySelector("#get_odpad").innerHTML = '<i style="color:red" class="bi bi-x-circle-fill">';
                    document.getElementById("odpad").style.backgroundColor = "#0d6efd";
                }
                else {
                    document.querySelector("#get_odpad").innerHTML = '<i style="color:green" class="bi bi-check-circle-fill">';
                    document.getElementById("odpad").style.backgroundColor = "#06377e";
                }
            }
        })
    },1000);
});