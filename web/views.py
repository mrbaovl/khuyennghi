from collections import Counter

import joblib
import numpy as np
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.db.models import Q
from django.shortcuts import render, redirect

from .forms import UserForm
from .models import Student, Course

# ignore divide by zero or divide by NaN
np.seterr(divide='ignore', invalid='ignore')


def index(request):
    return render(request, 'web/index.html')


def statistics(request):
    return render(request, 'web/statistics.html')


def evaluation(request):
    model = joblib.load('./web/model/Model_CB.sav')
    rsme = model.evaluate_RMSE()
    mae = model.evaluate_MAE()
    mse = model.evaluate_MSE()
    return render(request, 'web/evaluation.html', {'rsme': rsme, 'mae': mae, 'mse': mse})


def evaluation_results(request):
    model = joblib.load('./web/model/Model_CB.sav')
    rsme = model.evaluate_RMSE()
    mae = model.evaluate_MAE()
    mse = model.evaluate_MSE()
    return rsme, mae, mse


def data(request):
    model = joblib.load('./web/model/Model_CB.sav')
    list_data = []
    vmlist = []
    for x in range(0, 32):
        ids = np.where(model.Y_data[:, 0] == x)[0]
        ids = model.Y_data[ids]
        ids = ids[ids[:, 1].argsort(kind='mergesort')]
        test = model.get_item_null(x)
        rul = np.append(ids[:, 1:], np.asarray(test), axis=0)
        rul = rul[rul[:, 0].argsort(kind='mergesort')]

        for i in rul:
            myvm = i[1]
            vmlist.append(myvm)
    list_data.append(vmlist)
    return list_data


def cb_result(request, ):
    model = joblib.load('./web/model/Model_CB.sav')
    list_data = []
    vmlist = []
    for x in range(0, 32):
        test = model.get_result_item(x)
        for i in test:
            myvm = i[1]
            vmlist.append(myvm)
    list_data.append(vmlist)
    return list_data


def predict_all(request):
    model = joblib.load('./web/model/Model_CB.sav')
    global data
    list_data = []
    vmlist = []
    for x in range(0, 32):
        ids = model.null_rated_item(x)
        ids = np.array(ids)
        ids = ids[ids[:, 1].argsort(kind='mergesort')]
        test = model.pred_for_user(x)
        data = np.append(ids, np.asarray(test), axis=0)
        data = data[data[:, 0].argsort(kind='mergesort')]
        for i in data:
            myvm = i[1]
            vmlist.append(myvm)
    list_data.append(vmlist)
    return list_data


# Predict full subject for specfic user
def predict_full(request, student_id):
    model = joblib.load('./web/model/Model_CB.sav')
    # idsv = int(request.json.get('mssv'))
    ids = np.where(model.Y_data[:, 0] == student_id)[0]
    test = model.Y_data[ids]
    data = model.pred_for_user(student_id)
    temp = 0
    for i in test:
        test[temp][2] = -i[2]
        temp += 1
    rul = np.append(test[:, 1:], np.asarray(data), axis=0)
    rul = rul[rul[:, 0].argsort(kind='mergesort')]
    vmlist = []
    for i in rul:
        myvm = i[1]
        vmlist.append(myvm)

    print(vmlist)
    return vmlist


def listCourses(request):
    return render(request, 'web/list.html')


def predict_all_view(request):
    # List Data
    model = joblib.load('./web/model/Model_CB.sav')
    list_data = []
    vmlist = []
    for x in range(0, 32):
        ids = np.where(model.Y_data[:, 0] == x)[0]
        ids = model.Y_data[ids]
        ids = ids[ids[:, 1].argsort(kind='mergesort')]
        test = model.get_item_null(x)
        rul = np.append(ids[:, 1:], np.asarray(test), axis=0)
        rul = rul[rul[:, 0].argsort(kind='mergesort')]

        for i in rul:
            myvm = i[1]
            vmlist.append(myvm)
    print(vmlist)
    list_data.append(vmlist)

    # List CB All
    global datacb
    list_cb = []
    vmlist2 = []
    for x in range(0, 32):
        ids = model.null_rated_item(x)
        ids = np.array(ids)
        ids = ids[ids[:, 1].argsort(kind='mergesort')]
        test = model.pred_for_user(x)
        datacb = np.append(ids, np.asarray(test), axis=0)
        datacb = datacb[datacb[:, 0].argsort(kind='mergesort')]
        for i in datacb:
            myvm = i[1]
            vmlist2.append(myvm)
    list_cb.append(vmlist2)

    list_cb_result = []
    vmlist3 = []
    for x in range(0, 32):
        test = model.get_result_item(x)
        for i in test:
            myvm = i[1]
            vmlist3.append(myvm)
    list_cb_result.append(vmlist3)
    rsme, mae, mse = evaluation_results(request)
    return render(request, 'web/predictAll.html',
                  {'list_data': list_data, 'n': range(1, 53), 'list_cb_all': list_cb,
                   'list_result': list_cb_result, 'rsme': rsme, 'mae': mae, 'mse': mse})


def list_first(request):
    return render(request, 'web/list_first.html')


def recommend(request):
    query = request.GET.get('q')
    if Student.objects.filter(Q(code__contains=query)) and query != "":
        id = Student.objects.filter(Q(code__contains=query)).values('id')[0]['id']
        list_data = predict_full(request, id)
        N = 4
        list_index = sorted(range(len(list_data)), key=lambda sub: list_data[sub])[-N:]
        listOfZeros = [0] * 52
        counter_a = Counter(list_index)
        for key in counter_a:
            for i in range(len(listOfZeros)):
                if key == i:
                    listOfZeros[i] = 1

        list_courses = Course.objects.all()
        list_datas = list(zip(list_data, list_courses, listOfZeros))
        return render(request, 'web/recommend.html', {'list_datas': list_datas})
    return render(request, 'web/list_first.html', {'error_message': 'please enter correct student id format'})


# Register user
def signUp(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("listCourses")
    context = {
        'form': form
    }
    return render(request, 'web/signUp.html', context)


# Login User
def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("listCourses")
            else:
                return render(request, 'web/login.html', {'error_message': 'Your account disable'})
        else:
            return render(request, 'web/login.html', {'error_message': 'Invalid Login'})
    return render(request, 'web/login.html')


# Logout user
def Logout(request):
    logout(request)
    return redirect("login")


if __name__ == "__main__":
    model = joblib.load('./web/model/Model_CB.sav')
