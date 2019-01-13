from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import datetime
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
now = datetime.datetime.today().strftime("%Y-%m-%d")


def register(request):
    if request.method == 'POST':
        
        form=request.POST
        errors = []
        if len(form['first_name']) < 2:
            errors.append('First name must be at least 2 characters.')
        if len(form['last_name']) < 2:
            errors.append('Last name must be at least 2 characters.')
        if len(form['password']) < 8:
            errors.append('Password must be at least 8 characters.')
        if not form['password'] == form['cpassword']:
            errors.append('Password and password confirmation do not match.')
        if not EMAIL_REGEX.match(form['email']):
            errors.append('Please provide a valid email') 
        if form['birthday']>now:
            errors.append("Your birthday refers to a future date. Please check!!")
        
        if errors:
            for e in errors:
                messages.error(request, e)
        else:        
            try:
                User.objects.get(email=form['email'])
                messages.error(request, 'Your email already exists. Please Login.')
            except User.DoesNotExist:
                hashed_pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())
                c_hashed_pw = hashed_pw.decode('utf-8')
                birthday=str(form['birthday'])
                User.objects.create(first_name=form['first_name'], last_name=form['last_name'], email=form['email'], password=c_hashed_pw, birth=birthday)
                messages.success(request,"You successfully registered. Please login!")
                return redirect('/')
    return render(request, 'its_login_register/register.html')


def login(request):
    if request.method == 'POST':
        
        errors = []
        form=request.POST
        if not EMAIL_REGEX.match(form['emaill']):
            errors.append('Please provide a valid email') 
        else:
            try:
                user=User.objects.get(email=form['emaill'])
                result = bcrypt.checkpw(request.POST['passwordl'].encode(), user.password.encode())
                if result:
                    request.session['user_id'] = user.id
                    return redirect('/dashboard')
                else:
                    messages.error(request, 'Password does not match.')    
            except User.DoesNotExist:
                messages.error(request, 'Your email does not exists. Please register.')
                return redirect('/')
        
        if errors:
            for e in errors:
                messages.error(request, e)   
        return redirect('/')     

def success(request):
    if not 'user_id' in request.session:
        messages.error(request, 'You need to login.')
        return redirect('/')
    
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,     
        'job': Job.objects.all(),
        
    }
    return render(request,'its_login_register/success.html', context)

def add(request):
    if not 'user_id' in request.session:
        messages.error(request, 'You need to login.')
        return redirect('/')
    if request.POST:
        errors=[]
        
        form=request.POST
        if len(form['title'])<3:
            errors.append('Title must be at least 3 characters.')
        if len(form['desc']) < 10:
            errors.append('Description must be at least 10 characters.')
      
        if errors:
            for e in errors:
                messages.error(request, e)
        else:
            Job.objects.create(name=form['title'], desc=form['desc'], location=form['location'],users_id=request.session['user_id'])                   
        
    return render(request, 'its_login_register/newjob.html')

def index(request):
   return render(request, 'its_login_register/index.html')
 
def show(request, job_id):
    if not 'user_id' in request.session:
        messages.error(request, 'You need to login.')
        return redirect('/')
    
    job = Job.objects.get(id=job_id) 
    user=User.objects.get(id=request.session['user_id'])
    context={
        'job':job,
        'user':user,
    }
    request.session['job']=job_id
    return render(request, 'its_login_register/show.html', context)    
 
def edit(request, job_id):
    if not 'user_id' in request.session:
        messages.error(request, 'You need to login.')
        return redirect('/')

    context={   
        'job':Job.objects.get(id=job_id),
    }
    
    if request.POST:

        errors=[]
        form=request.POST
        if len(form['title'])<3:
            errors.append('Title must be at least 3 characters.')
        if len(form['desc']) < 10:
            errors.append('Description must be at least 10 characters.')
        if len(form['location']) < 3:
            errors.append('Location must be at least 3 characters.')


        if errors:
            for e in errors:
                messages.error(request, e)
        else:
            job=Job.objects.get(id=job_id)
            job.name=form['title']
            job.desc=form['desc']
            job.location=form['location']
            job.save()
            return redirect('/dashboard')
    return render(request, 'its_login_register/edit.html', context)

def delete(request, job_id):
    if not 'user_id' in request.session:
        messages.error(request, 'You need to login.')
        return redirect('/')
    job = Job.objects.get(id=job_id) 
    job.delete()
    return redirect('/dashboard')   

def record(request, job_id, user_id):
    if not 'user_id' in request.session:
        messages.error(request, 'You need to login.')
        return redirect('/')
    try: 
        Job.objects.get(id=job_id, job_owner_id=user_id) 
        return redirect('/dashboard') 
    except Job.DoesNotExist:   
        j=Job.objects.get(id=job_id) 
        j.job_owner_id=user_id
        j.save()
        return redirect('/dashboard') 


def logout(request):
    if not 'user_id' in request.session:
        messages.error(request, 'You need to login.')
        return redirect('/')
    request.session.clear()
    return redirect('/')    