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
                    document.querySelector("#get_material").innerHTML = '<i style="color:red" class="bi bi-x-circle-fill">'
                }
                else {
                    document.querySelector("#get_material").innerHTML = '<i style="color:green" class="bi bi-check-circle-fill">'
                }
                if (data.get_zbytek == false) {
                    document.querySelector("#get_odvoz").innerHTML = '<i style="color:red" class="bi bi-x-circle-fill">'
                }
                else {
                    document.querySelector("#get_odvoz").innerHTML = '<i style="color:green" class="bi bi-check-circle-fill">'
                }
            }
        })
    },300);
});