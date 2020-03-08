from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    return render(request, 'prototype/index.html')


@login_required
def order(request):
    return render(request, 'prototype/order.html')


