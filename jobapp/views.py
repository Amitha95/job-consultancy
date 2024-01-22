from asyncore import read
from urllib import request, response
from xml.dom.expatbuilder import CDATA_SECTION_NODE
from datetime import date
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,redirect
from .models import login as log, candidate as cad,company as com,company_complaint as comc,job,result as rslt,complaint as cm,feedback as fd,qualificaton as qua,experience as exp,applicant as app, question as qn,invitation as invt,company_feedback as fd_cmp,user_feedback as ufd
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
# Create your views here.
def index(request): 
    data=job.objects.all()
    paginator = Paginator(data, 3)
    page = request.GET.get('page', 1)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request,"index.html",{"data":users})

def candidatehome(request): 
    return render(request,"candidatehome.html")

def register(request):
    return render(request,"user_register.html")

def about(request):
    return render(request,"about.html")

def Logout(request):       
    try:
        del request.session['id']
        del request.session['role']
        del request.session['username']
        response = redirect("/index")
        return response
    except:
        response = redirect("/index")
        return response
    
    
def jobs(request):
    search_query = request.GET.get('search', '')
    data = job.objects.all()

    if search_query:
        data = data.filter(
            Q(job_title__icontains=search_query) |
            Q(job_role__icontains=search_query) |
            Q(job_description__icontains=search_query)|
            Q(company_id__company_name__icontains=search_query)
            # Add more fields to search here...
        )

    paginator = Paginator(data, 6)
    page = request.GET.get('page', 1)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, "searchjob.html", {"data": users})

def adlogin(request):
    return render(request,"login.html")

def login(request):
    return render(request,"login.html")

def login_form(request):
    if request.POST:
        user = request.POST["username"]
        password = request.POST["password"]
        try:
            datac = log.objects.filter(username=user, password=password).count()
            if datac==1:
              data=log.objects.get(username=user, password=password)
              if data.role=="company":
                 request.session['username'] = data.username
                 request.session['role'] = data.role
                 request.session['id'] = data.logid
                 response=redirect('/companyhome')

                 return response
              elif data.role=="candidate":
                 request.session['username'] = data.username
                 request.session['role'] = data.role
                 request.session['id'] = data.logid
                 response=redirect('/jobs')
                 return response
              elif data.role=="admin":
                 request.session['username'] = data.username
                 request.session['role'] = data.role
                 request.session['id'] = data.logid
                 response=redirect('/adminhome')
                 return response
              else:
                 response = redirect('/index?msg=invalid access')
                 return response
            else:
              response = redirect('/index?msg=invalid username or password')
              return response
        except:
            response = redirect('/index?msg=something went wrong')
            return response
    else:
        response = redirect('/index')
        return response

def admin(request):
    if request.POST:
        user = request.POST["username"]
        password = request.POST["password"]
        
        datac = log.objects.filter(username=user, password=password,role="admin").count()
        if datac==1:
                data=log.objects.get(username=user, password=password,role="admin")
                request.session['username'] = data.username
                request.session['role'] = data.role
                request.session['id'] = data.logid
                response = redirect('/adminhome')
                return response
        else:
                 return render(request,"adminlog.html",{"msg":"invalid username or password"})
    else:
        return render(request,"adminlog.html",{"msg":""})
    
def adminhome(request):
    return render(request,"adminhome.html")

def companylogin(request):
    if request.POST:
        user = request.POST["username"]
        password = request.POST["password"]
        try:
            datac = log.objects.filter(username=user, password=password).count()
            if datac==1:
              data=log.objects.get(username=user, password=password)
              if data.role=="company":
                 request.session['username'] = data.username
                 request.session['role'] = data.role
                 request.session['id'] = data.logid
                 response=redirect('/companyhome')

                 return response
              elif data.role=="candidate":
                 request.session['username'] = data.username
                 request.session['role'] = data.role
                 request.session['id'] = data.logid
                 response=redirect('/jobs')
                 return response
              else:
                 response = redirect('/index?msg=invalid access')
                 return response
            else:
              response = redirect('/index?msg=invalid username or password')
              return response
        except:
            response = redirect('/index?msg=something went wrong')
            return response
    else:
        response = redirect('/index')
        return response


