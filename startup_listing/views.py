from django.shortcuts import render, get_object_or_404, Http404, redirect
from . models import *
from django.contrib import messages
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
# Create your views here.
def home(request):
    communities = Community.objects.all()
    context ={
        'communities':communities
    }

    return render(request, 'home.html', context)

def community(request, id):
    community = get_object_or_404(Community, id = id)
    projects = Startup_Project.objects.filter(community = community)
    # images = StartUpImage.objects.filter(start)
    context = {
        'community':community,
        'projects':projects,

    }
    return render(request, 'community.html', context)

def project(request, id):
    project = get_object_or_404(Startup_Project, id =id)
    # event = Event.objects.filter(unique_id =unique_id)[0]
    type_of_fields = Type_Of_Field.objects.filter(project_of =project)
    prof = request.user.profile
    print(type_of_fields)

    
    
    if request.method == "POST":
        for i in type_of_fields:
            project.participants.add(request.user.profile)
            if i.type_of == "CF":
                char_in = request.POST.get('char_in','')
                form_field = Form_Field(char_field =char_in, field_of = i, participant = prof, project_of = project)
                form_field.save()
                print("char_in saved")

            elif i.type_of == "TF":
                text_in = request.POST.get('text_in', '')
                form_field = Form_Field(text_field =text_in, field_of = i, participant = prof, project_of = project)
                form_field.save()
                print("text_in saved")
            elif i.type_of =="FF":
                img_in = request.FILES['img_in']
                form_field = Form_Field(file_field =img_in, field_of = i, participant = prof, project_of = project)
                form_field.save()
                print("img_in saved")
            elif i.type_of == "IF":
                integer_in = request.POST.get('int_in', '')
                form_field = Form_Field(int_field =integer_in, field_of = i, participant = prof, project_of = project)
                form_field.save()
                print("int_in saved")
    
        
    if prof in get_object_or_404(Startup_Project, id =id).participants.all():
        context ={
            'project':project,
            'registered':prof,
        }
    else:
        context ={
            'project':project,
            'set_fields':type_of_fields
        }

    return render(request, 'project.html', context)

def profile(request, username):
    user_obj = get_object_or_404(User, username =username)
    profile = get_object_or_404(Profile, user = user_obj)
    skills = Skill.objects.all()
    prof_skills = profile.skill_set.all()
    remaining_skills = skills.difference(prof_skills)
    context ={
        'profile':profile,
        'skills':skills,
        'remaining_skills':remaining_skills,
        'prof_skills':prof_skills
    }
    return render(request, "profile.html", context)




def profile_edit(request, username):
    if request.method == "POST":
        user_obj = get_object_or_404(User, username =username)
        if user_obj.profile.type_of =="DEV":
            open_to_work = request.POST.get('open_to_work', '')
            skills = request.POST.getlist('skills')
            dp = request.FILES.get('dp')
            resume = request.FILES.get('resume')
            github_link = request.POST.get("github_link", "")
            linkedin_link = request.POST.get("linkedin_link", "")
            email = request.POST.get("email", "")
            phone = request.POST.get("phone", "")
            work_experience = request.POST.get("work_experience", "")
            about = request.POST.get("about", "")
            if resume and dp:
                prof = get_object_or_404(Profile, user = user_obj)
                prof.about = about
                prof.image = dp
                prof.resume = resume
                prof.linkedin_link = linkedin_link
                prof.github_link = github_link
                prof.email = email
                prof.phone = phone
                prof.work_experience = work_experience

            elif not dp and resume:
                prof = get_object_or_404(Profile, user = user_obj)
                prof.about = about
                # prof.image = dp
                prof.resume = resume
                prof.linkedin_link = linkedin_link
                prof.github_link = github_link
                prof.email = email
                prof.phone = phone
                prof.work_experience = work_experience
            elif not resume and dp:
                prof = get_object_or_404(Profile, user = user_obj)
                prof.about = about
                prof.image = dp
                # prof.resume = resume
                prof.linkedin_link = linkedin_link
                prof.github_link = github_link
                prof.email = email
                prof.phone = phone
                prof.work_experience = work_experience
            elif not resume and not dp:
                prof = get_object_or_404(Profile, user = user_obj)
                prof.about = about
                # prof.image = dp
                # prof.resume = resume
                prof.linkedin_link = linkedin_link
                prof.github_link = github_link
                prof.email = email
                prof.phone = phone
                prof.work_experience = work_experience
            prof.skill_set.clear()
            for i in skills:
                sk = get_object_or_404(Skill, id = i)
                

                sk.profile.add(prof)
            if open_to_work =="on":
                prof.open_to_work = True
            else:
                prof.open_to_work = False
            print(open_to_work)
            prof.save()
            sk.save()

            return redirect('/profile/' + str(username))
            









        else:
            pass
        
    else:
        raise Http404()




def startup_listing(request):
    return render(request, 'startup_listing.html')

def startup_home(request, id):
    start_up = get_object_or_404(StartUp, id=id)
    latest_projects = Startup_Project.objects.filter(startup=start_up, complete = False).order_by("-time")
    past_projects = Startup_Project.objects.filter(startup=start_up, complete = True).order_by("-time")
    context ={
        'startup':start_up,
        'past_projects':past_projects,
        'latest_projects':latest_projects
    }

    return render(request, "startup_home.html", context)



    

