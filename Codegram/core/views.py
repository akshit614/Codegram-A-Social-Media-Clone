import email
from email.mime import image
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from .models import ProFil
from django.contrib.auth.decorators import login_required
from core.models import ProFil  , Poost



# Create your views here.


@login_required(login_url='signup')
def index(request):
    
    user_object = User.objects.get(username = request.user.username)
    check = ProFil.objects.filter(user = user_object)
    print(check , len(check))
    if len(check) > 0 :
        user_profile = ProFil.objects.get(user = user_object)
        return render(request, 'index.html', {'user_profile' : user_profile})
    return render(request, 'index.html')
  
@login_required(login_url='signin')
def upload(request):
    
    if request.method == 'POST':
        user = request.user.username
        image_upload = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Poost.objects.create(user=user, image_upload=image_upload , caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                 messages.info(request, 'Username already taken')
                 return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password= password)
                user.save()

                #log user in and redirect to page

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = ProFil.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('index')
        else:
            messages.info(request, 'Password should be same ')
            return redirect('signup')
        
    else:
        return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Wrong Details')
            return redirect('signin')

    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def settings(request):
    user_profile = ProFil.objects.get(user = request.user)

    if request.method == 'POST' :

        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        return redirect('settings')


    return render(request, 'setting.html', {'user_profile': user_profile})


@login_required(login_url='signin')


def logout(request):

    auth.logout(request)
    return redirect('signin')


