from django.contrib import messages
from django.shortcuts import render
import requests
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import FurnitureForm
import requests
from django.shortcuts import render
from django.views import View
from .forms import FurnitureForm


class IndexAdminView(View):
    def get(self, request):
        return render(request, 'index_admin.html')



class ShopAdminView(View):
    def get(self, request):
            access_token = request.COOKIES.get('access_token')
            if not access_token:
                return HttpResponseRedirect('/login/')

            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get("http://127.0.0.1:8032/admin/token/verify", headers=headers)

            if response.status_code <= 300:
                furniture_response = requests.get("http://127.0.0.1:8032/furniture", headers=headers).json()
                if furniture_response:
                    form = FurnitureForm()
                    return render(request, 'shop_admin.html', {'form': form, 'furnitures': furniture_response})
                return redirect("login_admin")
            return redirect("login_admin")

    def post(self, request):
        form = FurnitureForm(request.POST)
        token = request.COOKIES.get('access_token')

        if not token:
            messages.error(request, 'Invalid token')
            return render(request, 'shop_admin.html', {'form': form})

        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            quantity = form.cleaned_data['quantity']
            image = form.cleaned_data['image']
            url = 'http://127.0.0.1:8032/furniture/create'

            data = {
                'name': name,
                'description': description,
                'price': price,
                'quantity': quantity,
                'image': image
            }
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            response = requests.post(url, json=data, headers=headers)

            if response.status_code <= 300:
                return render(request, 'shop_admin.html', {'form': form, "message":"successfully"})
            messages.error(request, 'Invalid credentials')
            return redirect("login_admin")
        return redirect("login_admin")


class FurnitureUpdateView(View):
    def get(self, request, id):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return HttpResponseRedirect('/login/')

        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get("http://127.0.0.1:8032/admin/token/verify", headers=headers)
        if response.status_code <= 300:
            url = f'http://127.0.0.1:8032/furniture/furniture/{id}'
            token = request.COOKIES.get('access_token')
            headers = {'Authorization': f'Bearer {token}'}

            response = requests.get(url, headers=headers)
            if response.status_code <= 300:
                form = FurnitureForm()
                furniture = response.json()
                return render(request, 'shop_admin_update.html', {'form': form, "furniture": furniture})
            return redirect("login_admin")
        return redirect("login_admin")

    def post(self, request, id):
        form = FurnitureForm(request.POST)
        if form.is_valid():
            url = f'http://127.0.0.1:8032/furniture/furniture/{id}'
            token = request.COOKIES.get('access_token')
            headers = {'Authorization': f'Bearer {token}'}

            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                furniture = response.json()
                form = FurnitureForm(initial=furniture)
                print("ddddddddddddddddddddddddddddddd", request.POST.get('name'))
                data = {
                    "name": f"{request.POST.get('name')}",
                    "description": f"{request.POST.get('description')}",
                    "price": request.POST.get('price'),
                    "quantity": request.POST.get('quantity'),
                    "image": f"{request.POST.get('image')}"
                }
                url = f'http://127.0.0.1:8032/furniture/update/{id}'
                response1 = requests.put(url, json=data, headers=headers)
                if response1.status_code <= 300:
                    return render(request, 'shop_admin_update.html', {'form': form, "furniture": furniture, "message":"successfully"})
                return redirect("login_admin")
            else:
                return HttpResponse('Error fetching data from API')
        return render(request, 'shop_admin_update.html', {'form': form, "message":"not fully"})

class FurnitureDeleteView(View):
    def get(self, request, id):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return HttpResponseRedirect('/login/')

        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get("http://127.0.0.1:8032/admin/token/verify", headers=headers)
        if response.status_code <= 300:
            url = f'http://127.0.0.1:8032/furniture/delete/{id}'
            token = request.COOKIES.get('access_token')
            headers = {'Authorization': f'Bearer {token}'}
            response1 = requests.delete(url, headers=headers)
            if response1.status_code <= 300:
                furniture_response = requests.get("http://127.0.0.1:8032/furniture", headers=headers).json()
                if furniture_response:
                    return render(request,'funiture_delete.html', {"furniture": response1, "message":"delete"})
                return redirect("login_admin")
            return redirect("login_admin")

    def post(self, request, id):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return HttpResponseRedirect('/login/')

        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get("http://127.0.0.1:8032/admin/token/verify", headers=headers)
        if response.status_code <= 300:
            url = f'http://127.0.0.1:8032/furniture/delete/{id}'
            token = request.COOKIES.get('access_token')
            headers = {'Authorization': f'Bearer {token}'}
            response1 = requests.delete(url, headers=headers)
            if response1.status_code <= 300:
                furniture_response = requests.get("http://127.0.0.1:8032/furniture", headers=headers).json()
                if furniture_response:
                    return render(request, 'funiture_delete.html', {"furniture": response1, "message": "delete"})
                return redirect("login_admin")
            return redirect("login_admin")

class LoginAdminView(View):
    def get(self, request):
        return render(request, 'auth/login_admin.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        url = "http://127.0.0.1:8032/admin/login/"
        data = {
            "username": username,
            "password": password,
        }

        if username and password:
            response = requests.post(url, json=data)
            if response.json()["status_code"] == 200:
                access_token = response.json()['access_token']

                response = redirect('index_admin')
                response.set_cookie('access_token', access_token, httponly=True)  # Tokenni cookie'da saqlash
                return response
            else:
                messages.error(request, "Invalid login credentials")

        return render(request, 'auth/login_admin.html')


class RegisterAdminView(View):
    def get(self, request):
        return render(request, 'auth/register_admin.html')

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        url = "http://127.0.0.1:8032/admin/register/"
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "email": email,
            "phone": phone,
            "password": password,
        }

        if all([first_name, last_name, username, email, phone, password]):
            response = requests.post(url, json=data)
            try:
                response.raise_for_status()  # Raise an error for bad responses
                detail = response.json().get('detail')

                if detail == "email":
                    messages.error(request, 'Email already exists.')
                elif detail == "username":
                    messages.error(request, 'Username already exists.')
                else:
                    return redirect('login_admin')
                # Render the registration page with the error message
            except requests.exceptions.HTTPError:
                error_message = "username yoki email alloqachon ro`yxatdan o`tgan"
                return render(request, 'auth/register_admin.html', {'message': error_message, 'data': data})
            except (ValueError, KeyError):
                error_message = "Error processing FastAPI response."
                return render(request, 'auth/register_admin.html', {'message': error_message, 'data': data})
        else:
            error_message = 'All fields are required.'
            return render(request, 'auth/register_admin.html', {'message': error_message, 'data': data})
