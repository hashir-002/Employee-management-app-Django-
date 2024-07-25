from django.shortcuts import render, HttpResponse, redirect
from .models import *
from datetime import datetime
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'index.html')

def all_emp(request):
    emps =Employee.objects.all()
    context = {'emps': emps}

    return render(request, 'all.html', context)


def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        dept = int(request.POST['dept'])
        role = int(request.POST['role'])
        new_emp = Employee(first_name=first_name, last_name= last_name, salary=salary, bonus=bonus, phone=phone, dept_id = dept, role_id = role, hire_date = datetime.now())
        new_emp.save()
        return redirect('/all-emp')
    elif request.method == 'GET':
        return render(request, 'add.html')
    else:
        return HttpResponse('An unknown error has occured')
        

    # return render(request, 'add.html')

def remove_emp(request, emp_id=0):
    if emp_id:
        try:
            emps_to_be_removed = Employee.objects.get(id = emp_id)
            emps_to_be_removed.delete()
            return redirect('/all-emp')
        except:
            return HttpResponse('Please enter a valid id')
    
    emps = Employee.objects.all()
    context = {'emps': emps}
    return render(request, 'remove.html', context)

def filter_emp(request):
    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        emps = Employee.objects.all()
        if name:
            emps = emps.filter(Q(first_name__icontains= name) | Q(last_name__icontains = name))
        if dept:
            emps = emps.filter(dept__name__icontains = dept)
        if role:
            emps = emps.filter(role__name__icontains = role)
        
        context = {'emps': emps}

        return render(request, 'all.html', context)
    elif request.method == 'GET':
        return render(request, 'filter.html')
    else:
        return HttpResponse('Unexpexted error occured')