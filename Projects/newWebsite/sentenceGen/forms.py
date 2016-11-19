from django import forms

class QuizStart(forms.Form):
    name = forms.CharField(required = True)
    mode = forms.ChoiceField(choices = [(1, 'noun'), (2, 'adverb'), (3, 'adjective')])
    teacher = forms.CharField(required = True)

class TeacherLogin(forms.Form):
    code = forms.CharField(required = True)
    password = forms.CharField(widget = forms.PasswordInput())
