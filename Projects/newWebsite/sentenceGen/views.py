from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
import random
from . import forms
from models import Quiz, Question, Word, Teacher
# Create your views here.

# import henrysCode
from grammar import getSentence

def home(request):
    return render(request, 'sentenceGen/home.html')

def newsentence():
    return getSentence.getSentence()#random.choice([["django", "programming", "fun", "woo"], ["becca", "woot", "yay"], ["programming", "computer"]])

def joinSentence(sentence):
    realSentence = getSentence.getStrSent(sentence)
    print "sentence: ", 
    print realSentence
    return realSentence

def getPartOfSpeech(word): # fix
    if type(word) == str:
        return "punctuation"
    return word.getPOS()#random.choice(["noun"]) #, "adjective", "adverb"])

def getWord(word): # return the string
    # fix
    return word.getWord()

def makeWord(word, question, index):
    part_of_speech = getPartOfSpeech(word)
    word = getWord(word)
    w = Word(question = question, word = word, part_of_speech = part_of_speech, index = index)
    w.save()
    return w.pk

def makeQuestion(sentence):
    q = Question(sentence = joinSentence(sentence), wordPKs = "")
    q.save()

    index = 0
    wordPKs = ""

    for word in sentence:
        if getPartOfSpeech(word) != "punctuation":
            current_pk = makeWord(word, q, index)
            index += 1
            wordPKs = wordPKs + str(current_pk) + ","

    wordPKs = wordPKs[:-1]
    print(wordPKs)


    q.wordPKs = wordPKs

    q.save()
    return q.pk

def generate(request):
    sentence = joinSentence(newsentence())
    return render(request, 'sentenceGen/generate.html', {'sentence': sentence})

def quiz(request):
    form = forms.QuizStart()
    return render(request, 'sentenceGen/quiz.html', {'form':form})

def about(request):
    return render(request, 'sentenceGen/about.html')

def startQuiz(request):
    if request.method == "POST":
        form = forms.QuizStart(request.POST)

        if form.is_valid():

            data = form.cleaned_data

            name = data['name']
            mode = data['mode']
            teacher = data['teacher']

            mode = int(mode)
            possible_modes = getPossibleQuestionModes()
            for (i, m) in possible_modes:
                if i == mode:
                    mode = m

            quiz = Quiz.objects.create(name = name, mode = mode, teacher = teacher, score = 0, attempts = 0, old_questions = "")
            quiz.save()

            sentence = newsentence()
            question_id = makeQuestion(sentence)


    return redirect('quiz1', quiz_id = quiz.pk, question_id = question_id)


def getPossibleQuestionModes():
    return [(1, 'noun'), (2, 'adverb'), (3, 'adjective')]

def quizQuestion(request, quiz_id, question_id):

    quiz = get_object_or_404(Quiz, pk = quiz_id)
    question = get_object_or_404(Question, pk = question_id)

    return render(request, 'sentenceGen/quizQuestion.html', {'sentence': question.sentence, 'mode': quiz.mode, 'question':question, 'quiz': quiz})

def findAnswer(question, i):
    word_pks = question.wordPKs.split(",")
    for pk in word_pks:
        word = get_object_or_404(Word, pk = int(pk))
        if word.index == i:
            return pk

