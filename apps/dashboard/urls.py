from django.conf.urls import url
from . import views           # This line is new!

print("I M IN USER DASHBOARD APP URLS.PY")
urlpatterns = [
    url(r'^$', views.index),
    url(r'^signIn$',views.signIn),
    url(r'^register$',views.register),
    url(r'^success$',views.success),
    url(r'^regVal$',views.regVal),
    url(r'^logVal$',views.logVal),
    url(r'^dashboard$',views.dashboard),
    url(r'^new$',views.new),
    url(r'^admin$', views.admin),
    url(r'^admindashboard$', views.admindashboard),
    url(r'^(?P<number>\d+)\/show$', views.show),
    url(r'^edit\/(?P<number>\d+)$',views.edit),
    url(r'^userInfoVal$',views.userInfoVal),
    url(r'^(?P<number>\d+)\/userpwdVal$',views.userpwdVal),
    url(r'^useredit$',views.useredit),
    url(r'^(?P<number>\d+)\/destroy$',views.destroy),
    # url(r'^post_msg$',views.post_msg),
    # url(r'^post_cmt$',views.post_cmt),
    url(r'^adminCollegeTab$',views.adminCollegeTab),
    url(r'^adminTaskTab$',views.adminTaskTab),
    url(r'^addChecklist$',views.addChecklist),
    url(r'^updateChecklist$',views.updateChecklist),
    url(r'^logout$',views.logout)
]
