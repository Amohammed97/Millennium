from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse, request
from main.models import Accounts, MainAccounts
from django.views.decorators.cache import cache_control
# Create your views here.
valid = False


@cache_control(no_cache=True, must_revalidate=True)
def index(request):
    users = {
        'Accounts': Accounts.objects.all()
    }
    #data = MainAccounts.objects.create( name = 'ahmed' , role = 'admin' ,  password = '1234' )
    #data = MainAccounts.objects.all().delete()
    #data = MainAccounts.objects.all()
    # print(len(data))
    return render(request, 'main/index.html', users)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_user(request):
    if request.method == "POST":
        username = request.POST['Uname']
        role = request.POST['role']
        password = request.POST['password']
        Accounts.objects.create(name=username, role=role, password=password)
        return redirect(Users)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_user(request):
    try:
        if request.method == "POST":
            id = request.POST['Selrow']
            Accounts.objects.get(id=id).delete()
            return redirect(Users)
    except KeyError:
        return redirect(Users)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_user(request):
    if request.method == "POST":
        username = request.POST['Nname']
        id = request.POST['Selrow']
        role = request.POST['Nrole']
        password = request.POST['Npassword']

        selected = Accounts.objects.get(id=id)
        selected.name = username
        selected.role = role
        selected.password = password
        selected.save()
        return redirect(Users)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def validate(request):
    global valid
    valid = False
    users = {
        'Accounts': Accounts.objects.all(),
        'message': 'Incorrect User , try again'
    }

    if request.method == "POST":
        username = request.POST['Uname']
        role = request.POST['role']
        password = request.POST['password']

    all_accounts = Accounts.objects.all()
    for i in all_accounts:
        if i.name == username and i.role == role and i.password == password:
            valid = True

    if valid == True:
        return redirect(Users)
    else:
        return render(request, 'main/index.html', users)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ticket(request):

    if valid == True:
        return render(request, 'main/ticket.html')
        # return render(request,'main/ticket.html')
    else:
        return redirect(index)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    global valid
    valid = False
    return redirect(index)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Users(request):
    users = {
        'users': Accounts.objects.all()
    }
    if valid == True:
        return render(request, 'main/users.html', users)
    else:
        return redirect(index)


x = 0


def weight(request):
    global x
    while 1:
        x = x+1
        print(x)
        return JsonResponse(x, safe=False)