def companyreg(request):
    name=request.POST["name"]
    addr=request.POST["addr"]
    phone=request.POST["phone"]
    mail=request.POST["mail"]
    poc=request.POST["poc"]
    pocdis=request.POST["pocdis"]
    logo=request.FILES["logo"]
    location=request.POST["location"]
    web=request.POST["pocmail"]
    pocphone=request.POST["pocphone"]
    regno=request.POST["regno"]
    foundedyear=request.POST["foundedyear"]
    username=request.POST["username"]
    password=request.POST["password"]
    log.objects.create(username=username,password=password,role="company")
    datal=log.objects.last()
    com.objects.create(logid =datal ,company_name=name,company_address=addr, company_phone=phone,company_email=mail,company_poc=poc,
    company_logo=logo,company_location=location,company_pocmail=web,comapany_pocdis=pocdis,company_pocphone=pocphone,company_regno=regno,company_foundedyear=foundedyear,status="waiting")
    response = redirect('/index')
    return response

def candidreg(request):
    name=request.POST["name"]
    addr=request.POST["address"]
    phone=request.POST["phone"]
    mail=request.POST["mail"]
    files=request.FILES["photo"]
    toexp=request.FILES["toexp"]
    lastqua=request.POST["lastqua"]
    exp=request.POST["exp"]
    marks=request.POST["marks"]
    username=request.POST["username"]
    password=request.POST["password"]
    log.objects.create(username=username,password=password,role="candidate")
    datal=log.objects.last()
    cad.objects.create(logid =datal,candidate_name=name,candidate_address=addr, candidate_phone=phone,candidate_email=mail,
    candidate_photo=files,candidate_lastqualification=lastqua,candidate_experienced=exp,candidate_totalexperienced=toexp,status="approved")
    response = redirect('/index')
    return response

def companyhome(request):
    return render(request,"companyhome.html")

def candidhome(request):
    return render(request,"candidate.html")

def requests(request):
    return render(request,"requests.html")

def listcompany(request):
    datacom=com.objects.filter(status="approved").all()
    return render(request,"listcompany.html",{"dataco":datacom})

def listcandid(request):
    datast=cad.objects.filter(status="approved").all()
    return render(request,"list_candid.html",{"datalst":datast})

def comp_reply(request):
    data=fd_cmp.objects.all()
    return render(request,"comp_reply.html",{"data":data})

def deletecandid(request):
    id=request.POST["candidate_id"]
    cad.objects.filter(candidate_id=id).delete()
    response = redirect("listcandid")
    return response

def approvecandid(request):
    datacad=cad.objects.filter(status="waiting").all()
    return render(request,"approve_candid.html",{"dataz":datacad})

def approvedcandid(request):
    id=request.POST["candidate_id"]
    cad.objects.filter(candidate_id=id).update(status="approved")
    response=redirect("/approvecandid")
    return response
  
def rejectedcandid(request):
    id=request.POST["candidate_id"]
    cad.objects.filter(candidate_id=id).delete()
    response = redirect("/approvecandid")
    return response

def approvecompany(request):
    datacomp=com.objects.filter(status="waiting").all()
    return render(request,"approvecompany.html",{"datacomp":datacomp})

def approvedcompany(request):
    id=request.POST["company_id"]
    com.objects.filter(company_id=id).update(status="approved")
    response=redirect("/approvecompany")
    return response

def rejectedcompany(request):
    id=request.POST["company_id"]
    com.objects.filter(company_id=id).delete()
    response = redirect("/approvecompany")
    return response

def deletecompany(request):
    id=request.POST["company_id"]
    com.objects.filter(company_id=id).delete()
    response = redirect("listcompany")
    return response

def company_complaint(request):
    if request.POST:
        t1= request.POST["t1"]
        t2= request.POST["t2"]
        comc.objects.filter(complaint_id=t1).update(reply=t2)
    data=comc.objects.all()
    return render(request,"company_complaint.html",{"data":data})

def company_user_complaint(request):
    if request.POST:
        t1= request.POST["t1"]
        t2= request.POST["t2"]
        ufd.objects.filter(complaint_id=t1).update(complaint_reply=t2)
    data=ufd.objects.all()
    return render(request,"company_user_complaint.html",{"data":data})

