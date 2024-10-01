from django.shortcuts import render, redirect, get_object_or_404
from .models import Pet
from .forms import PetForm, UserRegisterForm, CustomLoginForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    try:
        pets = Pet.objects.all()
        user = request.user
    except Exception as e:
        print(e)
    return render(request, "index.html", {'pets_list': pets, "user":user}  )
    

@login_required
def add_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index_page')
    else:
        form = PetForm()
    return render(request, 'add_pet.html', {'form':form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('index_page') 
    
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back {username}")
                return redirect('index_page') 
            else:
                messages.error(request, 'Invalid Username or Password')
        else:
           messages.error(request, 'Please correct the errors in the form.') 

    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    return render(request, 'pet_detail.html', {'pet':pet})