def add_project(request):
    if request.user.profile.startup:
        startup = request.user.profile.startup
        communities = Community.objects.all()
        tags_objs = Tags.objects.all()
        skill_objs = Skill.objects.all()
        if request.method == "POST":
            name = request.POST.get("name", '')
            project_details = request.POST.get("project_details",'')
            tags = request.POST.getlist('tags', [])
            skills = request.POST.getlist('skills', [])
            print(tags)
            requirement = request.POST.get("requirement",'')
            community = request.POST.get("community", "")

           

            project_obj = Startup_Project(
                name=name,
                project_details=project_details,
                startup = startup,
                requirement = requirement,
                community = get_object_or_404(Community, id =community),

            )
            project_obj.save()
            for i in tags:
                project_obj.tags.add(get_object_or_404(Tags, id =i))
            project_obj.save()
            for i in skills:
                skill_obj = get_object_or_404(Skill, id=i)
                skill_obj.project.add(project_obj)
            
            messages.success(request, "Project Added Successfully")


            
        else:
            pass
        context = {'startup':startup, 'communities':communities, 'tags':tags_objs,'skills':skill_objs}
        return render(request, "add_project.html", context)
    else:
        pass
    #404 no startup



def project_details_startup(request, pk):
    project = get_object_or_404(Startup_Project,pk=pk)
    if project.startup.owner.user == request.user:
        
        startup = request.user.profile.startup
        form_fields = Type_Of_Field.objects.filter(project_of = project)

        #rendering applications

        field_submissions = Form_Field.objects.filter(project_of = project).order_by('-time')
        types_of_fields = Type_Of_Field.objects.filter(project_of =project)
        paticipants_list =[]
        for i in field_submissions:
            if i.participant in paticipants_list:
                print("alrteady In")
            else:
                paticipants_list.append(i.participant)
        print(paticipants_list)
        sub_data ={

        }
        for i in paticipants_list:
            sub_data[(i.user)] =[]
            for j in Form_Field.objects.filter(participant = i, project_of = project):
                sub_data[(i.user)].append(j)
        print(sub_data)
        #end
        
        context={
            'field_submissions':field_submissions,
            'types_of_fields':types_of_fields,
            'project':project,
            'startup':startup,
            'set_fields': form_fields,
            'sub_data':sub_data
        }
        return render(request, "project_details_startup.html",context)
    else:
        pass

def add_skills(request):
    if request.user.profile.startup:
        startup= request.user.profile.startup
        skills = Skill.objects.all()
        temp = []
        skills_objs =[]
        if request.method == 'POST':
            skill = request.POST.get('skill','')
            skill = str(skill)
            if ',' in skill:

                skills_objs = skill.split(",")
            elif ' ' in skill:
                skills_objs =skill.split(" ")
            print(skills_objs)

            objs = []
            for i in skills:
                objs.append(i.name)
            
            for i in skills_objs:
                if i in objs:
                    print("already exists")
                    temp.append(get_object_or_404(Skill, name=i))
                else:
                    skillobj = Skill(name=i)
                    skillobj.save()
            skills = Skill.objects.all()
        return render(request, "add_skills.html", {"skills":skills, 'startup':startup, 'temp':temp})
    else:
        pass

def add_tags(request):
    if request.user.profile.startup:
        temp =[]
        tags_objs =[]
        startup= request.user.profile.startup
        tags = Tags.objects.all()
        if request.method == 'POST':
            tag = request.POST.get('tag','')
            tag = str(tag)
            if ',' in tag:
                tags_objs = tag.split(',')
            elif ' ' in tag:
                tags_objs = tag.split(' ')
            print(tags_objs)
            objs =[]

            for i in tags:
                objs.append(i.name)
            for i in tags_objs:
                if i in objs:
                    temp.append(get_object_or_404(Tags, name=i))
                else:
                    tagobj = Tags(name =i)
                    tagobj.save()
            tags = Tags.objects.all()

        return render(request, "add_tags.html", {"tags":tags, 'startup':startup, 'temp':temp})
    else:
        pass

def add_form_field(request, id):
    
    # event = Event.objects.filter(unique_id=unique_id)[0]
    project = get_object_or_404(Startup_Project, id=id)
    set_fields = Type_Of_Field.objects.filter(project_of = project)
    

    if project.startup.owner.user == request.user:
        startup= request.user.profile.startup
        if request.method == "POST":
            label = request.POST.get('label','')
            type_of_field = request.POST.get('type_of_field','')
            type_field = Type_Of_Field(label =label, type_of =type_of_field, project_of = project)
            type_field.save()
        print(set_fields)

        context ={
            'project':project,
            'set_fields':set_fields,
            'startup':startup
        }
        return render(request, "add_form_field.html",context)
    else:
        raise Http404()


def delete_field(request,pk):

    type_of_field = Type_Of_Field.objects.filter(pk=pk)[0]
    unq_id = type_of_field.project_of.id
    if type_of_field.project_of.startup.owner.user == request.user:
        type_of_field.delete()



        return redirect("/add_form_field/" + str(unq_id))
    else:
        raise Http404()

def approval(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print("starts")
        print(data['approves_value'])
        if len(data['approves_value']) >= 1:

            for i in data['approves_value']:
                print(i)
                user_obj = get_object_or_404(User,username=i)
                profile_obj = get_object_or_404(Profile, user = user_obj)
                project_obj = get_object_or_404(Startup_Project,pk = data['project'])
                print(project_obj)
                print(profile_obj)
                if profile_obj in project_obj.approved_participants.all():
                    print("already in")
                else:
                    project_obj.approved_participants.add(profile_obj)



        return JsonResponse({'message':'hello'})


def registration(request):
    return render(request,'registration.html')