def privacy(request):
    msg=""
    if request.POST:
        t1=request.POST["t1"]
        t2=request.POST["t2"]
        id=request.session['id']
        data=log.objects.get(logid=id)
        if data.password==t1:
            msg="sucessfully updated"
            log.objects.filter(logid=id).update(password=t2)
        else:
            msg="invalid current password"

    returnpage="adminhome.html"

    if(request.session.get("role","")==""):
        return redirect("/index")
    elif(request.session.get("role","")=="candidate"):
        returnpage="candidate.html"
    elif(request.session.get("role","")=="company"):
        returnpage="companyhome.html"
    return render(request,"privacy.html",{"role":returnpage,"msg":msg})


def candidate_feed(request):
    if request.POST:
        t1= request.POST["t1"]
        t2= request.POST["t2"]
        fd.objects.filter(feedback_id=t1).update(reply=t2)
    data=fd.objects.all()
    return render(request,"candidate_feed.html",{"data":data})

def approvejob(request):
    return render(request,"approvejob.html")

def listjob(request):
    return render(request,"listjob.html")


#candidate

def profileeditcandid(request):
    t1=request.GET["t1"]
    data=cad.objects.get(candidate_id=t1)
    return render(request,"profileeditscandid.html",{"d":data})

def profilecandid(request):
    id=request.session['id']
    data=log.objects.get(logid=id)
    datacn=cad.objects.get(logid=data)
    datast=cad.objects.filter(logid=data).all()
    datarr=qua.objects.filter(candidate_id=datacn).all()
    dataexp=exp.objects.filter(candidate_id=datacn).all()
    return render(request,"profilecandid.html",{"datalst":datast,"datarr":datarr,"dataexp":dataexp})
    
def profileeditscandid(request):
    t1=request.GET["t1"]
    name=request.POST["n1"]
    addr=request.POST["addr"]
    phone=request.POST["phone"]
    mail=request.POST["mail"]
    
    lastqua=request.POST["lastqua"]
    exp=request.POST["exp"]
    toexp=request.POST["toexp"]
    cad.objects.filter(candidate_id=t1).update(candidate_name=name,candidate_address=addr, candidate_phone=phone,candidate_email=mail,
    candidate_lastqualification=lastqua,candidate_experienced=exp,candidate_totalexperienced=toexp)
    response = redirect("profilecandid")
    return response
    
def feedback(request):
    id=request.session['id']
    datal=log.objects.get(logid=id)
    datas=cad.objects.get(logid=datal)
    #datastf=com.objects.all()
    if request.POST:
        t1=request.POST["subject"]
        t2=request.POST["msg"]
        #company=request.POST["company"]
        #datac=com.objects.get(company_id=company)
        fd.objects.create(candidate_id=datas,sub=t1,msg=t2,reply="")
    data=fd.objects.filter(candidate_id=datas).all()
    return render(request,"feedback.html",{"data":data})

def company_feedback(request):
    id=request.session['id']
    datal=log.objects.get(logid=id)
    datas=com.objects.get(logid=datal)
    #datastf=com.objects.all()
    if request.POST:
        t1=request.POST["subject"]
        t2=request.POST["msg"]
        #company=request.POST["company"]
        #datac=com.objects.get(company_id=company)
        comc.objects.create(company_id=datas,sub=t1,msg=t2,reply="")
    data=comc.objects.filter(company_id=datas).all()
    return render(request,"company_feedback.html",{"data":data})

def user_feedback(request):
    id=request.session['id']
    datal=log.objects.get(logid=id)
    datas=cad.objects.get(logid=datal)
    datastf=com.objects.all()
    if request.POST:
        t1=request.POST["subject"]
        t2=request.POST["msg"]
        company=request.POST["company"]
        datac=com.objects.get(company_id=company)
        fd_cmp.objects.create(candidate_id=datas,sub=t1,msg=t2,reply="",company_id=datac)
    data=fd_cmp.objects.filter(candidate_id=datas).all()
    return render(request,"user_feedback.html",{"data":data,"datastf":datastf})

