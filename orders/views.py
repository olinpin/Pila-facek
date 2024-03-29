# import needed modules
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, FileResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .groups import group_required
from .models import Rozmitacka, Hoblovani, Baliky
from reportlab.pdfgen import canvas
import io

### FUNCTIONS IN THIS FILE ### 

# get all the models for the navbar and sort them
# so that it can display 10 latest orders from each
def update_models():
    global rozmitacka_model
    global hoblovani_model
    rozmitacka_model = Rozmitacka.objects.all().filter(do_vyroby=True)
    hoblovani_model = Hoblovani.objects.all().filter(do_vyroby=True)

# Create your views here.

### PAGES ###

# check if user is logged in and if not, redirect to login page
@login_required
def index(request):
    update_models()
    # show the index page and paste the models
    return render(request, "orders/index.html", {
        "rozmitacka": rozmitacka_model,
        "hoblovani": hoblovani_model,
    })

@login_required
@group_required('Rozmitac', 'Admin', 'Vozickar')
def r_info(request, r_id):
    update_models()
    # shows info for a particular rozmitacka order
    info = Rozmitacka.objects.get(id=r_id)
    return render(request, 'orders/r_info.html', {
        "order": info,
        "rozmitacka": rozmitacka_model,
        "hoblovani": hoblovani_model,
        "table": "r",
    })
@login_required
@group_required('Hoblovac', 'Admin', 'Vozickar')
def h_info(request, h_id):
    update_models()
    # shows info for a particular hoblovani order
    info = Hoblovani.objects.get(id=h_id)
    return render(request, 'orders/h_info.html', {
        "order": info,
        "rozmitacka": rozmitacka_model,
        "hoblovani": hoblovani_model,
        "table": "h",
    })

def login_view(request):
    if request.method == "POST":
        # gets the username and password
        username = request.POST["username"]
        password = request.POST["password"]
        #checks if the username and password are correct
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # logs the user in and redirects to the index page
            login(request, user)
            return HttpResponseRedirect(reverse("orders:index"))
        else:
            # invalid credentials error
            return render(request, "orders/login.html", {
                "message": "Špatné přihlašovací údaje",
                "bad": "yes",
            })
    return render(request, "orders/login.html")

def logout_view(request):
    # logs the user out
    logout(request)
    return render(request, "orders/login.html",{
        "message": "You've been logout.",
        "good": "yes",
    })
@login_required
@group_required('Vozickar', 'Admin')
def odvoz(request):
    update_models()
    return render(request, "orders/odvoz.html", {
        "rozmitacka": rozmitacka_model,
        "hoblovani": hoblovani_model,
    })

def permissionNG(request):
    update_models()
    return render(request, "orders/permissionNG.html", {
        "rozmitacka": rozmitacka_model,
        "hoblovani": hoblovani_model,
    })

### FUNCTIONS ###

# this function makes the "done" attribute of order True
def done(request):
    update_models()
    if request.method == "POST":
        # extract the variables
        id = request.POST["id"]
        table = request.POST["table"]
        counter = int(request.POST["counter"])
        # check which table is it
        if table == "r":
            r = Rozmitacka.objects.get(id=id)
        elif table == "h":
            r = Hoblovani.objects.get(id=id)
        else:
            return JsonResponse({"code": 500})
        # change the hotovo value for the order to "True"
        r.hotovo = True
        if counter == 0:
            if r.baliky_celkem == 0:
                Baliky.objects.create(rozmitacka=r, ks=r.ks, done=True)
        r.save()
        # return successful http response
        return JsonResponse({"code": 400})


def countBaliky(request):
    update_models()
    if request.method == "POST":
        # extract the variables
        baliky = request.POST["baliky"]
        id = request.POST["id"]
        table = request.POST["table"]
        done = request.POST["d"]
        # check which tables
        if table == "r":
            r = Rozmitacka.objects.get(id=id)
            balik, _ = Baliky.objects.get_or_create(rozmitacka=r, done=False)
        elif table == "h":
            r = Hoblovani.objects.get(id=id)
            balik, _ = Baliky.objects.get_or_create(hoblovani=r, done=False)
        else:
            return JsonResponse({"code": 500})
        # change the number to the counter variable
        balik.ks = baliky
        if done == 'true':
            balik.done = True
        balik.save()
        return JsonResponse({"code": 400})

