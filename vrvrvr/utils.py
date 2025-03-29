import pandas as pd

a=pd.read_csv('vacancies_2024.csv')
b=a[a['name'] == 'Тестировщик']
c=a[a['name'] == 'QA-инженер']
d=a[a['name'] == 'QA-engineer']
ou=pd.concat([b,c])
ouo=pd.concat([ou,d])
print(ouo[ouo['name'] == 'QA-инженер'])