def candidate_complaint(request):
    id=request.session['id']
    datal=log.objects.get(logid=id)
    datas=com.objects.get(logid=datal)
    if request.POST:
        t1= request.POST["t1"]
        t2= request.POST["t2"]
        fd_cmp.objects.filter(feedback_id=t1).update(reply=t2)
    data=fd_cmp.objects.filter(company_id=datas.company_id).all()
    return render(request,"candidate_complaint.html",{"data":data,"datas":datas})

def qualification(request):
    course=request.POST["course"]
    passyear=request.POST["passyear"]
    score=request.POST["score"]
    id=request.session['id']
    datal=log.objects.get(logid=id)
    dataqc=cad.objects.get(logid=datal)
    qua.objects.create(candidate_id=dataqc,course=course,passyear=passyear,score=score)
    response = redirect('/profilecandid')
    return response

def experience(request):
    company=request.POST["company"]
    month=request.POST["month"]
    fro=request.POST["fro"]
    to=request.POST["to"]
    id=request.session['id']
    datal=log.objects.get(logid=id)
    dataex=cad.objects.get(logid=datal)
    exp.objects.create(candidate_id=dataex,exp_company=company,exp_months=month,exp_from=fro,exp_to=to)
    response = redirect('/profilecandid')
    return response

def searchjob(request): 
    datalist=job.objects.filter(status="completed").all()
    return render(request,"searchjob.html",{"datalist":datalist})
   
def readmore(request):
    s1=request.GET["s1"]
    data=job.objects.get(job_id=s1)
    dl=log.objects.get(logid=request.session["id"])
    dataapp=cad.objects.get(logid=dl)
    chek=app.objects.filter(candidate_id=dataapp,job_id=data).count()
    return render(request,"applyjob.html",{"d":data,"s1":s1,"chek":chek})

def upload(request):
    id=request.POST["applicant_id"]
    t6=request.FILES["resume"]
    fs=FileSystemStorage()
    fs.save(t6.name,t6)

    app.objects.filter(applicant_id=id).update(resume_status=t6.name)
    response=redirect("application")
    return response
  
def applyjob(request):
    s1=request.GET["s1"]
    dt=date.today()
    datajob=job.objects.get(job_id=s1)
    dl=log.objects.get(logid=request.session["id"])
    dataapp=cad.objects.get(logid=dl)
    app.objects.create(candidate_id=dataapp,job_id=datajob,applicant_status="waiting",applicant_date=dt,exam_status="waiting",resume_status="waiting",result_status="waiting")
    response = redirect('/jobs')
    return response

def exam(request):
    id=request.GET["id"]
    aid=request.GET["aid"]
    dataj=job.objects.get(job_id=id)
    data=qn.objects.filter(job_id=dataj).all()
    tq=qn.objects.filter(job_id=dataj).count()
    return render(request,"exam.html",{"data":data,"tq":tq,"id":id,"aid":aid}) 

def examresult(request):
    id=request.GET["id"]
    aid=request.GET["aid"]
    dataj=job.objects.get(job_id=id)
    dataa=app.objects.get(applicant_id=aid)
    cutoff=int(dataj.job_cutoff)
    totq=int(request.POST["tq"])
    correct=0
    wrong=0
    skiped=0
    for i in range(1,totq+1):
        op=request.POST.get("op"+str(i),"")
        ans=request.POST["ans"+str(i)]
        if op == "" :
            skiped=skiped+1
        elif op == ans :
            correct=correct+1
        else :
            wrong=wrong+1
    
    cpes=(correct/totq)*100
    wpes=(wrong/totq)*100
    spes=(skiped/totq)*100
    cp=int(cpes)
    print(cp)
    st=""
    if cutoff <= cp :
        st="pass"
    else :
        st="fail"
    app.objects.filter(applicant_id=aid).update(exam_status="attended")
    rslt.objects.create(applicant_id=dataa,score=str(cp),toquest=str(totq),status=st)


    return redirect("application")


def application(request):
    datau=cad.objects.get(logid=request.session["id"])
    datacom=app.objects.filter(candidate_id=datau).all()
    return render(request,"application.html",{"datacom":datacom})

