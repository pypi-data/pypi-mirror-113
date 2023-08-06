from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import menus

# Create your views here.

def index(request):
    context = {} 
    myMenu = menus.Menus(request.user.id , 'frontend_unlogin')
    context['menu'] = myMenu.get_menus()
    context['activeMenuList'] = myMenu.find_activeMenuList('child profile2')
    context['breadCrumb'] = myMenu.create_breadCrumb('child profile2')    
    return render(request, 'gmenu/index.html', context) 

# def get_menus(request):
#     myMenu = menus.Menus(request.user.id, 'frontend_unlogin')
#     menu = myMenu.get_menus()
#     return JsonResponse(menu, safe=False)