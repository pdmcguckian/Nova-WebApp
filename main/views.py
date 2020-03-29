from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import StructuredProject, PersonalProject, StructuredProjectContent
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm, NewProjectForm, StructuredProjectForm, EditProjectForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def dashboard(request):
    if request.method == "POST":
        newpersonalproject(request)
        return redirect('/')
    else:
        form = NewProjectForm()
    return render(request=request,
                template_name="main/dashboard.html",
                context={"structuredprojects": StructuredProject.objects.all(), "personalprojects": PersonalProject.objects.filter(user__username=request.user.username), "form":form},
                )

def register(request):
    if request.user.is_authenticated:
        return redirect('main:dashboard')
    else:
        form = NewUserForm()
        if request.method == "POST":
            form = NewUserForm(request.POST)        
            if form.is_valid():
                user = form.save()
                user
                username=form.cleaned_data.get("username")
                messages.success(request, "Account Created for " + username)
                messages.info(request, "Logged in")
                login(request, user)
                return redirect("main:dashboard")

            else:
                for msg in form.error_messages:
                    messages.error(request, (msg, form.error_messages[msg]))

        
        return render(request,
                    "main/register.html",
                    {"form":form})


def logout_request(request):
    logout(request)

    messages.info(request, "Logged Out")

    return redirect("main:dashboard")


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.info(request, "Logged in")
                return redirect("main:dashboard")
            else:
                messages.error(request, "Invalid Username or Password")

        else:
            messages.error(request, "Invalid Username or Password")

    
    form = AuthenticationForm()

    return render(request,
                "main/login.html",
                {"form":form})

@login_required(login_url='/login/')
def personalproject(request):
    if request.method == "POST":
        if 'project-id' in request.POST:
            project_id = request.POST["project-id"]
            project = PersonalProject.objects.get(id = project_id)
            
            form = EditProjectForm(instance=project)
            return render(request,
                    "main/personalproject.html",
                    {"form":form, "projid":project_id})
        else:
            project_id = request.POST["project-save-id"]
            print(project_id)
            project = PersonalProject.objects.get(id = project_id)
            form = EditProjectForm(request.POST, instance=project)
            if form.is_valid():
                form.save()
                title=form.cleaned_data.get("title")
                messages.success(request, title + " has been saved")

                return redirect("main:dashboard")
    else:
        return redirect("main:dashboard")





@login_required(login_url='/login/')
def newpersonalproject(request):
    form = NewProjectForm(request.POST)
    if form.is_valid:
        form.instance.code = ""
        form.instance.user = request.user
        form.save()
        
    else:
        messages.error(request, "Error")
    return

    """
    if request.method == "POST":
        form = NewProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('main:dashboard')
        else:
            messages.error(request, "Error")
    else:
        form = NewProjectForm()

    return render(request,
                "main/newpersonalproject.html",
                {"form":form})
"""

    return HttpResponse(f"Error")

@login_required(login_url='/login/')
def strucutedproject(request, single_slug):
    projects = [c.slug for c in StructuredProject.objects.all()]

    if request.method == "POST":
        form = StructuredProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return render(request=request,
                template_name="main/structuredproject.html",
                context={"project": StructuredProject.objects.filter(slug=single_slug), "content": StructuredProjectContent.objects.filter(slug=single_slug), "form":form})
        else:
            messages.error(request, "Error")
    else:
        form = StructuredProjectForm()
                
    if single_slug in projects:
      return render(request=request,
                template_name="main/structuredproject.html",
                context={"project": StructuredProject.objects.filter(slug=single_slug), "content": StructuredProjectContent.objects.filter(slug=single_slug), "form":form})


    return HttpResponse(f"Error")