def attendexam(request):
    id=request.session["id"]
    datac=com.objects.get(logid=id)
    jobid =job.objects.filter(company_id=datac).get("job_id")
    datapps=app.objects.filter(applicant_status="waiting",job_id = jobid).all()
    return render(request,"applicantslist.html",{"datapps":datapps})

def attendexams(request):
    id=request.POST["id"]
    app.objects.filter(applicant_id=id).update(applicant_status="approved")
    response = redirect("/applicantslist")
    return response

def list_applicants(request):
    id=request.session["id"]
    datac=com.objects.get(logid=id)
    jobobj=job.objects.filter(company_id=datac).values('job_id')
    data = []
    appp=rslt.objects.all()
    inv=invt.objects.all()
    for i in jobobj:
        datapp=app.objects.filter(job_id = i.get('job_id')).values('applicant_id')
      
        if datapp.exists():
            for j in datapp:
                 for key in j.values():
                    # print(key)
                    data.append(key)
    app_list = []
    for i in data:
        appobj = app.objects.get(applicant_id = i)
        app_list.append(appobj)
        print(appobj)
    return render(request,"list_applicants.html",{"app_list":app_list,"appp":appp,"inv":inv})

def announced(request):
    id=request.POST["id"]
    app.objects.filter(applicant_id=id).update(exam_status="attended",result_status="")
    response=redirect("/list_applicants")
    return response

def announce(request):
    datann=app.objects.filter(exam_status="waiting",result_status="waiting").all()
    return render(request,"list_applicants.html",{"datapps":datann})

def invite(request):
    datares=app.objects.filter(resume_status="waiting").all()
    
    return render(request,"list_applicants.html",{"datares":datares})

def invited(request):
    id=request.POST["id"]
    app.objects.filter(applicant_id=id).update(invitation_status="invited")
    result = rslt.objects.get(applicant_id = id)
    invt.objects.create(result_id = result, status = "invited", invit_time = datetime.now())
    response=redirect("/list_applicants")   
    return response




def exam(request):
    id=request.GET["id"]
    aid=request.GET["aid"]
    dataj=job.objects.get(job_id=id)
    data=qn.objects.filter(job_id=dataj).all()
    tq=qn.objects.filter(job_id=dataj).count()
    return render(request,"exam.html",{"data":data,"tq":tq,"id":id,"aid":aid}) 

def examresult(request):
    id=request.GET["id"]
    aid=request.GET["aid"]
    dataj=job.objects.get(job_id=id)
    dataa=app.objects.get(applicant_id=aid)
    cutoff=int(dataj.job_cutoff)
    totq=int(request.POST["tq"])
    correct=0
    wrong=0
    skiped=0
    for i in range(1,totq+1):
        op=request.POST.get("op"+str(i),"")
        ans=request.POST["ans"+str(i)]
        if op == "" :
            skiped=skiped+1
        elif op == ans :
            correct=correct+1
        else :
            wrong=wrong+1
    
    cpes=(correct/totq)*100
    wpes=(wrong/totq)*100
    spes=(skiped/totq)*100
    cp=int(cpes)
    print(cp)
    st=""
    if cutoff <= cp :
        st="pass"
    else :
        st="fail"
    app.objects.filter(applicant_id=aid).update(exam_status="attended",result_status=st)
    rslt.objects.create(applicant_id=dataa,score=str(cp),toquest=str(totq),status=st)
    

    return redirect("application")


def application(request):
    datau=cad.objects.get(logid=request.session["id"])
    datacom=app.objects.filter(candidate_id=datau).all()
    return render(request,"application.html",{"datacom":datacom})


def editex(request):
    x1=request.GET["x1"]
    data=exp.objects.get(experience_id=x1)
    return render(request,"editexp.html",{"d":data})


def editexp(request):
    x1=request.GET["x1"]
    company=request.POST["company"]
    month=request.POST["month"]
    fro=request.POST["fro"]
    to=request.POST["to"]
    exp.objects.filter(experience_id=x1).update(exp_company=company,exp_months=month,exp_from=fro,exp_to=to)
    response = redirect("profilecandid")
    return response



