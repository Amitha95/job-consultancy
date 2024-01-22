from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
path('',views.index,name="index"),
path('index',views.index,name="index"),
path("Logout",views.Logout,name='Logout'),
path("privacy/",views.privacy,name="privacy"),
path("about",views.about,name="about"),
path('admin',views.admin,name="admin"),
path('adminhome',views.adminhome,name="adminhome"),
path('candidreg', views.candidreg,name="candidreg"),
path('candidhome',views.candidhome,name="candidhome"),
path('candidatehome',views.candidatehome,name="candidatehome"),
path('companylogin',views.companylogin,name="companylogin"),
path('companyreg',views.companyreg,name="companyreg"),
path('approvecompany',views.approvecompany,name="approvecompany"),
path('approvedcompany',views.approvedcompany,name="approvedcompany"),
path('rejectedcompany',views.rejectedcompany,name="rejectedcompany"),
path('listcompany',views.listcompany,name="listcompany"),

path('companyhome',views.companyhome,name="companyhome"),
path('listcandid',views.listcandid,name="listcandid"),
path('approvecandid',views.approvecandid,name="approvecandid"),
path('approvedcandid',views.approvedcandid,name="approvedcandid"),
path('deletecandid',views.deletecandid,name="deletecandid"),
path('rejectedcandid',views.rejectedcandid,name="rejectedcandid"),
path('deletecompany',views.deletecompany,name="deletecompany"),
path('company_complaint',views.company_complaint,name="company_complaint"),
path('candidate_feed',views.candidate_feed,name="candidate_feed"),
path('approvejob',views.approvejob,name="approvejob"),
path('listjob',views.listjob,name="listjob"),

path('feedback',views.feedback,name="feedback"),
path("user_feedback",views.user_feedback,name="user_feedback"),
path("register",views.register,name="register"),
path("candidate_complaint",views.candidate_complaint,name="candidate_complaint"),
path("comp_reply",views.comp_reply,name="comp_reply"),
path("company_feedback",views.company_feedback,name="company_feedback"),


path('profileeditcandid',views.profileeditcandid,name="profileeditcandid"),
path('profileeditscandid',views.profileeditscandid,name="profileeditscandid"),
path('profilecandid',views.profilecandid,name="profilecandid"),
path('qualification',views.qualification,name="qualification"),
path('experience',views.experience,name="experience"),
path('searchjob',views.searchjob,name="searchjob"),
path('readmore',views.readmore,name="readmore"),
path('applyjob/',views.applyjob,name="applyjob"),
path('application,',views.application,name="application"),
path('exam',views.exam,name="exam"),
path('upload',views.upload,name="upload"),
path('examresult',views.examresult,name="examresult"),


path("login",views.login,name="login"),
path("login_form",views.login_form,name="login_form"),
path('examresult',views.examresult,name="examresult"),


#company
path("jobs",views.jobs,name="jobs"),
path('edt_job',views.edt_job,name="edt_job"),
path('edtsjob',views.edtsjob,name="edtsjob"),
path('edit_jobs',views.edit_jobs,name="edit_jobs"),
path('delete_jobs',views.delete_jobs,name="delete_jobs"),
path('approve_job',views.approve_job,name="approve_job"),
path('approved_job',views.approved_job,name="approved_job"),
path('list_jobs',views.list_jobs,name="list_jobs"),
path('approve_listjobs',views.approve_listjobs,name="approve_listjobs"),
path('delete_listjobs',views.delete_listjobs,name="delete_listjobs"),
path('new_jobs',views.new_jobs,name="new_jobs"),
path('add_jobs',views.add_jobs,name="add_jobs"),
path('approve_adjob',views.approve_adjob,name="approve_adjob"),
path('approved_adjob',views.approved_adjob,name="approved_adjob"),
path('approve_finaljob',views.approve_finaljob,name="approve_finaljob"),
path('approved_finaljob',views.approved_finaljob,name="approved_finaljob"),
path('applicant',views.applicant,name="applicant"),
path('application',views.application,name="application"),

path('questions',views.questions,name="questions"),
path('questions/',views.questions,name="questions"),
path('answers',views.answers,name="answers"),
path('editque',views.editque,name="editque"),
path('edit_question',views.edit_question,name="edit_question"),

path('list_applicants',views.list_applicants,name="list_applicants"),
path('applicantslist',views.applicantslist,name="applicantslist"),
path('delete_applicants',views.delete_applicants,name="delete_applicants"),
path('approve_applicants',views.approve_applicants,name="approve_applicants"),
path('approved_applicants',views.approved_applicants,name="approved_applicants"),
path('new_applicants',views.new_applicants,name="new_applicants"),

path('attendexam',views.attendexam,name="attendexam"),
path('attendexams',views.attendexams,name="attendexams"),
path('announce',views.announce,name="announce"),
path('announced',views.announced,name="announced"),
path('invite',views.invite,name="invite"),
path('invited',views.invited,name="invited"),

path('delete_qua',views.delete_qua,name="delete_qua"),
path('editqual',views.editqual,name="editqual"),
path('editqua',views.editqua,name="editqua"),

path('editex',views.editex,name="editex"),
path('editexp',views.editexp,name="editexp"),
path('delete_exp',views.delete_exp,name="delete_exp"),

path('upload_resume/', views.upload_resume, name='upload_resume'),
    path('converted/', views.converted_resume, name='converted_resume'),
    path("convert_resume",views.convert_resume,name="convert_resume"),
     path('download_resume/<str:resume_filename>/', views.download_resume, name='download_resume'),
     path("choose_best_resume",views.choose_best_resume,name="choose_best_resume"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)