def submit(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, pk = quiz_id)
    question = get_object_or_404(Question, pk = question_id)
    sentence = question.sentence
    words = sentence.split()
    correct = True

    correct_words = ""
    chosen_words = ""

    for i in range(len(words)):
        key = "word%d" % (i+1)
        try:
            answer = question.word_set.get(pk = request.POST[key])
            print ("POS: " + answer.part_of_speech)
            chosen_words = chosen_words + answer.word + ", "
            if str(answer.part_of_speech) != str(quiz.mode):
                correct = False
            else:
                correct_words = correct_words + answer.word + ", "

        except:
            answer_pk = findAnswer(question, i)

            answer = get_object_or_404(Word, pk = answer_pk)
            print ("POS: " + answer.part_of_speech)
            if str(answer.part_of_speech) == str(quiz.mode):
                print(str(quiz.mode), str(answer.part_of_speech), str(answer.word))
                correct_words = correct_words + answer.word + ", "
                correct = False

    if correct == True:
        quiz.score += 1

    correct_words = correct_words[:-2]
    chosen_words = chosen_words[:-2]

    question.correct_words = correct_words
    question.chosen_words = chosen_words
    question.save()

    quiz.attempts += 1
    quiz.old_questions = quiz.old_questions + str(question_id) + ","
    quiz.save()

    if quiz.attempts < 10:

        sentence = newsentence()
        question_id = makeQuestion(sentence)

        return redirect('quiz1', quiz_id = quiz.pk, question_id = question_id)

    else:
        old_questions = quiz.old_questions[:-1]
        old_questions = old_questions.split(",")

        q0 = get_object_or_404(Question, pk = int(old_questions[0]))
        q1 = get_object_or_404(Question, pk = int(old_questions[1]))
        q2 = get_object_or_404(Question, pk = int(old_questions[2]))
        q3 = get_object_or_404(Question, pk = int(old_questions[3]))
        q4 = get_object_or_404(Question, pk = int(old_questions[4]))
        q5 = get_object_or_404(Question, pk = int(old_questions[5]))
        q6 = get_object_or_404(Question, pk = int(old_questions[6]))
        q7 = get_object_or_404(Question, pk = int(old_questions[7]))
        q8 = get_object_or_404(Question, pk = int(old_questions[8]))
        q9 = get_object_or_404(Question, pk = int(old_questions[9]))

        return render(request, 'sentenceGen/submit.html', {'quiz':quiz, 'q0':q0, 'q1':q1, 'q2':q2, 'q3':q3, 'q4':q4, 'q5':q5, 'q6':q6, 'q7':q7, 'q8':q8, 'q9':q9})

def teacherLogin(request):
    form = forms.TeacherLogin()
    return render(request, 'sentenceGen/teacherLogin.html', {'form':form})

def attemptLogon(request):

    if request.method == "POST":
        form = forms.TeacherLogin(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            code = data['code']
            password = data['password']

            poss_teachers = Teacher.objects.all()

            for teacher in poss_teachers:
                if teacher.code == code and teacher.password == password:
                    return redirect('viewScores', teacher_id = teacher.pk)

    return redirect('teacherLogin')

def viewScores(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk = teacher_id)
    quizzes = Quiz.objects.filter(teacher__startswith = teacher.code)

    return render(request, 'sentenceGen/viewScores.html', {'teacher':teacher, 'quizzes':quizzes})

def lightningRound(request): 
    sentence = newsentence()
    question_id = makeQuestion(sentence)
    question = get_object_or_404(Question, pk = question_id)
    modes = getPossibleQuestionModes()
    random_index = random.randrange(0,len(modes))
    random_tuple = modes[random_index]
    mode = random_tuple[1]

    #correct_words = getCorrectWordsForQuestion(question, mode)

    return render(request, 'sentenceGen/lightningQuestion.html', {'sentence': question.sentence, 'mode': mode, 'question':question})

#def getChosenWordsFromRequest(request):

def getCorrectWordsForQuestion(question, mode):
    correct_words = set()
    words = question.sentence.split()

    for word in question.word_set.all():
        if doesPOSMatchMode(word, mode):
            print ("adding to correct words: " + word.word)
            correct_words.add(word)

    return correct_words

def doesPOSMatchMode(word, mode):
    return str(word.part_of_speech) == str(mode)



def scoreQuestion(request, question_id, mode):
    question = get_object_or_404(Question, pk = question_id)
    sentence = question.sentence
    words = sentence.split()
    correct = True


    print ("Correct Words: " + str(getCorrectWordsForQuestion(question, mode)))

    correct_words = ""
    chosen_words = ""

    for i in range(len(words)):
        key = "word%d" % (i+1)
        try:
            answer = question.word_set.get(pk = request.POST[key])
            print ("POS: " + answer.part_of_speech)
            chosen_words = chosen_words + answer.word + ", "
            if str(answer.part_of_speech) != str(mode):
                correct = False
            else:
                correct_words = correct_words + answer.word + ", "

        except:
            answer_pk = findAnswer(question, i)

            answer = get_object_or_404(Word, pk = answer_pk)
            print ("POS: " + answer.part_of_speech)
            if str(answer.part_of_speech) == str(mode):
                print(str(mode), str(answer.part_of_speech), str(answer.word))
                correct_words = correct_words + answer.word + ", "
                correct = False

    return render(request, 'sentenceGen/lightningAnswer.html', {'sentence': question.sentence, 'mode': mode, 'question':question, 'correct_words': correct_words, 'chosen_words':chosen_words, 'correct':correct})