import requests
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
# from django.core.mail import send_mail
from .forms import PaymentForm, CargoForm
from django.contrib import messages


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')


class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html')


class CartView(View):
    def get(self, request):
        return render(request, 'cart.html')


class CheckoutView(View):
    def get(self, request):
        return render(request, 'checkout.html')


class ShopView(View):
    def get(self, request):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return HttpResponseRedirect('/login/')

        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get("http://127.0.0.3:8023/client/token/verify", headers=headers)

        if response.status_code == 200:
            furniture_response = requests.get("http://127.0.0.3:8023/furniture", headers=headers).json()
            if furniture_response:
                context = {"furnitures": furniture_response}
                return render(request, 'shop.html', context)
            return render(request, "shop.html", 'furniture not found')

        response = HttpResponseRedirect('/login/')
        response.delete_cookie("access_token")
        return response


class ThankyouView(View):
    def get(self, request):
        return render(request, 'thankyou.html')


class ServiceView(View):
    def get(self, request):
        return render(request, 'services.html')


class BlogView(View):
    def get(self, request):
        return render(request, 'blog.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        url = "http://127.0.0.3:8023/client/login/"
        data = {
            "username": username,
            "password": password,
        }

        if username and password:
            response = requests.post(url, json=data)
            if response.json()["status_code"] == 200:
                access_token = response.json()['access_token']

                response = redirect('index')
                response.set_cookie('access_token', access_token, httponly=True)  # Tokenni cookie'da saqlash
                return response
            else:
                messages.error(request, "Invalid login credentials")

        return render(request, 'auth/login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'auth/register.html')

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        url = "http://127.0.0.3:8023/client/register/"
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "email": email,
            "password": password,
        }

        if all([first_name, last_name, username, email, password]):
            response = requests.post(url, json=data)

            try:
                response.raise_for_status()  # Raise an error for bad responses
                detail = response.json().get('detail')

                if detail == "email":
                    error_message = 'Email already exists.'
                elif detail == "username":
                    error_message = 'Username already exists.'
                else:
                    return redirect('login')

                # Render the registration page with the error message
                return render(request, 'auth/register.html', {'message': error_message, 'data': data})

            except requests.exceptions.HTTPError:
                error_message = "username yoki email alloqachon ro`yxatdan o`tgan"
                return render(request, 'auth/register.html', {'message': error_message, 'data': data})
            except (ValueError, KeyError):
                error_message = "Error processing FastAPI response."
                return render(request, 'auth/register.html', {'message': error_message, 'data': data})
        else:
            error_message = 'All fields are required.'
            return render(request, 'auth/register.html', {'message': error_message, 'data': data})
