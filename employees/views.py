from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from employees.models import Employee
from employees.forms import EmployeeForm
from django.core.paginator import Paginator

PER_PAGE = 100

def get_filtered_and_sorted_employees(request):
    sort_field = request.GET.get('sorted_field', 'full_name')
    current_sort_order = request.GET.get('sort', 'asc')
    page_number = request.GET.get('page', '1')

    sort_field = '-' + sort_field if current_sort_order == 'desc' else sort_field

    search_full_name = request.GET.get('search_full_name', '')
    search_position = request.GET.get('search_position', '')
    search_hire_date = request.GET.get('search_hire_date', '')
    search_email = request.GET.get('search_email', '')
    search_supervisor__full_name = request.GET.get('search_supervisor__full_name', '')

    # Виконуємо пошук співробітників за заданими умовами с использованием Q объекта
    if search_supervisor__full_name:
        employees = Employee.objects.filter(
            Q(full_name__icontains=search_full_name) &
            Q(position__icontains=search_position) &
            Q(hire_date__icontains=search_hire_date) &
            Q(email__icontains=search_email) &
            Q(supervisor__full_name__icontains=search_supervisor__full_name)
        ).order_by(sort_field)
    else:
        employees = Employee.objects.filter(
            Q(full_name__icontains=search_full_name) &
            Q(position__icontains=search_position) &
            Q(hire_date__icontains=search_hire_date) &
            Q(email__icontains=search_email)
        ).order_by(sort_field)


    paginator = Paginator(employees, PER_PAGE)
    page_obj = paginator.get_page(page_number)

    return page_obj

def employee_hierarchy(request):
    employees = Employee.objects.filter(Q(position='CEO') | Q(position='Director')).order_by("position")
    return render(request, 'employees/employee_hierarchy.html', {'employees': employees})

def employee_list(request):
    page_obj = get_filtered_and_sorted_employees(request)
    return render(request, 'employees/employee_list.html', {'employees': page_obj})

def sort_employees(request):
    page_obj = get_filtered_and_sorted_employees(request)
    return render(request, 'employees/search_result.html', {
        'employees': page_obj,
    })

def employee_search(request):
    page_obj = get_filtered_and_sorted_employees(request)
    return render(request, 'employees/search_result.html', {
        'employees': page_obj,
    })

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('employee_list')
        else:
            return render(request, 'employees/login.html', {'error': 'Invalid credentials.'})
    return render(request, 'employees/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def employee_create(request):
    employees = Employee.objects.all()
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form, 'employees': employees})


@login_required
def employee_detail(request, pk):
    employee = Employee.objects.get(pk=pk)
    return render(request, 'employees/employee_detail.html', {'employee': employee})


@login_required
def employee_update(request, pk):
    employees = Employee.objects.all()
    employee = Employee.objects.get(pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/employee_form.html', {'form': form, 'employees': employees})


@login_required
def employee_delete(request, pk):
    employee = Employee.objects.get(pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')
    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})


def load_subordinates(request):
    employee_id = request.GET.get('employee_id')
    try:
        employee = Employee.objects.get(pk=employee_id)
        subordinates = employee.subordinates.all()
        return render(request, 'employees/employee_tree.html', {'employee': employee, 'subordinates': subordinates})
    except Employee.DoesNotExist:
        return JsonResponse({'error': 'Employee not found'}, status=404)

def load_more_employees(request):
    page_obj = get_filtered_and_sorted_employees(request)
    return render(request, 'employees/search_result.html', {'employees': page_obj})
