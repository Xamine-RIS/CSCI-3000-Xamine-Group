from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

@login_required
def index(request):
    return render(request, 'base/coming_soon.html')