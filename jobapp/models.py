from inspect import CO_VARARGS
from string import capwords
from unicodedata import name

from django.db import models

# Create your models here.
class login(models.Model):
    logid = models.AutoField(primary_key=True)
    username = models.CharField("username",max_length=100)
    password =  models.CharField("password",max_length=100)
    role=models.CharField('role',max_length=10)

class company(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField("name",max_length=100)
    company_address =  models.CharField("address",max_length=500)
    company_email = models.CharField("email",max_length=100)
    company_phone = models.CharField("phone_no",max_length=100)
    company_poc = models.CharField("poc_no",max_length=100)
    company_location = models.CharField("location",max_length=100)
    company_pocmail = models.CharField("pocmail",max_length=100)
    comapany_pocdis = models.CharField("posdis",max_length=100)
    company_pocphone = models.CharField("pocphone",max_length=100)
    company_logo = models.FileField("logo:",max_length=100,upload_to="images/")
    company_regno = models.CharField("regno",max_length=100)
    company_foundedyear   = models.CharField("fyear",max_length=100)
    status =  models.CharField("status",max_length=100)
    logid = models.ForeignKey(login, on_delete=models.CASCADE, null=True)

class candidate(models.Model):
    candidate_id = models.AutoField(primary_key=True)
    candidate_name = models.CharField("name",max_length=100)
    candidate_address = models.CharField("address",max_length=500)
    candidate_email = models.CharField("email",max_length=100)
    candidate_phone =  models.CharField("phone_no",max_length=100)
    candidate_photo = models.FileField("photo:",max_length=100,upload_to="images/")
    candidate_lastqualification = models.CharField("lastqua",max_length=100)
    candidate_experienced = models.CharField("exp",max_length=100)
    candidate_mark = models.CharField("candidate_mark",max_length=100)
    candidate_totalexperienced=models.FileField("candidate_totalexperienced",max_length=100,upload_to="resumes/")
    status =  models.CharField("status",max_length=100)
    logid = models.ForeignKey(login, on_delete=models.CASCADE, null=True)

class job(models.Model):
    job_id = models.AutoField(primary_key=True)
    company_id = models.ForeignKey(company, on_delete=models.CASCADE, null=True)
    job_title = models.CharField("title",max_length=100)
    job_role = models.CharField("role",max_length=100)
    job_description=models.CharField("desc",max_length=500)
    job_designation =models.CharField("desig",max_length=100)
    job_qualificaion = models.CharField("qualification",max_length=500)
    job_experience = models.CharField("experience",max_length=100)
    job_experiencein =  models.CharField("experiencein",max_length=500)
    job_salary = models.CharField("salary",max_length=100)
    job_location = models.CharField("location",max_length=100)
    job_qcount = models.CharField("qcount",max_length=100)
    job_examschedule=models.CharField("exam",max_length=100)
    job_cutoff=models.CharField("cut",max_length=100)
    status = models.CharField("status",max_length=100)
    @property
    def getapplicant(self):
        return applicant.objects.filter(job_id=self).count()
    

class question(models.Model):
    question_id = models.AutoField(primary_key=True)
    job_id= models.ForeignKey(job, on_delete=models.CASCADE, null=True)
    question_no =  models.CharField("qno",max_length=100)
    question = models.CharField("qn",max_length=100)
    option1 = models.CharField("op1",max_length=100)
    option2 = models.CharField("op2",max_length=100)
    option3 = models.CharField("op3",max_length=100)
    option4 = models.CharField("op4",max_length=100)
    answer= models.CharField("answer",max_length=100)

    
    
class complaint(models.Model):
    complaint_id = models.AutoField(primary_key=True)
    company_id = models.ForeignKey(company,on_delete=models.CASCADE,null=True)
    sub=models.CharField("subject",max_length=200)
    msg=models.CharField("message",max_length=500)
    reply=models.CharField("reply",max_length=500)

class company_complaint(models.Model):
    complaint_id = models.AutoField(primary_key=True)
    company_id = models.ForeignKey(company,on_delete=models.CASCADE,null=True)
    candidate_id = models.ForeignKey(candidate,on_delete=models.CASCADE,null=True)
    sub=models.CharField("subject",max_length=200)
    msg=models.CharField("message",max_length=500)
    reply=models.CharField("reply",max_length=500)
    
class user_feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    candidate_id = models.ForeignKey(candidate,on_delete=models.CASCADE,null=True)
    company_id = models.ForeignKey(company,on_delete=models.CASCADE,null=True)
    sub = models.CharField("sub",max_length=200)
    msg = models.CharField("message",max_length=500)
    reply = models.CharField("reply",max_length=500)

class feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    candidate_id = models.ForeignKey(candidate,on_delete=models.CASCADE,null=True)
    sub = models.CharField("sub",max_length=200)
    msg = models.CharField("message",max_length=500)
    reply = models.CharField("reply",max_length=500)

class company_feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    company_id = models.ForeignKey(company,on_delete=models.CASCADE,null=True)
    candidate_id = models.ForeignKey(candidate,on_delete=models.CASCADE,null=True)
    sub = models.CharField("sub",max_length=200)
    msg = models.CharField("message",max_length=500)
    reply = models.CharField("reply",max_length=500)
    

class applicant(models.Model):
    applicant_id = models.AutoField(primary_key=True)
    job_id = models.ForeignKey(job,on_delete=models.CASCADE,null=True)
    candidate_id = models.ForeignKey(candidate,on_delete=models.CASCADE,null=True)
    applicant_date = models.CharField("date",max_length=100)
    applicant_status = models.CharField("status",max_length=100)
    exam_status = models.CharField("status",max_length=100)
    resume_status = models.CharField("status",max_length=100)
    result_status = models.CharField("status",max_length=100)
    invitation_status=models.CharField("status",max_length=100)
    @property
    def getresult(self):
        return result.objects.get(applicant_id=self)

class result(models.Model):
    result_id = models.AutoField(primary_key=True)
    applicant_id = models.ForeignKey(applicant,on_delete=models.CASCADE,null=True)
    score = models.CharField("score",max_length=100)
    toquest = models.CharField("toquest",max_length=100)
    status = models.CharField("status",max_length=100)
    @property
    def checkpassed(self):
        c=invitation.objects.filter(result_id=self).count()
        if c == 0:
            return False
        else :
            return True
    @property
    def getpassed(self):
        return invitation.objects.get(result_id=self)


class qualificaton(models.Model):
    qualification_id = models.AutoField(primary_key=True)
    course = models.CharField("course",max_length=100)
    passyear = models.CharField("passyear",max_length=100)
    score = models.CharField("score",max_length=100)
    candidate_id = models.ForeignKey(candidate,on_delete=models.CASCADE,null=True)


class experience(models.Model):
    experience_id = models.AutoField(primary_key=True)
    exp_company = models.CharField("expcompany",max_length=100)
    exp_months = models.CharField("expmonths",max_length=100)
    exp_from=models.CharField("expfrom",max_length=100)
    exp_to=models.CharField("expto",max_length=100)
    candidate_id = models.ForeignKey(candidate,on_delete=models.CASCADE,null=True)



class invitation(models.Model):
    invit_id = models.AutoField(primary_key=True)
    result_id = models.ForeignKey(result,on_delete=models.CASCADE,null=True)
    status = models.CharField("status",max_length=100)
    invit_venu = models.CharField("venu",max_length=100)
    invit_time = models.CharField("time",max_length=100)

