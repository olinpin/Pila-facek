# import needed modules
from django.contrib import auth
from django.forms.forms import Form
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
import datetime
from .models import Rozmitacka, Hoblovani
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from .groups import group_required

### FUNCTIONS IN THIS FILE ###

# get all the models for the navbar and sort them
# so that it can display 10 latest orders from each
def update_models():
    global rozmitacka_model
    global hoblovani_model
    rozmitacka_model = Rozmitacka.objects.all().filter(do_vyroby=True).order_by("vytvoreno")
    hoblovani_model = Hoblovani.objects.all().filter(do_vyroby=True).order_by("vytvoreno")

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
@group_required('Rozmitacka', 'Admin')
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
@group_required('Hoblovani', 'Admin')
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
                "message": "Invalid credentials",
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
@group_required('Material', 'Admin')
def material(request):
    update_models()
    return render(request, "orders/material.html", {
        "rozmitacka": rozmitacka_model,
        "hoblovani": hoblovani_model,
    })
    
@login_required
@group_required('Odvoz', 'Admin')
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
        # check which table is it
        if table == "r":
            r = Rozmitacka.objects.get(id=id)
        elif table == "h":
            r = Hoblovani.objects.get(id=id)
        else:
            return JsonResponse({"code": 500})
        # change the hotovo value for the order to "True"
        r.hotovo = True
        r.ks_hotovo = r.ks
        r.save()
        # return successful http response
        return JsonResponse({"code": 400})

# this function makes the "ks_hotovo" attribute of order to the right amount of ks
def count(request):
    update_models()
    if request.method == "POST":
        # extract the variables
        counter = request.POST["counter"]
        id = request.POST["id"]
        table = request.POST["table"]
        # check which tables
        if table == "r":
            r = Rozmitacka.objects.get(id=id)
        elif table == "h":
            r = Hoblovani.objects.get(id=id)
        else:
            return JsonResponse({"code": 500})
        # change the number to the counter variable
        r.ks_hotovo = counter
        r.save()
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

# this function gets back what orders currently need material
def getMaterial(request):
    update_models()
    if request.method == "GET":
        # get the orders that have "get_material" field True
        r = Rozmitacka.objects.filter(get_material=True)
        r_list = [order.id for order in r]
        h = Hoblovani.objects.filter(get_material=True)
        h_list = [order.id for order in h]
        return JsonResponse({"r":r_list, "h":h_list})
    elif request.method == "POST":
        order_id = request.POST["id"]
        table = request.POST["table"]
        if table == "r":
            order = Rozmitacka.objects.get(id=order_id)
            order.get_material = False
            order.save()
        elif table == "h":
            order = Hoblovani.objects.get(id=order_id)
            order.get_material = False
            order.save()
        else:
            pass
        return JsonResponse({"code":400})

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

def getOdvoz(request):
    update_models()
    if request.method == "GET":
        r = Rozmitacka.objects.filter(get_zbytek=True)
        r_list = [order.id for order in r]
        h = Hoblovani.objects.filter(get_zbytek=True)
        h_list = [order.id for order in h]
        return JsonResponse({"r":r_list, "h":h_list})
    elif request.method == "POST":
        order_id = request.POST["id"]
        table = request.POST["table"]
        if table == "r":
            order = Rozmitacka.objects.get(id=order_id)
            order.get_zbytek = False
            order.save()
        elif table == "h":
            order = Hoblovani.objects.get(id=order_id)
            order.get_zbytek = False
            order.save()
        else:
            pass
        return JsonResponse({"code":400})