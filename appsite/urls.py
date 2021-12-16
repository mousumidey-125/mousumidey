from django.contrib import admin
from django.urls import path
from appsite import views
admin.site.site_header = "CDC ADMIN"
admin.site.site_title = "CDC ADMIN"
admin.site.index_title = "CDC ADMIN"

urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('student/', views.student, name='student'),
    path('teacher/', views.teacher, name='teacher'),
    path('cdc/', views.cdc, name='cdc'),
    path('category/', views.category, name='category'),
    path('addquestion/', views.addquestion, name='addquestion'),
    path('allquestion/', views.allquestion, name='allquestion'),
    
    path('answersubmit/<int:pk>/<int:fk>', views.answersubmit, name='answersubmit'),
    path('category1/', views.category1, name='category1'),
    path('addquestion1/', views.addquestion1, name='addquestion1'),
    path('allquestion1/', views.allquestion1, name='allquestion1'),
    
    path('answersubmit1/<int:pk>/<int:fk>', views.answersubmit1, name='answersubmit1'),

    
]