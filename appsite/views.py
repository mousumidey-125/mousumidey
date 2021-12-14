from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from .decorator import *
from django.core.exceptions import PermissionDenied
from datetime import datetime
from datetime import date

# Create your views here.





@OnlyAuth
def signin(request):
    LM = LoginForm(request.POST or None)
    if request.method == 'POST':
        if LM.is_valid():
            UserName = request.POST.get('username')
            PassWord = request.POST.get('password')
            user = authenticate(request, username=UserName, password=PassWord)

            if user is not None and user.is_cdc:
                login(request, user)
                return redirect('cdc')
            elif user is not None and user.is_teacher:
                login(request, user)
                return redirect('teacher')
            elif user is not None and user.is_student:
                login(request, user)
                return redirect('student')
            else:
                messages.error(request, 'Username or Password is incorrect')
        else:
            messages.error(request, LM.errors)
    else:
        LM = LoginForm()
    context = {'form': LM}
    return render(request, 'common/signin.html', context)


@OnlyAuth
def signup(request):
    if request.method == 'POST':
        SF = SignupForm(request.POST)
        if SF.is_valid():
            isStudent = SF.cleaned_data.get('is_student')
            isTeacher = SF.cleaned_data.get('is_teacher')
            if isStudent:
                SignUpUser = SF.save(commit=False)
                SignUpUser.is_student = True
                SignUpUser.status = True
                SignUpUser.save()
            elif isTeacher:
                SignUpUser = SF.save(commit=False)
                SignUpUser.is_teacher = True
                SignUpUser.status = False
                SignUpUser.save()
            else:
                messages.warning(request, 'Please Select Your user Type')
                return redirect('signin')
            user = SF.cleaned_data.get('username')
            messages.success(request, 'Account Created for ' + user)
            return redirect('signin')
        else:
            messages.error(request, SF.errors)
    else:
        SF = SignupForm()
    context = {'form': SF}
    return render(request, 'common/signup.html', context)


@login_required(login_url='signin')
def signout(request):
    logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def student(request):
    if not request.user.is_student:
        raise PermissionDenied
    if not request.user.status:
        return render(request, 'common/notActive.html')

    userdata = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        UserProfileForm = SignupForm(
            request.POST, request.FILES, instance=userdata)

        if UserProfileForm.is_valid():
            student = UserProfileForm.save(commit=False)
            student.is_student = True
            student.status = True
            UserProfileForm.save()
            messages.success(
                request, 'Profile is Updated. please login again to craete a new Session')
            return redirect('signout')
        else:
            messages.warning(request, UserProfileForm.errors)
    else:
        UserProfileForm = SignupForm(instance=userdata)
    context = {'StudentData': userdata, 'UserProfileForm': UserProfileForm}
    return render(request, 'student/studentprofile.html', context)


@login_required(login_url='signin')
def teacher(request):
    if not request.user.is_teacher:
        raise PermissionDenied
    if not request.user.status:
        return render(request, 'common/notActive.html')
    userdata = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        UserProfileForm = SignupForm(
            request.POST, request.FILES, instance=userdata)

        if UserProfileForm.is_valid():
            student = UserProfileForm.save(commit=False)
            student.is_teacher = True
            student.status = True
            UserProfileForm.save()
            messages.success(
                request, 'Profile is Updated. please login again to craete a new Session')
            return redirect('signout')
        else:
            messages.warning(request, UserProfileForm.errors)
    else:
        UserProfileForm = SignupForm(instance=userdata)
    context = {'StudentData': userdata, 'UserProfileForm': UserProfileForm}
    return render(request, 'teacher/teacherprofile.html', context)










@login_required(login_url='signin')
def cdc(request):
    if not request.user.is_cdc:
        raise PermissionDenied
    return render(request, 'common/cdc.html')


@login_required(login_url='signin')
def category(request):
    if not request.user.status:
        return render(request, 'common/notActive.html')
    userdata = User.objects.get(pk=request.user.id)
    
    categorydata = QuestionCategory.objects.filter(owner=request.user.id)
    if request.method == 'POST':
        CategoryForm = CategoryManagement(request.POST)
        if CategoryForm.is_valid():
            CF = CategoryForm.save(commit=False)
            CF.status = True
            CF.owner = request.user.id
            CF.save()
            messages.success(
                request, 'Your Category Details is submited and approved by CDC')
            CategoryForm = CategoryManagement(None)
        else:
            messages.warning(request, CategoryForm.errors)
    else:
        CategoryForm = CategoryManagement()

    context = {'StudentData': userdata, 'categorydata': categorydata,
               'CategoryForm': CategoryForm}
    return render(request, 'student/category.html', context)

