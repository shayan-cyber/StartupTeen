from django.shortcuts import render, get_object_or_404, Http404, redirect, HttpResponse
from . models import *
from django.contrib import messages
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
# Create your views here.
def home(request):
    communities = Community.objects.all()
    past_projects = Startup_Project.objects.filter(complete=True)
    context ={
        'communities':communities,
        'past_projects':past_projects,
    }

    return render(request, 'index.html', context)
def communities(request):
    if request.method == 'POST':
        community_text = request.POST.get('community', '')
        search_results = Community.objects.filter(name__icontains = community_text)
        context ={
            'search_results':search_results,
        }
        return render(request, 'communities.html', context)
    else:

        communities = Community.objects.all()
        context ={
            'communities':communities
        }

        return render(request, 'communities.html', context)

def community(request, id):
    community = get_object_or_404(Community, id = id)
    projects = Startup_Project.objects.filter(community = community, complete=False)
    past_projects = Startup_Project.objects.filter(community = community, complete=True)
    
    # images = StartUpImage.objects.filter(start)
    context = {
        'community':community,
        'projects':projects,
        'past_projects':past_projects,

    }
    return render(request, 'community.html', context)
@login_required(login_url='/login_page')
def project(request, id):
    project = get_object_or_404(Startup_Project, id =id)
    # event = Event.objects.filter(unique_id =unique_id)[0]
    type_of_fields = Type_Of_Field.objects.filter(project_of =project)
    prof = request.user.profile
    print(type_of_fields)

    
    
    if request.method == "POST":
        if project.complete == False:
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
        else:
            raise Http404()
    
        
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


@login_required(login_url='/login_page')
def profile(request, username):
    if request.user.profile.type_of =="DEV":

        user_obj = get_object_or_404(User, username =username)
        profile = get_object_or_404(Profile, user = user_obj)
        completed_projects = Startup_Project.objects.filter(approved_participants= profile, complete = True).order_by('-time')
        skills = Skill.objects.all()
        prof_skills = profile.skill_set.all()
        remaining_skills = skills.difference(prof_skills)
        applications = Startup_Project.objects.filter(approved_participants= profile)
        # form_field = Form_Field.objects.filter(project_of= )
        sub_data ={}
        for i in applications:
            sub_data[i] = Form_Field.objects.filter(project_of= i, participant = profile)[0]
        print(applications)
        print(sub_data)
        context ={
            'profile':profile,
            'skills':skills,
            'remaining_skills':remaining_skills,
            'prof_skills':prof_skills,
            'applications': applications,
            'sub_data':sub_data,
            'completed_projects':completed_projects,
        }
        return render(request, "profile.html", context)
    elif request.user.profile.type_of =="OWN":
        user_obj = get_object_or_404(User, username =username)
        profile = get_object_or_404(Profile, user = user_obj)
        startup = StartUp.objects.filter(owner=profile)
        context ={
            'profile':profile,
            'startup':startup

        }
        return render(request, "profile_owner.html", context)



@login_required(login_url='/login_page')
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
                # prof.phone = phone
                prof.work_experience = work_experience

            elif not dp and resume:
                prof = get_object_or_404(Profile, user = user_obj)
                prof.about = about
                # prof.image = dp
                prof.resume = resume
                prof.linkedin_link = linkedin_link
                prof.github_link = github_link
                prof.email = email
                # prof.phone = phone
                prof.work_experience = work_experience
            elif not resume and dp:
                prof = get_object_or_404(Profile, user = user_obj)
                prof.about = about
                prof.image = dp
                # prof.resume = resume
                prof.linkedin_link = linkedin_link
                prof.github_link = github_link
                prof.email = email
                # prof.phone = phone
                prof.work_experience = work_experience
            elif not resume and not dp:
                prof = get_object_or_404(Profile, user = user_obj)
                prof.about = about
                # prof.image = dp
                # prof.resume = resume
                prof.linkedin_link = linkedin_link
                prof.github_link = github_link
                prof.email = email
                # prof.phone = phone
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

            if phone != 'None':
                prof.phone = phone
            prof.save()
            sk.save()

            return redirect('/profile/' + str(username))
        elif user_obj.profile.type_of =="OWN":
            dp = request.FILES.get('dp')
            github_link = request.POST.get("github_link", "")
            linkedin_link = request.POST.get("linkedin_link", "")
            email = request.POST.get("email", "")
            phone = request.POST.get("phone", "")
            about = request.POST.get("about", "")
            prof = get_object_or_404(Profile, user = user_obj)
            prof.linkedin_link = linkedin_link
            prof.github_link = github_link
            prof.email = email
            # prof.phone = phone
            prof.about = about
            if dp:
                
                prof.image = dp
            if phone != 'None':
                prof.phone = phone
                
            prof.save()
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



    
@login_required(login_url='/login_page')
def add_project(request):
    if request.user.profile.startup:
        startup = request.user.profile.startup
        communities = Community.objects.all()
        tags_objs = Tags.objects.all()
        skill_objs = Skill.objects.all()
        benefit_objs = Benefit.objects.all()
        if request.method == "POST":
            name = request.POST.get("name", '')
            project_details = request.POST.get("project_details",'')
            tags = request.POST.getlist('tags', [])
            skills = request.POST.getlist('skills', [])
            benefits = request.POST.getlist('benefits', [])
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
            for i in benefits:
                benefits_obj = get_object_or_404(Benefit, id=i)
                benefits_obj.project.add(project_obj)
            
            messages.success(request, "Project Added Successfully")


            
        else:
            pass
        context = {'startup':startup, 'communities':communities, 'tags':tags_objs,'skills':skill_objs,'benefits':benefit_objs}
        return render(request, "add_project.html", context)
    else:
        pass
    #404 no startup


