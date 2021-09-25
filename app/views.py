from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import UserProfile, Input
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages, auth
from django.http import JsonResponse, HttpResponse
import json
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
# Create your views here.


def registration(request):
    if request.method == 'GET':
        return render(request, 'reg.html')

    if request.method == "POST":
        
        password_1 = request.POST['password1']
        password_2 = request.POST['password2']
        phone = request.POST['phone']
        email = request.POST['email']
        if password_1 == password_2:
            try:
                new_user = User(username=phone, email=email, password=make_password((password_2)))
                new_user.save()
                new_profile = UserProfile(user=new_user)
                new_profile.save()
                
                messages.success(request, 'User registration successfully done')
            except Exception as e:
                messages.error(request, 'Failed to register')
        return redirect('login')


# def user_login(request):
#     if request.method == "POST":
#         name = request.POST['name']
#         password = request.POST['password']
#     try:
#         user_obj = User.objects.get(username=name)
#     except Exception as e:
#         messages.error(request, 'Wrong credentials!')
#         return render(request, 'login.html')
#     user = auth.authenticate(username=name, password=password)
#     if user is not None:
#         auth.login(request, user)
#         return redirect('search')
#     return render(request, 'login.html')

def user_login(request):
    if request.method == "POST":
        name = request.POST['name']
        password = request.POST['password']
        user=authenticate(request,username=name,password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect('/')
        else:    
            messages.error(request, 'Usename or Password is incorrect')
    return render(request, 'login.html')





def getlogout(request):
    logout(request)
    return redirect('login')


def binary_search(arr, l, r, x):
    if r >= l:

        mid = l + (r - l) // 2
        if arr[mid] == x:
            return mid

        elif arr[mid] > x:
            return binary_search(arr, l, mid - 1, x)

        else:
            return binary_search(arr, mid + 1, r, x)

    else:
        return -1


@login_required
def search(request):
    if request.method == 'GET':
        content = {
            'result': ''
        }
        return render(request, 'search.html', content)

    if request.method == 'POST':
        data = request.POST
        search_value = data.get('search_value')
        input_values = data.get('input_values')
        input_list = input_values.split(',')
        result = binary_search([int(i) for i in input_list], 0, len(input_list) - 1, int(search_value))
        output = False
        if result < 0:
            print('Failed')
        else:
           output = True

        try:
            input_values = [int(i) for i in input_list]
            input_values.sort(reverse=True)
            input_values = ",".join(str(x) for x in input_values)
            new_input = Input(input_values=input_values, search_value=search_value, output=output)
            new_input.save()
            messages.success(request, 'Data Saved Successfully!')
        except Exception as e:
            messages.error(request, 'Failed to save data!')

        content = {
            'result': output
        }
        return render(request, 'search.html', content)


def get_input_data(request):
    data_list = []
    input_data = Input.objects.all()
    data_dict = {
        'status': 'success',
        'user_id': 1,
        'payload': []
    }
    for data in input_data:
        payload = {
            'time_stamp': str(data.timestamp),
            'input_values': data.input_values
        }
        data_dict['payload'].append(payload)

    data_list.append(data_dict)
    data = json.dumps(data_list)
    return HttpResponse(data, content_type='application/json')