def delete_exp(request):
    id=request.POST["experience_id"]
    exp.objects.filter(experience_id=id).delete()
    response = redirect('/profilecandid')
    return response

#editqua
def editqual(request):
    d1=request.GET["d1"]
    data=qua.objects.get(qualification_id=d1)
    return render(request,"editqua.html",{"d":data})


def editqua(request):
    d1=request.GET["d1"]
    course=request.POST["course"]
    passyear=request.POST["passyear"]
    score=request.POST["score"]
    
    qua.objects.filter(qualification_id=d1).update(course=course,passyear=passyear,score=score)
    response = redirect("profilecandid")
    return response



def delete_qua(request):
    id=request.POST["qualification_id"]
    qua.objects.filter(qualification_id=id).delete()
    response = redirect('/profilecandid')
    return response





#company

def approvejob(request):
    return render(request,"approvejob.html")

def listjob(request):
    return render(request,"listjob.html")


def add_jobs(request):
    msg="Successfully Updated"
    if request.POST:
        title=request.POST['title']
        role=request.POST['role']
        desc=request.POST['desc']
        desig=request.POST['designation']
        qualification=request.POST['qualification']
        exp=request.POST['exp']
        expin=request.POST['expin']
        salary=request.POST['salary']
        cutoff=request.POST['cutoff']
        examsch=request.POST['examsch']
        location=request.POST['location']
        quecount=request.POST['quecount']
        logid=request.session["id"]
        datac=com.objects.get(logid=logid)
        job.objects.create(company_id=datac,job_title=title,job_role=role,job_description=desc, job_designation=desig, job_salary=salary,job_qualificaion=qualification, job_experience=exp, job_experiencein=expin,job_location =location, job_cutoff=cutoff, job_examschedule=examsch,job_qcount=quecount,status="completed")
        msg="Successfully Updated"
    else:
        msg=""
        
    data1=job.objects.all()
    return render(request,"add_jobs.html",{"msg":msg,"data":data1})

def edit_jobs(request):
    id=request.session["id"]
    logid=log.objects.get(logid=id)
    datal=com.objects.get(logid=logid)
    datajob=job.objects.filter(company_id=datal,status="completed").all()
    return render(request,"edit_jobs.html",{"datajob":datajob})

def edt_job(request):
    b1=request.GET["c"]
    data=job.objects.get(job_id=b1)
    return render(request,"edtsjob.html",{"d":data})

def edtsjob(request):
    c=request.GET["c"]
    t4=request.POST["t4"]
    t5=request.POST["t5"]
    t6=request.POST["t6"]
    t7=request.POST["t7"]
    t8=request.POST["t8"]
    t9=request.POST["t9"]
    t1=request.POST["t1"]
    t2=request.POST["t2"]
    t3=request.POST["t3"]
    a2=request.POST["a2"]
    a3=request.POST["a3"]
    a4=request.POST["a4"]
    job.objects.filter(job_id=c).update(job_title =t4,job_role=t5,job_description=a4,job_designation=t6,job_qualificaion=t7,job_experience=t8,job_experiencein=t9,job_salary=t1,job_location=t2,job_examschedule=t3,job_cutoff=a2,job_qcount=a3)
    response = redirect("edit_jobs")
    return response

def delete_jobs(request):
    id=request.POST["id"]
    job.objects.filter(job_id=id).delete()
    response = redirect("edit_jobs")
    return response

def approve_job(request):
    datajb=job.objects.filter(status="waiting").all()
    return render(request,"approve_jobs.html",{"data":datajb})
    
def approved_job(request):
    id=request.POST["id"]
    job.objects.filter(job_id=id).update(status="completed")
    response = redirect("/edit_jobs")
    return response

def approve_listjobs(request):
    id=request.session["id"]
    logid=log.objects.get(logid=id)
    datal=com.objects.get(logid=logid)
    datajab=job.objects.filter(company_id=datal).all()

    return render(request,"approve_listjobs.html",{"datajab":datajab})

#admin job section
def list_jobs(request):
    datalst=job.objects.filter(status="approved").all()
    return render(request,"list_jobs.html",{"datalst":datalst})

