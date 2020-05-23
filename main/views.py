from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import PersonalProject, StructuredProjectContent, StructuredProject, StructuredProjectCode
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm, NewProjectForm, StructuredProjectForm, EditProjectForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('main:login')

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

@login_required(login_url='/login/')
def structuredproject(request, single_slug):
    projects = [c.slug for c in StructuredProject.objects.all()]
    if single_slug in projects:
        project = StructuredProject.objects.get(slug = single_slug)
        project_steps = StructuredProjectContent.objects.filter(slug=single_slug)
        project_user_steps = StructuredProjectCode.objects.filter(user=request.user, project=project)
        user_step = max([c.step for c in project_user_steps] + [0,]) + 1
        displayed_steps = [c for c in project_steps if c.step<= user_step]

        return render(request=request,
                    template_name="main/structuredprojectlist.html",
                    context={"project": project, "content": displayed_steps,})

    else:
        return HttpResponse(f"Error")

@login_required(login_url='/login/')
def structuredproject_edit(request, single_slug):
    project = StructuredProject.objects.get(slug = single_slug)
    project_steps = StructuredProjectContent.objects.filter(slug=single_slug)
    project_user_steps = StructuredProjectCode.objects.filter(user=request.user, project=project)

    if request.method == "POST":
        step_no = int(request.POST['step_no'])
        step_content = project_steps.get(step=step_no)

        if 'save' in request.POST:
            if project_user_steps.filter(step=step_no)[::1] != []:
                print('overwriting saved code')
                prev_instance = project_user_steps.get(step=(step_no))
                form = StructuredProjectForm(request.POST, instance=prev_instance)
            else:
                form = StructuredProjectForm(request.POST)
            
            if form.is_valid():
                form.instance.user = request.user
                form.instance.project = project
                form.instance.step = step_no
                form.save()
                form = StructuredProjectForm(instance = form.instance)

        else:
            if project_user_steps.filter(step=step_no)[::1] != [] and 'reset' not in request.POST:
                print('using saved code')
                step_code = project_user_steps.get(step=(step_no)).code
            elif step_content.default_code == "":
                print('default code empty, using last user code')
                step_code = project_user_steps.get(step=(step_no-1)).code
            else:
                print('using default code')
                step_code = step_content.default_code
            form = StructuredProjectForm(initial={'code' : step_code })

        return render(request=request,
            template_name="main/structuredproject.html",
            context={"project": project, "content": step_content, "form":form})

    return redirect('/'+single_slug)