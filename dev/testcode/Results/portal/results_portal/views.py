from django.shortcuts import render
#from django.shortcuts import send_mail
from .models import Inbox,Choice
# Create your views here.

#get patient name and display
def index(request):
    return render(request, 'results_portal/index.html')