@login_required(login_url='/login_page')
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
@login_required(login_url='/login_page')
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
            else:
                skills_objs.append(skill)
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
@login_required(login_url='/login_page')
def add_benefits(request):
    if request.user.profile.startup:
        startup= request.user.profile.startup
        benefits = Benefit.objects.all()
        temp = []
        benefits_objs =[]
        if request.method == 'POST':
            benefit = request.POST.get('benefit','')
            benefit = str(benefit)
            if ',' in benefit:

                benefits_objs = benefit.split(",")
            else:
                benefits_objs.append(benefit) 
            print(benefits_objs)

            objs = []
            for i in benefits:
                objs.append(i.name)
            
            for i in benefits_objs:
                if i in objs:
                    print("already exists")
                    temp.append(get_object_or_404(Benefit, name=i))
                else:
                    benefitobj = Benefit(name=i)
                    benefitobj.save()
            benefits = Benefit.objects.all()
        return render(request, "add_benefits.html", {"benefits":benefits, 'startup':startup, 'temp':temp})
    else:
        pass
@login_required(login_url='/login_page')
def add_tags(request):
    if request.user.profile.startup:
        temp =[]
        tags_objs =[]
        startup= request.user.profile.startup
        tags = Tags.objects.all()
        print(request.method)
        if request.method == 'POST':
            tag = request.POST.get('tag','')
            tag = str(tag)
            print(tag)
            if ',' in tag:
                tags_objs = tag.split(',')
            elif ' ' in tag:
                tags_objs = tag.split(' ')
            else:
                tags_objs.append(tag)
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


@login_required(login_url='/login_page')
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

@login_required(login_url='/login_page')
def delete_field(request,pk):

    type_of_field = Type_Of_Field.objects.filter(pk=pk)[0]
    unq_id = type_of_field.project_of.id
    if type_of_field.project_of.startup.owner.user == request.user:
        type_of_field.delete()



        return redirect("/add_form_field/" + str(unq_id))
    else:
        raise Http404()


@login_required(login_url='/login_page')
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
                    if request.user == project_obj.startup.owner.user:
                        project_obj.approved_participants.add(profile_obj)
                    else:
                        raise Http404()



        return JsonResponse({'message':'hello'})


def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # request.user.profile.type_of = da
        if len(data.get('approves_value')) ==1:
            request.user.profile.type_of = data['approves_value'][0]
        elif len(data.get('approves_value')) ==2:
            request.user.profile.type_of = data['approves_value'][1]
        request.user.profile.save()
        print(data)
        return JsonResponse({'message':'hello'})

    return render(request,'registration.html')


