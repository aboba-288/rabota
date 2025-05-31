import os.path
import pandas as pd
from django.shortcuts import render

current_dir=os.path.dirname(os.path.abspath(__file__))

def title(request):
    return render(request, 'title.html')

def salary(request):
    file_path=os.path.join(current_dir, 'csv', 'salary.csv')
    df=pd.read_csv(file_path)
    salary=df.to_html(classes='table table-striped',index=False)
    return render(request, 'salary.html',{'salary':salary})

def geography(request):
    file_path = os.path.join(current_dir, 'csv')

    tables_data= []

    for filename in os.listdir(file_path):
        if filename.startswith('Топ-10 городов по вакансиям в ') and filename.endswith('.csv'):
            year = filename.split(' в ')[1].split(' году.csv')[0]
            filepath= os.path.join(file_path, filename)
            df = pd.read_csv(filepath,encoding='utf-8')

            tables_data.append({
                'year': year,
                'title': f'топ-10 городов по вакансиям в {year} году',
                'html_table': df.to_html(
                    classes='table table-striped table-hover',
                    index=False,
                    border=0
                )
            })

    tables_data.sort(key=lambda x: x['year'], reverse=True)
    return render(request, 'geography.html',{'tables':tables_data})

def skills(request):
    file_path = os.path.join(current_dir, 'csv', 'топ-15 ключевых навыков.csv')
    df = pd.read_csv(file_path)
    skills = df.to_html(classes='table table-striped', index=False)
    return render(request, 'skills.html',{'skills':skills})