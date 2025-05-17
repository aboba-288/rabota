import pandas as pd
from django.shortcuts import render


def title(request):
    return render(request, 'title.html')

def salary(request):
    df=pd.read_csv("salary.csv")
    return render(request, 'salary.html',{'df':df})

def geography(request):
    df = pd.read_csv(".csv")
    return render(request, 'geography.html',{'df':df})

def skills(request):
    df = pd.read_csv("топ-15 ключевых навыков.csv")
    return render(request, 'skills.html',{'df':df})