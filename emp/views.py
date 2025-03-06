from django.shortcuts import render,redirect,get_object_or_404
from .models import CustomUser,Employee
from django.contrib.auth.decorators import login_required
from .forms import EmployeeForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from .forms import RegistrationForm,LoginForm
# Create your views here.
def home(request):
    return render(request, 'home.html', {'title': 'Employee Management System'})

@login_required
def employee_dashboard(request):
    return render(request, 'employee_dashboard.html')
@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

@login_required
def employee_create(request):
    form = EmployeeForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('employee_list')
    return render(request, 'employee_form.html', {'form': form})

@login_required
def employee_update(request, id):
    employee = get_object_or_404(Employee, id=id)
    
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)  # This ensures fields are pre-filled

    return render(request, 'employee_form.html', {'form': form})

@login_required
def employee_delete(request, id):
    employee = get_object_or_404(Employee, id=id)
    employee.delete()
    return redirect('employee_list')

# User Registration
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            # Check if user already exists BEFORE saving
            if CustomUser.objects.filter(Q(username=username) | Q(email=email)).exists():
                return render(request, 'register.html', {'form': form, 'error': 'Username or Email already exists!'})

            # Check if passwords match
            if password != confirm_password:
                return render(request, 'register.html', {'form': form, 'error': 'Password and Confirm Password did not match!'})

            # Save the user
            user = form.save(commit=False)
            user.set_password(password)  # Hash the password
            user.save()

            return redirect('login')  # Redirect to login after successful registration
        else:
            return render(request, 'register.html', {'form': form})
    else:
        return render(request, 'register.html', {'form': RegistrationForm()})


# User Login


def login_view(request):
    print('Login view function called')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = request.POST.get('password') 

            user = authenticate(request, username=username, password=password)
           

            if user:
                login(request, user)
                if user.role == 'admin':
                    return redirect('employee_list')
                elif user.role == 'employee':
                    return redirect('employee_dashboard')
                else:
                    return redirect('login')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password!'})

        else:
            print("Form errors:", form.errors)  # Debugging

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})  # Show login form again

# User Logout
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout