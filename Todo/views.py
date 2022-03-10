
from django.shortcuts import render,redirect, HttpResponse
from .models import List
from .forms import ListForm
from django.views.generic.base import TemplateView
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from django.contrib import messages


import json

# Create your views here.

class ToDoList(TemplateView):
    template_name = 'list/sample.html'
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['all_item'] = List.objects.filter(user=self.request.user)
        return context


    def post(self,request, *args, **kwargs):
        # context = self.get_context_data(**kwargs)
        form = ListForm(request.POST)
        items = self.request.POST.get("list")
        List.objects.create(user= self.request.user,item = items)
        if form.is_valid():
            form.save()
        return redirect('home')

    def delete(self, request):
        id = request.GET.get('id')
        tasks = List.objects.get(id=id)  
        tasks.delete()
        response_data = {'status': 'success'}
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    def put(self,request):
        id = request.GET.get('id')
        tasks = List.objects.get(id=id)
        tasks.completed = True
        tasks.save()
        response_data = {'status': 'success'}
        return HttpResponse(json.dumps(response_data), content_type="application/json")


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

        return redirect('home')
    return render(request, "list/login.html")


def register(request):
    if request.method == "POST":
        user_name = request.POST["username"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        email = request.POST["email"]
        password = request.POST["password1"]
        password2 = request.POST["password2"]

        if User.objects.filter(username=user_name):
            messages.error(request,"User name is already Exist. Try other names")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request,"Email already exists.")
            return redirect('home')

        if password != password2:
            messages.error(request,"Password Doesn't Match!")

        if not user_name.isalnum():
            messages.error(request,"user name should be in Alfa-Nuemeric!")
            return redirect('home')


        my_user = User.objects.create_user(user_name, email, password)
        my_user.first_name = first_name
        my_user.last_name = last_name 
        my_user.save()

        messages.success(request,"your account has been successfully created.")
        return redirect('home')
    return render(request,"list/register.html")


def user_logout(request):
    logout(request)
    return render(request, "list/sample.html")





# def index(request):
#     form = ListForm()
#     all_items = List.objects.all()
#     context = {'all_items': all_items}
#     if request.method == 'POST':
#         print(all_items)
#         form = ListForm(request.POST )
#         items = request.POST.get("list")
#         List.objects.create(item=items)
#         if form.is_valid():
#             form.save()
#             print("valid")
#             messages.success(request,"Item has been created successfully")
#             return redirect("home",context)
#         else:
#             return redirect("home")

#     else:
#         return render(request,"list/sample.html",context)

# def completed(request, pk):
#     tasks = List.objects.get(id=pk)
#     tasks.completed = True
#     tasks.save()
#     return redirect("home")

# def delete(request, pk):
#     tasks = List.objects.get(id=pk)
#     tasks.delete()
#     return redirect("home")