@login_required(login_url='signin')
def category1(request):
    if not request.user.status:
        return render(request, 'common/notActive.html')
    userdata = User.objects.get(pk=request.user.id)
    
    categorydata = QuestionCategory.objects.filter(owner=request.user.id)
    if request.method == 'POST':
        CategoryForm = CategoryManagement(request.POST)
        if CategoryForm.is_valid():
            CF = CategoryForm.save(commit=False)
            CF.status = True
            CF.owner = request.user.id
            CF.save()
            messages.success(
                request, 'Your Category Details is submited and approved by CDC')
            CategoryForm = CategoryManagement(None)
        else:
            messages.warning(request, CategoryForm.errors)
    else:
        CategoryForm = CategoryManagement()

    context = {'StudentData': userdata, 'categorydata': categorydata,
               'CategoryForm': CategoryForm}
    return render(request, 'teacher/category1.html', context)

    
    

@login_required(login_url='signin')
def addquestion(request):
    if not request.user.status:
        return render(request, 'common/notActive.html')

    categorydata = QuestionCategory.objects.all()
    userdata = User.objects.get(pk=request.user.id)
    questiondata = Question.objects.filter(owner=request.user.id)

    if request.method == 'POST':
        QuestionForm = QuestionManagement(request.POST, request.FILES)
        print(QuestionForm)
        if QuestionForm.is_valid():
            QF = QuestionForm.save(commit=False)
            QF.status = False
            QF.owner = request.user.id
            QF.postedtime = date.today()
            QF.save()
            messages.success(
                request, 'Your Question  is submited ')
            QuestionForm = QuestionManagement(None)
        else:
            messages.warning(request, QuestionForm.errors)
    else:
        QuestionForm = QuestionManagement()

    context = {'StudentData': userdata, 'categorydata': categorydata,
               'QuestionForm': QuestionForm, 'questiondata': questiondata}
    return render(request, 'student/addquestion.html', context)


@login_required(login_url='signin')
def addquestion1(request):
    if not request.user.status:
        return render(request, 'common/notActive.html')

    categorydata = QuestionCategory.objects.all()
    userdata = User.objects.get(pk=request.user.id)
    questiondata = Question.objects.filter(owner=request.user.id)

    if request.method == 'POST':
        QuestionForm = QuestionManagement(request.POST, request.FILES)
        print(QuestionForm)
        if QuestionForm.is_valid():
            QF = QuestionForm.save(commit=False)
            QF.status = False
            QF.owner = request.user.id
            QF.postedtime = date.today()
            QF.save()
            messages.success(
                request, 'Your Question  is submited ')
            QuestionForm = QuestionManagement(None)
        else:
            messages.warning(request, QuestionForm.errors)
    else:
        QuestionForm = QuestionManagement()

    context = {'StudentData': userdata, 'categorydata': categorydata,
               'QuestionForm': QuestionForm, 'questiondata': questiondata}
    return render(request, 'teacher/addquestion1.html', context)


        


 
@login_required(login_url='signin')
def allquestion(request):
    if not request.user.status:
        return render(request, 'common/notActive.html')

    userdata = User.objects.get(pk=request.user.id)
    questiondata = Question.objects.all()
    try:
        questiondata = Question.objects.all()
    except Question.DoesNotExist:
        questiondata = None

    AllQuestion = []
    if questiondata is not None:
        for QD in questiondata:
            user = User.objects.filter(pk=QD.owner).first()
            category = QuestionCategory.objects.get(pk=QD.questioncategory)

            if user is not None:
                author = user.first_name + ' ' + user.last_name
                img = user.profilepic.url
            else:
                author = ""

            if category is not None:
                catname = category.name
            else:
                catname = ""

            AllQuestion.append({
                "id": QD.id,
                "question": QD.question,
                "questioncategory": QD.questioncategory,
                'categoryname': catname,
                'owner': QD.owner,
                'ownername': author,
                'ownerimg': img,
                "postedtime": QD.postedtime,
            })

    context = {'StudentData': userdata, 'questiondata': AllQuestion}
    return render(request, 'student/allquestion.html', context)