def delete_listjobs(request):
    id=request.POST["id"]
    job.objects.filter(job_id=id).delete()
    response = redirect("list_jobs")
    return response

def approve_adjob(request):
    datajbs=job.objects.filter(status="waiting").all()
    return render(request,"list_jobs.html",{"datajbs":datajbs})
    
def approved_adjob(request):
    id=request.POST["id"]
    job.objects.filter(job_id=id).update(status="completed")
    response = redirect("/list_jobs")
    return response

def approve_finaljob(request):
    datafljob=job.objects.filter(status="waiting").all()
    return render(request,"approve_listjobs.html",{"datafljob":datafljob})

def approved_finaljob(request):
    id=request.POST["id"]
    job.objects.filter(job_id=id).update(status="finished")
    response = redirect("/approve_listjobs")
    return response

def new_jobs(request):
    datalist=job.objects.filter(status="completed").all()
    return render(request,"new_jobs.html",{"datalist":datalist})



#applicant
def applicant(request):
    d1=date.today()
    id=request.session["id"]
    datac=com.objects.get(logid=id)
    datapjob=job.objects.get(job_id=datac)
    datapp=app.objects.filter(applicant_id=applicant)
    app.objects.create(login=datapp,applicant_date=d1,applicant_status="waiting", exam_status="waiting",company=datac,job=datapjob)
    return render(request,"list_applicants.html",{"datac":datac,"datapjob":datapjob,"datapp":datapp})

def delete_applicants(request):
    id=request.POST["id"]
    app.objects.filter(applicant_id=id).delete()
    response = redirect("list_applicants")
    return response

def approve_applicants(request):
    datapps=app.objects.filter(applicant_status="waiting",exam_status="waiting",resume_status="waiting",result_status="waiting").all()
    return render(request,"list_applicants.html",{"datapps":datapps})
    
def approved_applicants(request):
    id=request.POST["id"]
    app.objects.filter(applicant_id=id).update(applicant_status="accepted",exam_status="accepted",resume_status="accepted",result_status="accepted")
    response = redirect("/list_applicants")
    return response



def new_applicants(request):
    dataapps=app.objects.filter(applicant_status="approved",exam_status="waiting",resume_status="waiting",result_status="waiting").all()
    return render(request,"new_applicants.html",{"dataapps":dataapps})

def applicantslist(request):
    msg = ""
    # data1=app.objects.all()
    id=request.session["id"]
    datal=log.objects.get(logid=id)
    datac=com.objects.get(logid=datal)
    jobobj=job.objects.filter(company_id = datac).all()
    for j in jobobj:
        jobid =job.objects.get(job_id = j.job_id)   
        data1=app.objects.filter(job_id = jobid).all()
    return render(request,"applicantslist.html",{"msg":msg,"data":data1})
    

#questions
    
def questions(request): 
    id=request.GET["id"]
    dataq=job.objects.get(job_id=id)
    tq=dataq.job_qcount
    data=qn.objects.filter(job_id=dataq).all()
    qc=qn.objects.filter(job_id=dataq).count()
    if int(tq) <= int(qc) :
        return render(request,"questions1.html",{"dataqus":data,"id":id})
    qc+=1
    
    return render(request,"questions.html",{"dataqus":data,"id":id,"qc":qc})

def answers(request):
    qu=request.POST["qu"]
    qu1=request.POST["qu1"]
    q3=request.POST["q3"]
    q4=request.POST["q4"]
    q5=request.POST["q5"]
    q6=request.POST["q6"]
    q8=request.POST["q8"] 
    id=request.GET["id"]
    dataq=job.objects.get(job_id=id)
    qn.objects.create(job_id=dataq,question_no=qu,question=qu1,option1=q3, option2=q4,option3=q5, option4=q6,answer =q8)
    
    return redirect("questions/?id="+id)

def editque(request):
    d1=request.GET["b"]
    id=request.GET["id"]
    data=qn.objects.get(question_id=d1)
    return render(request,"edit_question.html",{"d":data,"id":id})


