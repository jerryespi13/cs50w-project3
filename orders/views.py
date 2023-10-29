from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "orders/index.html")

def register(request):
    return render(request, "orders/register.html")

def login(request):
    return render(request, "orders/login.html")