@login_required(login_url='signin')
def allquestion1(request):
    if not request.user.status:
        return render(request, 'common/notActive.html')

    userdata = User.objects.get(pk=request.user.id)
    questiondata = Question.objects.all()
    try:
        questiondata = Question.objects.all()
    except Question.DoesNotExist:
        questiondata = None

    AllQuestion = []
    if questiondata is not None:
        for QD in questiondata:
            user = User.objects.filter(pk=QD.owner).first()
            category = QuestionCategory.objects.get(pk=QD.questioncategory)

            if user is not None:
                author = user.first_name + ' ' + user.last_name
                img = user.profilepic.url
            else:
                author = ""

            if category is not None:
                catname = category.name
            else:
                catname = ""

            AllQuestion.append({
                "id": QD.id,
                "question": QD.question,
                "questioncategory": QD.questioncategory,
                'categoryname': catname,
                'owner': QD.owner,
                'ownername': author,
                'ownerimg': img,
                "postedtime": QD.postedtime,
            })

    context = {'StudentData': userdata, 'questiondata': AllQuestion}
    return render(request, 'teacher/allquestion1.html', context)


@login_required(login_url='signin')
def answersubmit1(request,pk,fk):
    if not request.user.status:
        return render(request, 'common/notActive.html')
    userdata = User.objects.get(pk=request.user.id)
    QuestionData=Question.objects.get(pk=pk)
    QuestionOwnerData=User.objects.get(pk=fk)
    AnswerData=Answer.objects.filter(questionid=pk)
    AllAnswer = []
    for AD in AnswerData:
            user = User.objects.get(pk=AD.solver)
            if user is not None:
                author = user.first_name + ' ' + user.last_name
                img = user.profilepic
            else:
                author = ""

            AllAnswer.append({
                "answer": AD.answer,
                "answertime": AD.answertime,
                'ownername': author,
                'ownerimg': img,
            })

    
    
    if request.method == 'POST':
        AnswerForm = AnswerManagement(request.POST)
        if AnswerForm.is_valid():
            answer = AnswerForm.save(commit=False)
            answer.questionid =pk
            answer.solver = request.user.id
            answer.answertime = date.today()
            answer.status=True
            answer.save()
            messages.success(
                request, 'Your Answer is Submited')
            return redirect('answersubmit1',pk=pk,fk=fk)
            #return HttpResponseRedirect('/answersubmit/%pk%fk')
        else:
            messages.warning(request, AnswerForm.errors)
    else:
         AnswerForm = AnswerManagement()
    
    context = {'StudentData': userdata,'QuestionData':QuestionData,'AnswerForm':AnswerForm,'QuestionOwnerData':QuestionOwnerData,'AllAnswer':AllAnswer}
    return render(request, 'teacher/questiondetails1.html', context)
    
@login_required(login_url='signin')
def answersubmit(request,pk,fk):
    if not request.user.status:
        return render(request, 'common/notActive.html')
    userdata = User.objects.get(pk=request.user.id)
    QuestionData=Question.objects.get(pk=pk)
    QuestionOwnerData=User.objects.get(pk=fk)
    AnswerData=Answer.objects.filter(questionid=pk)
    AllAnswer = []
    for AD in AnswerData:
            user = User.objects.get(pk=AD.solver)
            if user is not None:
                author = user.first_name + ' ' + user.last_name
                img = user.profilepic
            else:
                author = ""

            AllAnswer.append({
                "answer": AD.answer,
                "answertime": AD.answertime,
                'ownername': author,
                'ownerimg': img,
            })

    
    
    if request.method == 'POST':
        AnswerForm = AnswerManagement(request.POST)
        if AnswerForm.is_valid():
            answer = AnswerForm.save(commit=False)
            answer.questionid =pk
            answer.solver = request.user.id
            answer.answertime = date.today()
            answer.status=True
            answer.save()
            messages.success(
                request, 'Your Answer is Submited')
            return redirect('answersubmit',pk=pk,fk=fk)
            #return HttpResponseRedirect('/answersubmit/%pk%fk')
        else:
            messages.warning(request, AnswerForm.errors)
    else:
         AnswerForm = AnswerManagement()
    
    context = {'StudentData': userdata,'QuestionData':QuestionData,'AnswerForm':AnswerForm,'QuestionOwnerData':QuestionOwnerData,'AllAnswer':AllAnswer}
    return render(request, 'student/questiondetails.html', context)
    
