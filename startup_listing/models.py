from django.db import models
from django.contrib.auth.models import User
# Create your models here.
TYPE = [
    ('OWN', 'Owner'),
    ('DEV', 'Developer')
]

TYPE_OF_FIELD =[
    ('CF','Character Filed'),
    ('TF','Text Field'),
    ('FF', 'File Field'),
    ('IF', 'Integer Field'),
   
]

# class Skill(models.Model):

class Tags(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    about = models.TextField()
    type_of = models.CharField(max_length=3, choices =TYPE, blank=True, null=True)
    image = models.ImageField(upload_to ="dp",default="avatar.png")
    resume = models.FileField(upload_to='resume', blank=True, null = True)
    linkedin_link = models.URLField(blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.BigIntegerField(blank=True, null=True)
    open_to_work = models.BooleanField(default=True)
    work_experience = models.FloatField(default=0)
    dev_type = models.CharField(max_length=20, blank=True, null=True)
    tags = models.ManyToManyField(Tags, blank=True, null=True)

    # applications = models
    def __str__(self):
        return self.user.username



class Community(models.Model):
    name = models.CharField(max_length=50)
    about = models.TextField(default="")
    logo = models.ImageField(upload_to="community_logo", null=True, blank= True)
    def __str__(self):
        return self.name




class StartUp(models.Model):
    name = models.CharField(max_length=200)
    about = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    linkedin_link = models.URLField(null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    owner = models.OneToOneField(Profile, on_delete=models.CASCADE)


    def __str__(self):
        return self.name


class StartUpImage(models.Model):
    start_up = models.ForeignKey(StartUp, on_delete= models.CASCADE)
    image = models.ImageField(upload_to ="startup_images")

    def __str__(self):
        return self.start_up.name
    


class Startup_Project(models.Model):
    name = models.CharField(max_length = 100)
    project_details = models.TextField()
    tags = models.ManyToManyField(Tags, related_name = "project_tags")
    startup = models.ForeignKey(StartUp, on_delete= models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(Profile, related_name="participants", blank=True, null=True)
    approved_participants = models.ManyToManyField(Profile, related_name="approved_participants", blank=True, null=True)
    requirement = models.TextField(default="")
    community = models.ForeignKey(Community, on_delete= models.CASCADE, null= True, blank=True)
    complete = models.BooleanField(default=False)
    # hired_dev = models.ManyToManyField(Profile, related_name="hired_dev", blank=True, null=True)
    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length = 20)
    project = models.ManyToManyField(Startup_Project)
    profile = models.ManyToManyField(Profile)

    def __str__(self):
        return self.name 

class Benefit(models.Model):
    name = models.CharField(max_length=100)
    project = models.ManyToManyField(Startup_Project)

    def __str__(self):
        return self.name 



class Type_Of_Field(models.Model):
    label = models.CharField(max_length=300) 
    type_of = models.CharField(max_length=2, choices=TYPE_OF_FIELD,default='CF')
    project_of = models.ForeignKey(Startup_Project, on_delete=models.CASCADE)
    # filed_of = models.OneToOneField(Form_Field,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.label) + " of " + str(self.project_of.name)


class Form_Field(models.Model):
    
    char_field = models.CharField(max_length=300,blank=True, null=True)
    text_field = models.TextField(blank=True, null=True)
    int_field = models.IntegerField(blank=True, null= True)
    file_field = models.FileField(upload_to='field_file', null=True, blank=True)
    # email_field = models.EmailField()
    # phone_field = models.BigIntegerField()
    field_of = models.ForeignKey(Type_Of_Field,on_delete=models.CASCADE)
    project_of = models.ForeignKey(Startup_Project, on_delete=models.CASCADE)
    participant = models.ForeignKey(Profile, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    def __str__(self):
        return str(self.field_of.label) + " of " + str(self.field_of.project_of.name) + " by " + str(self.participant.user.username)        






# class Custom_Form(models.Model):
#     project = models.ForeignKey(Startup_Project, on_delete= models.CASCADE)
#     participant = models.ForeignKey(Profile, on_delete= models.CASCADE)
#     time = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return self.project.name + " from " + self.participant.user.username
# class File_field(models.Model):
#     form = models.ForeignKey(Custom_Form, on_delete=models.CASCADE)
#     label = models.CharField(max_length=100)
#     file_in = models.FileField(upload_to='FileField')
#     def __str__(self):
#         return self.label + self.form.project.name

# class Char_field(models.Model):
#     form = models.ForeignKey(Custom_Form, on_delete=models.CASCADE)
#     label = models.CharField(max_length=100)
#     character = models.CharField(max_length=300)
#     def __str__(self):
#         return self.label + self.form.project.name
# class Text_field(models.Model):
#     form = models.ForeignKey(Custom_Form, on_delete=models.CASCADE)
#     label = models.CharField(max_length=100)
#     text = models.TextField()
#     def __str__(self):
#         return self.label + self.form.project.name

# class Int_field(models.Model):
#     form = models.ForeignKey(Custom_Form, on_delete=models.CASCADE)
#     label = models.CharField(max_length=100)
#     integer = models.IntegerField()
#     def __str__(self):
#         return self.label + self.form.project.name
# class Email_field(models.Model):
#     form = models.ForeignKey(Custom_Form, on_delete=models.CASCADE)
#     label = models.CharField(max_length=100)
#     email = models.EmailField()
#     def __str__(self):
#         return self.label + self.form.project.name

# class Phone_field(models.Model):
#     form = models.ForeignKey(Custom_Form, on_delete=models.CASCADE)
#     label = models.CharField(max_length=100)
#     phone = models.BigIntegerField()
#     def __str__(self):
#         return self.label + self.form.project.name



