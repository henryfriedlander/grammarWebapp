from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^generate/', views.generate, name = 'generate'), # generate sentence
    url(r'^generate/?newSent=make+a+new+sentence#', views.generate, name = 'generate2'),
    url(r'^quiz/', views.quiz, name = 'quiz'), # useless
    url(r'^about/', views.about, name = 'about'), # about page
    url(r'^quizQuestion/(?P<quiz_id>\d+)/(?P<question_id>\d+)/', views.quizQuestion, name = 'quiz1'), # shows the question
    url(r'^startQuiz/', views.startQuiz, name = 'startQuiz'), # form to begin quiz
    url(r'^submit/(?P<quiz_id>\d+)/(?P<question_id>\d+)/', views.submit, name = 'submit'), # check correctness, redirects to next question
    url(r'^teacher/', views.teacherLogin, name = 'teacherLogin'), # takes in username and password
    url(r'^attemptLogon/', views.attemptLogon, name = 'attemptLogon'), # checks username/password combo
    url(r'^viewScores/(?P<teacher_id>\d+)/', views.viewScores, name = 'viewScores') # teacher can view scores of their students. 
]