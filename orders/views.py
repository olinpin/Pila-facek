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
from django.contrib.auth.decorators import login_required

rozmitacka_model = Rozmitacka.objects.all().order_by("vytvoreno")
hoblovani_model = Hoblovani.objects.all().order_by("vytvoreno")
info = Rozmitacka.objects.get(id=rozmitacka_model[0].id)

# Create your views here.

# check if user is logged in and if not, redirect to login page
@login_required
def index(request):

    # show the index page
    return render(request, "orders/index.html", {
        "rozmitacka": rozmitacka_model,
        "hoblovani": hoblovani_model,
    })
@login_required
def r_info(request, r_id):
    # shows info for a particular order
    info = Rozmitacka.objects.get(id=r_id)
    return render(request, 'orders/r_info.html', {
        "order": info,
        "rozmitacka": rozmitacka_model,
        "hoblovani": hoblovani_model,
    })
@login_required
def h_info(request, h_id):
    # shows info for a particular order
    info = Hoblovani.objects.get(id=h_id)
    return render(request, 'orders/h_info.html', {
        "order": info,
        "rozmitacka": rozmitacka_model,
        "hoblovani": hoblovani_model,
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

def done(request):
    if request.method == "POST":
        # get the id of the order
        id = request.POST["id"]
        table = request.POST["table"]
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

def count(request):
    if request.method == "POST":
        # get the count
        counter = request.POST["counter"]
        id = request.POST["id"]
        table = request.POST["table"]
        if table == "r":
            r = Rozmitacka.objects.get(id=id)
        elif table == "h":
            r = Hoblovani.objects.get(id=id)
        else:
            return JsonResponse({"code": 500})
        r.ks_hotovo = counter
        r.save()
        return JsonResponse({"code": 400})

def needMaterial(request):
    if request.method == "POST":
        order_id = request.POST["order_id"]
        table = request.POST["table"]
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

def getMaterial(request):
    if request.method == "GET":
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

@login_required
def material(request):
    return render(request, "orders/material.html", {
        "rozmitacka": rozmitacka_model,
        "hoblovani": hoblovani_model,
        "order":info,
    })
    