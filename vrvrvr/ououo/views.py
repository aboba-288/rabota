import pandas as pd
from django.shortcuts import render


def title(request):
    return render(request, 'title.html')

def salary(request):
    df=pd.read_csv("salary.csv")
    salary=df.to_html(classes='table table-striped',index=False)
    return render(request, 'salary.html',{'salary':salary})

def geography(request):
#    df = pd.read_csv(".csv")
    return render(request, 'geography.html',{'df':df})

def skills(request):
    df = pd.read_csv("топ-15 ключевых навыков.csv")
    skills = df.to_html(classes='table table-striped', index=False)
    return render(request, 'skills.html',{'skills':skills})