def edit_question(request):
    b=request.GET["b"]
    id=request.GET["id"]
    qno=request.POST["qno"]
    question=request.POST["question"]
    option1=request.POST["option1"]
    option2=request.POST["option2"]
    option3=request.POST["option3"]
    option4=request.POST["option4"]
    answer=request.POST["answer"]
    qn.objects.filter(question_id=b).update(question_no=qno,question=question, option1=option1, option2=option2,option3=option3, option4=option4,answer =answer)
    response = redirect("questions/?id="+id)
    return response

from pdf2docx import Converter
import os
from django.http import FileResponse

resumes = []
converted_resumes = []

def convert_resume(resume_file):
    if resume_file is None:
        return None

    pdf_path = resume_file.name
    doc_path = f"converted_{pdf_path}.docx"

    # Save the uploaded file temporarily
    with open(pdf_path, 'wb') as f:
        for chunk in resume_file.chunks():
            f.write(chunk)

    # Convert PDF to Word document
    cv = Converter(pdf_path)
    cv.convert(doc_path, start=0, end=None)
    cv.close()

    # Remove the temporary PDF file
    os.remove(pdf_path)

    return doc_path


def upload_resume(request):
    if request.method == 'POST' and 'resume_file' in request.FILES:
        resume_file = request.FILES['resume_file']

        converted_resume = convert_resume(resume_file)  # Convert the uploaded resume
        if converted_resume:
            converted_resumes.append(converted_resume)  # Store the converted resume

        return redirect('converted_resume')

    return render(request, 'upload_resume.html')

def choose_best_resume(request):
    best_resume = None
    best_score = 0

    for i, resume1 in enumerate(converted_resumes):
        score = 0

        for j, resume2 in enumerate(converted_resumes):
            if i != j:  # Skip comparing the resume with itself
                similarity_score = calculate_similarity(resume1, resume2)
                score += similarity_score

        # Update the best resume if the score is higher
        if score > best_score:
            best_score = score
            best_resume = resume1

    return render(request, 'choose_best_resume.html', {'best_resume': best_resume, 'converted_resumes': converted_resumes})



def converted_resume(request):
    return render(request, 'converted_resume.html', {'converted_resumes': converted_resumes})

def download_resume(request, resume_filename):
    file_path = os.path.join(os.getcwd(), resume_filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = FileResponse(file)
            response['Content-Disposition'] = f'attachment; filename="{resume_filename}"'
            return response

    return redirect('converted_resume')


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(resume1, resume2):
    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform the resumes into TF-IDF feature vectors
    features = vectorizer.fit_transform([resume1, resume2])

    # Compute the cosine similarity between the feature vectors
    similarity_matrix = cosine_similarity(features[0], features[1])

    # Get the cosine similarity score
    similarity_score = similarity_matrix[0][0]

    return similarity_score

# Example usage
resume1 = "Resume 1 text..."
resume2 = "Resume 2 text..."
score = calculate_similarity(resume1, resume2)
print("Similarity score:", score)

# views.py
from django.shortcuts import render
from pyresparser import ResumeParser

def upload_reference_resume(request):
    if request.method == 'POST' and 'resume_file' in request.FILES:
        reference_resume_file = request.FILES['resume_file']

        # Parse the reference resume and extract keywords
        reference_resume_data = ResumeParser(reference_resume_file).get_extracted_data()
        reference_keywords = extract_keywords(reference_resume_data)

        # Perform any other processing on reference_keywords as needed

    return render(request, 'resume_parser.html')

# views.py
import os

def list_and_score_resumes(request):
    resumes_folder_path = 'path_to_resumes_folder'  # Replace with the path to the folder containing resumes

    # Get a list of all resumes in the folder
    resumes = os.listdir(resumes_folder_path)

    resume_scores = []
    for resume_filename in resumes:
        # Create the full path to the resume file
        resume_file_path = os.path.join(resumes_folder_path, resume_filename)

        # Parse the resume and calculate the score
        resume_data = ResumeParser(resume_file_path).get_extracted_data()
        score = calculate_resume_score(resume_data, reference_keywords)  # Implement the scoring algorithm from the previous response

        # Add the resume filename and score to the list
        resume_scores.append((resume_filename, score))

    return render(request, 'resume_scores.html', {'resume_scores': resume_scores})



