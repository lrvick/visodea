from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from projects.models import Project, ProjectMember, ProjectFavorite
from projects.forms import AddProjectForm, AddUserForm, ProjectEditForm, AddFileForm, ProjectMemberForm
from uploads.models import Attachment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms.formsets import formset_factory
from django.db import IntegrityError

def index(request):
    projects = Project.objects.order_by('-date_created')
    return render_to_response('index.html', {
        'projects': projects,
    }, context_instance=RequestContext(request))

@login_required
def user_projects(request, username):
    return render_to_response('user_projects.html', {}, context_instance=RequestContext(request))

@login_required
def add(request):
    user = request.user
    if request.POST:
        form = AddProjectForm(request.POST)
        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.owner = user
            new_project.save()
            return HttpResponseRedirect(reverse('project-detail', args=[new_project.slug]))
    else:
        form = AddProjectForm()
    return render_to_response('add.html', {
        'form': form,    
    }, context_instance=RequestContext(request))

@login_required
def edit(request, slug):
    user = request.user
    project = get_object_or_404(Project, slug=slug)
    members = project.projectmember_set.all()
    if user in [member.user for member in members]:
        member = members.get(user=user)
        level = member.level
    if request.POST:
        form = ProjectEditForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('project-detail', args=[project.slug]))
    else:
        form = ProjectEditForm(instance=project)
    return render_to_response('edit_project.html', locals(), context_instance=RequestContext(request))

@login_required
def delete(request, slug):
    user = request.user
    project = get_object_or_404(Project, slug=slug)
    if request.POST:
        if project.owner == user:
            #do the delete stuff here
            pass
    else:
        pass
    return render_to_response('delete.html', {}, context_instance=RequestContext(request))

def detail(request, slug):
    user = request.user
    project = get_object_or_404(Project, slug=slug)
    attachments = project.attachment_set.all()
    members = project.projectmember_set.all() 
    if user in [member.user for member in members]:
        member = members.get(user=user)
        level = member.level
    return render_to_response('detail.html', locals(), context_instance=RequestContext(request))

@login_required
def adduser(request, slug):
    project = get_object_or_404(Project, slug=slug)
    owner = project.owner
    members = project.projectmember_set.all()
    user = request.user
    if user in [member.user for member in members]: #this thing here
        member = members.get(user=user)
        level = member.level
    
    if request.POST:
        form = AddUserForm(request.POST)
        if form.is_valid():
            #create new ProjectMember object bound to User (by email)
            #and to project (by current project)
            cd = form.cleaned_data
            email, level = cd['email'], cd['level']
            user = User.objects.get(email=email)
            new_member = ProjectMember(
                project = project,
                user = user,
                level = level,
            )
            new_member.save()
            #redirect to project detailed page
            return HttpResponseRedirect(reverse('project-detail', args=[project.slug]))
    else:
        form = AddUserForm()
    return render_to_response('adduser.html', locals(), context_instance=RequestContext(request))

@login_required
def addfile(request, slug):
    user = request.user
    project = get_object_or_404(Project, slug=slug)
    members = project.projectmember_set.all()
    attachments = project.attachment_set.all()
    if user in [member.user for member in members]:
        member = members.get(user=user)
        level = member.level
    if request.POST:
        form = AddFileForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            name, file = cd['name'], cd['file']
            
            new_file = Attachment(
                project = project,
                name = name, 
                file = file,
            )
            new_file.save()
            return HttpResponseRedirect(reverse('project-detail', args=[project.slug]))
    else:
        form = AddFileForm()
    return render_to_response('addfile.html', locals(), context_instance=RequestContext(request))

def search(request):
    errors = [] 
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Please enter a search term.')
        else:
            qset = (
                Q(name__icontains=q) |
                Q(description__icontains=q)
            )
            projects = Project.objects.filter(qset).distinct() #unique results
            return render_to_response('search_results.html', {
                'query': q,
                'projects': projects,
            }, context_instance=RequestContext(request))

    return render_to_response('search.html', {
        'errors': errors,
    }, context_instance=RequestContext(request))

@login_required
def manageusers(request, slug):
    project = get_object_or_404(Project, slug=slug)
    members = project.projectmember_set.all()

    ProjectMemberFormSet = formset_factory(ProjectMemberForm, can_delete=True, max_num=members.count())

    if request.POST:
        formset = ProjectMemberFormSet(request.POST)
        if formset.is_valid():
            #save formset data into models 
            cd = formset.cleaned_data
            for data in cd:
                member = members.get(user=User.objects.get(username=data['user']))
                if data['DELETE'] == True and request.user == project.owner: 
                    member.delete() #may want to actually do a two step process or use javascript so deletes aren't so raw
                else:
                    member.level = data['level']
                    member.save()
            return HttpResponseRedirect(reverse('project-manageusers', args=[project.slug]))
    else:
        formset = ProjectMemberFormSet(initial=[
            {'user': member.user, 'project': project, 'level': member.level} for member in members
        ])
    project = get_object_or_404(Project, slug=slug)
    return render_to_response('manageusers.html', {
        'project': project,
        'formset': formset,
    }, context_instance=RequestContext(request))

@login_required
def addfavorite(request, slug):
    project = Project.objects.get(slug=slug)
    try:
        new_favorite = ProjectFavorite(
            project = get_object_or_404(Project, slug=slug),
            user = request.user,
        )
        new_favorite.save()
        messages.add_message(request, messages.INFO, 'Project was added to your favorites')
        return HttpResponseRedirect(reverse('project-detail', args=[project.slug]))
    except IntegrityError:
        messages.add_message(request, messages.ERROR, 'This project is already in your favorites. Considering we removed the button, we are curious to know how you are even seeing this message...')
        return HttpResponseRedirect(reverse('project-detail', args=[project.slug]))