# this function changes order's field "get_material" to True if it's called
def needMaterial(request):
    update_models()
    if request.method == "POST":
        # extract the variables
        order_id = request.POST["order_id"]
        table = request.POST["table"]
        # get the right table and change the variable to True
        if table == "r":
            order = Rozmitacka.objects.get(id=order_id)
            order.get_material = True
            order.save()
        elif table == "h":
            order = Hoblovani.objects.get(id=order_id)
            order.get_material = True
            order.save()
        else:
            pass

    return HttpResponse(f"{order_id} from {table} - was succesfull")

def needOdvoz(request):
    update_models()
    if request.method == "POST":
        order_id = request.POST["order_id"]
        table = request.POST["table"]
        if table == "r":
            order = Rozmitacka.objects.get(id=order_id)
            order.get_zbytek = True
            order.save()
        elif table == "h":
            order = Hoblovani.objects.get(id=order_id)
            order.get_zbytek = True
            order.save()
        else:
            pass

    return HttpResponse(f"{order_id} from {table} - was succesfull")

def odpad(request):
    update_models()
    if request.method == "POST":
        order_id = request.POST["order_id"]
        table = request.POST["table"]
        if table == "r":
            order = Rozmitacka.objects.get(id=order_id)
            order.odpad = True
            order.save()
        elif table == "h":
            order = Hoblovani.objects.get(id=order_id)
            order.odpad = True
            order.save()
        else:
            pass

    return HttpResponse(f"{order_id} from {table} - was succesfull")

def getOdvoz(request):
    update_models()
    if request.method == "GET":
        r_odvoz = Rozmitacka.objects.filter(get_zbytek=True).filter(do_vyroby=True)
        r_odvoz_list = [order.id for order in r_odvoz]
        h_odvoz = Hoblovani.objects.filter(get_zbytek=True).filter(do_vyroby=True)
        h_odvoz_list = [order.id for order in h_odvoz]

        r_dovoz = Rozmitacka.objects.filter(get_material=True).filter(do_vyroby=True)
        r_dovoz_list = [order.id for order in r_dovoz]
        h_dovoz = Hoblovani.objects.filter(get_material=True).filter(do_vyroby=True)
        h_dovoz_list = [order.id for order in h_dovoz]

        r_odpad = Rozmitacka.objects.filter(odpad=True).filter(do_vyroby=True)
        r_odpad_list = [order.id for order in r_odpad]
        h_odpad = Hoblovani.objects.filter(odpad=True).filter(do_vyroby=True)
        h_odpad_list = [order.id for order in h_odpad]
        return JsonResponse({"r_odvoz":r_odvoz_list,
                            "h_odvoz":h_odvoz_list, 
                            "r_dovoz": r_dovoz_list, 
                            "h_dovoz": h_dovoz_list,
                            "r_odpad": r_odpad_list,
                            "h_odpad": h_odpad_list,})
    elif request.method == "POST":
        order_id = request.POST["id"]
        table = request.POST["table"]
        DorO = table.split("+")[1]
        table = table.split("+")[0]
        order_id = int(order_id.split("d")[1])
        if DorO == "odvoz":
            if table == "r":
                order = Rozmitacka.objects.get(id=order_id)
                order.get_zbytek = False
                order.save()
            elif table == "h":
                order = Hoblovani.objects.get(id=order_id)
                order.get_zbytek = False
                order.save()
        elif DorO == "dovoz":
            if table == "r":
                order = Rozmitacka.objects.get(id=order_id)
                order.get_material = False
                order.save()
            elif table == "h":
                order = Hoblovani.objects.get(id=order_id)
                order.get_material = False
                order.save()
        elif DorO == "odpad":
            if table == "r":
                order = Rozmitacka.objects.get(id=order_id)
                order.odpad = False
                order.save()
            elif table == "h":
                order = Hoblovani.objects.get(id=order_id)
                order.odpad = False
                order.save()
        return JsonResponse({"code":400})

def check(request):
    if request.method == "POST":
        table = request.POST["table"]
        id = request.POST["id"]
        if table == 'r':
            order = Rozmitacka.objects.get(id=id)
        elif table == 'h':
            order = Hoblovani.objects.get(id=id)
        return JsonResponse({
            "get_material": order.get_material,
            "get_zbytek": order.get_zbytek,
            "odpad": order.odpad,
            })

# PDF export
def pdf_export(request, h_id):
    buffer = io.BytesIO()
    x = canvas.Canvas(buffer)
    x.drawString(100, 100, "Let's generate this pdf file.")
    x.showPage()
    x.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='attempt1.pdf')