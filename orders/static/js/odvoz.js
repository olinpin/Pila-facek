var r_odvoz = [];
var r_dovoz = [];
var r_odpad = [];
var h_odvoz = [];
var h_dovoz = [];
var h_odpad = [];

var attention = false;
var flash = true;
let rozmitacka = document.getElementById("rozmitacka");
let hoblovani = document.getElementById("hoblovani")
var r_dovoz_visible = [];
var h_dovoz_visible = [];
var r_odvoz_visible = [];
var h_odvoz_visible = [];
var r_odpad_visible = [];
var h_odpad_visible = [];
var visible = 0;
var c_visible = 0;
// create event listener, that looks for clicks
document.addEventListener("click", event => {
    const element = event.target;
    // if the clicked element has "hide" class name, we delete its parent element
    if (element.className.includes("hide")) {
        $.ajax({
            type:"POST",
            url: URLgo,
            data:{
                id:element.parentElement.id,
                table:element.parentElement.className,
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function(data){
                // if succesfull, set the background color to grey
                document.body.style.background = "#eee"
            }
        })
        // get the id of the order
        id = parseInt(element.parentElement.id);
        // check if the class is rozmitacka or hoblovani and odvoz or dovoz
        if (element.parentElement.className == "r+odvoz") {
            if (r_odvoz_visible.includes(id)) {
                // delete the id from r_odvoz_visible, remove the order and subtract one from c_visible
                const index = r_odvoz_visible.indexOf(id)
                if (index > -1){
                    r_odvoz_visible.splice(index, 1);
                    element.parentElement.remove();
                    c_visible--
                }
            }
        } if (element.parentElement.className == "h+odvoz") {
            if (h_odvoz_visible.includes(id)) {
                // delete the id from h_odvoz_visible, remove the order and subtract one from c_visible
                const index = h_odvoz_visible.indexOf(id)
                if (index > -1){
                    h_odvoz_visible.splice(index, 1);
                    element.parentElement.remove();
                    c_visible--
                }
            }
        }
        if (element.parentElement.className == "r+dovoz") {
            if (r_dovoz_visible.includes(id)) {
                // delete the id from r_dovoz_visible, remove the order and subtract one from c_visible
                const index = r_dovoz_visible.indexOf(id)
                if (index > -1){
                    r_dovoz_visible.splice(index, 1);
                    element.parentElement.remove();
                    c_visible--
                }
                
            }
        } if (element.parentElement.className == "h+dovoz") {
            if (h_dovoz_visible.includes(id)) {
                // delete the id from h_dovoz_visible, remove the order and subtract one from c_visible
                const index = h_dovoz_visible.indexOf(id)
                if (index > -1){
                    h_dovoz_visible.splice(index, 1);
                    element.parentElement.remove();
                    c_visible--
                }
            }
        }if (element.parentElement.className == "r+odpad") {
            if (r_dovoz_visible.includes(id)) {
                // delete the id from r_odpad_visible, remove the order and subtract one from c_visible
                const index = r_dovoz_visible.indexOf(id)
                if (index > -1){
                    r_odpad_visible.splice(index, 1);
                    element.parentElement.remove();
                    c_visible--
                }
                
            }
        } if (element.parentElement.className == "h+odpad") {
            if (h_dovoz_visible.includes(id)) {
                // delete the id from h_odpad_visible, remove the order and subtract one from c_visible
                const index = h_dovoz_visible.indexOf(id)
                if (index > -1){
                    h_odpad_visible.splice(index, 1);
                    element.parentElement.remove();
                    c_visible--
                }
            }
        }
        
    }
});

$(document).ready(function(){
    // create a reccuring function
    setInterval(function(){
        // get the orders, that need to get rid of material
        $.ajax({
            type:'GET',
            url: URLgo,
            success: function(response){
                // set the variables to the results from the GET method
                r_odvoz = response.r_odvoz
                h_odvoz  = response.h_odvoz
                r_dovoz = response.r_dovoz
                h_dovoz = response.h_dovoz
                r_odpad = response.r_odpad
                h_odpad = response.h_odpad
                visible = r_odvoz.length + h_odvoz.length + r_dovoz.length + h_dovoz.length + r_odpad.length + h_odpad.length
                // check if the visible and c_visible arrays are the same and if the arrays are not empty
                if (visible != c_visible) {
                    if (r_dovoz_visible != [] || h_dovoz_visible != []){
                        attention = true;
                    }
                }
                // if a table has something inside it, flash the screen
                if (r_odvoz.length != 0 || h_odvoz.length != 0 || r_dovoz.length != 0 || h_dovoz.length != 0 || r_odpad.length != 0 || h_odpad.length != 0) {
                    // display the headings appropriate
                    if (r_odvoz.length != 0 || r_dovoz.length != 0 || r_odpad.length != 0) {
                        document.getElementById("rozmitacka_heading").style.display = "block";
                    } else {
                        document.getElementById("rozmitacka_heading").style.display = "none";
                    }
                    if (h_odvoz.length != 0 ||h_dovoz.length != 0 || h_odpad.length != 0) {
                        document.getElementById("hoblovani_heading").style.display = "block";
                    } else {
                        document.getElementById("hoblovani_heading").style.display = "none";
                    }
                    // run loops that add information for each order from both tables
                    // running them in odvoz.html, because they are jinja2 loops
                    
                    rozmitackaL()
                    hoblovaniL()
                    
                    // if attention is true, flash the screen
                    if (attention == true) {
                        if (flash == true) {
                            document.body.style.background = "#FF0000"
                            flash = !flash;
                        }else {
                            document.body.style.background = "#eee"
                            flash = !flash;
                        }
                    }
                } else {
                    // if the arrays are empty, hide the headings
                    document.getElementById("rozmitacka_heading").style.display = "none";
                    document.getElementById("hoblovani_heading").style.display = "none";
                }
            }
        });
    },399);
});