def sign_up(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data['name']
        email = data['email']
        username = data['username']
        password = data['password']
        confirm_password = data['confirm_password']
        usercheck = User.objects.filter(username =username)

        if len(username)>20:
            # messages.warning(request,"User name is too long")
            msg = "username is too long"
        elif usercheck:
            # messages.warning(request, "User name already exists")
            msg = "username already exists"
            print("exists")
        elif password != confirm_password:
            # messages.warning(request, "Passwords Do not Match")
            msg = "password does not match"
        else:
            user_ = User.objects.create_user(
                first_name =name,
                password=password,
                username =username,
                email = email
            )
            user_.save()
            user_obj = authenticate( username= username, password = password)
            
            login(request,user_obj)
            msg ="logged in"
        print(data)
        # return redirect('/register/')
        return JsonResponse({'message':msg})


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user_obj = authenticate( username= username, password = password)
        login(request,user_obj)

        return redirect('/register')

    return render(request, 'login_page.html')

@login_required(login_url='/login_page')
def add_startup(request):
    if request.user.profile.type_of == "OWN":
        if request.method == 'POST':
            name= request.POST.get('name','')
            about = request.POST.get('about','')
            linkedin_link = request.POST.get('linkedin_link','')
            email = request.POST.get('email','')
            logo = request.FILES.get('logo','')
            owner = request.user.profile
            startup_obj = StartUp(
                name=name,
                about=about,
                linkedin_link=linkedin_link,
                email=email,
                
                owner=owner,
            )
            startup_obj.save()
            startup_logo = StartUpImage(
                start_up = startup_obj,
                image = logo
            )
            startup_logo.save()
            
            return redirect('/startup_dashboard')
        return render(request, 'startup_add.html')

    else:
        # you dont have an owner account
        raise Http404()
@login_required(login_url='/login_page')
def startup_dashboard(request):
    # startup = get_object_or_404(StartUp, owner = request.user.profile)
    startup = StartUp.objects.filter(owner=request.user.profile)
    if startup:
        startup = request.user.profile.startup
        projects = Startup_Project.objects.filter(startup=startup)
        context = {
            'projects':projects,
            'startup':startup
        }
        return render(request, 'startup_dashboard.html',context)
    else:
        #dont have startup
        return redirect('/add_startup')
    

@login_required(login_url='/login_page')
def edit_startup(request, pk):
    startup = get_object_or_404(StartUp, pk =pk)
    startup_logos = StartUpImage.objects.filter(start_up = startup)[0]
    if startup.owner.user == request.user:
        if request.method == 'POST':
            name = request.POST.get('name','')
            about = request.POST.get('about','')
            linkedin_link = request.POST.get('linkedin_url','')
            logo = request.FILES.get('logo', '')
            email = request.POST.get('email','')
            if logo:
                logo = logo
            else:
                logo = startup_logos.image
            startup.name = name
            startup.about = about
            startup.linkedin_link = linkedin_link
            startup.email = email
            print(logo)
            print(startup_logos.image)
            startup_logos.image = logo

            startup_logos.save()
            print(startup_logos.image)
            startup.save()

            return redirect('/startup_dashboard')
    else:
        raise Http404()

@login_required(login_url='/login_page')
def edit_project(request, pk):
    project = get_object_or_404(Startup_Project,pk=pk)
    if project.startup.owner.user == request.user:
        if request.method == 'POST':
            name = request.POST.get('name','')
            details = request.POST.get('project_details','')
            requirements = request.POST.get('requirements','')
            project.name = name
            project.project_details = details
            project.requirement = requirements
            project.save()

            return redirect('/project_details_startup/' + str(pk))
        else:
            raise Http404()

@login_required(login_url='/login_page')
def delete_project(request,pk):
    project = get_object_or_404(Startup_Project,pk=pk)
    if project.startup.owner.user == request.user:
        project.delete()

        return redirect('/startup_dashboard')


    else:
        raise Http404()
@login_required(login_url='/login_page')
def completed_project(request,pk):
    project = get_object_or_404(Startup_Project,pk=pk)
    if project.startup.owner.user == request.user:
        project.complete = True
        project.save()

        return redirect('/project_details_startup/' + str(pk))


    else:
        raise Http404()

def tag_link(request, pk):
    projects = Startup_Project.objects.filter(tags = get_object_or_404(Tags, pk =pk), complete=False)
    past_projects = Startup_Project.objects.filter(tags = get_object_or_404(Tags, pk =pk), complete=True)
    context ={
        'projects':projects,
        'past_projects':past_projects,
        'tag':get_object_or_404(Tags, pk=pk)
    }
    return render(request, 'tag_link.html', context)

@login_required(login_url='/login_page')
def explore_section(request):
    skills = Skill.objects.filter(profile = request.user.profile)
    print(skills)
    project_list =[]
    past_project_list = []
    for skill in skills:
        for proj in skill.project.all():
            # if proj in project_list and proj in past_project_list:
            #     print("already in")
            #     continue
            if proj not in past_project_list and proj not in project_list:
                if proj.complete ==False :
                    project_list.append(proj)
                elif proj.complete ==True :
                    past_project_list.append(proj)
            
        

    # projects = Startup_Project.objects.filter()
    print(past_project_list)
    print(project_list)
    context = {'projects':project_list, 'past_projects':past_project_list}
    return render(request, 'explore_section.html', context)



def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        msg_subject = request.POST.get('msg_subject','')
        message = request.POST.get('msg', '')
        email_context = {
            "name":name,
            "msg_subject":msg_subject,
            "message":message,
            "email":email
        }
        template_email = render_to_string('email/email_template.html', email_context)

        email_obj = EmailMessage(

            name + " has sent an email",
            template_email,
            settings.EMAIL_HOST_USER,
            ['debroyshayan@gmail.com', 'contact@thestartupteens.com']
            
        )
        email_obj.fail_silently = False
        email_obj.send()
        print(email_obj)
        messages.success(request, "We have received your mail")

        return redirect('/')

    else:
        raise Http404()


def log_out(request):
    logout(request)
    return redirect("/")