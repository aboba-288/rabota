from http.client import responses

import pandas as pd
import matplotlib.pyplot as plt
from django.template.context_processors import request

a=pd.read_csv('vacancies_2024.csv')
b=a[a['name'] == 'Тестировщик']
c=a[a['name'] == 'QA-инженер']
d=a[a['name'] == 'QA-engineer']
ou=pd.concat([b,c])
ouo=pd.concat([ou,d])


def clean_salaries(ouo):
    ouo=ouo.copy()
    ouo['salary_from']=ouo['salary_from'].fillna(ouo['salary_to'])
    ouo['salary_to']=ouo['salary_to'].fillna(ouo['salary_from'])
    ouo=ouo.dropna(subset=['salary_from', 'salary_to'], how='all')

    return ouo

def get_currency_rates():
    try:
        response=request.get('https://www.cbr-xml-daily.ru/daily_json.js')
        data=response.json()
        rates={
            'RUR':1,
            'USD': data['Valute']['USD']['Value'],
            'EUR': data['Valute']['EUR']['Value'],
            'KZT': data['Valute']['KZT']['Value']/100
        }

        return rates
    except Exception as e:
        print(f"ошибка при получении курсов валют: {e}")

        return {
            'RUR': 1,
            'USD': 90,
            'EUR': 100,
            'KZT': 0.18
        }

def analyze_vacancies(filename, keywords):
    try:
        ouo=pd.read_csv('vacancies_2024.csv')
    except Exception as e:
        print(f"ошибка чтения файла: {e}")
        return

    ouo = clean_salaries(ouo)
    ouo = ouo.dropna(subset=['name'])

    pattern = '|'.join(keywords)
    uou = ouo[ouo['name'].str.contains(pattern, case=False, regex=True, na=False)]

    if len(uou) == 0:
        print("Нет вакансий, соответствующих критериям")
        return

    currency_rates = get_currency_rates()

    uou['salary'] = uou.apply(
        lambda row: calculate_salary(row, currency_rates),
        axis=1
    ).dropna()

    uou['published_at'] = ouo.apply(
        lambda row: int(row['published_at'][0:4]),
        axis=1
    ).dropna()


    print(
        f"Найдено {len(uou)} вакансий за период {uou['published_at'].min()}-{uou['published_at'].max()}")
    print(f"Средняя зарплата: {uou['salary'].mean():.2f} руб")
    print(f"Медианная зарплата: {uou['salary'].median():.2f} руб")


    plot_top_cities_by_year(uou)
    plot_salaries(uou)
    plot_skills(uou)

def calculate_salary(row, currency_rates):
    if pd.isna(row['salary_from']) and pd.isna(row['salary_to']):
        return None
    salary = (row['salary_from'] + row['salary_to']) / 2
    return salary * currency_rates.get(row['salary_currency'], 1)

def plot_top_cities_by_year(df, top_n=10):
    years = sorted(df['published_at'].unique())

    for year in years:
        year_data = df[df['published_at'] == year]
        if len(year_data) == 0:
            continue

        cities = year_data['area_name'].value_counts().head(top_n)

        if len(cities) == 0:
            continue

        plt.figure(figsize=(12, 6))
        cities.plot(kind='bar', color='lightblue')
        plt.title(f'Топ-{top_n} городов по вакансиям в {year} году', pad=20)
        plt.xlabel('Город')
        plt.ylabel('Количество вакансий')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(f'данные/Топ-{top_n} городов по вакансиям в {year} году.png')


def plot_salaries(df):
    plt.figure(figsize=(12, 6))

    salary_by_year = df.groupby('published_at')['salary'].mean()
    salary_by_year.plot(kind='line', marker='o', label='Средняя зарплата')

    median_by_year = df.groupby('published_at')['salary'].median()
    median_by_year.plot(kind='line', marker='o', label='Медианная зарплата')

    plt.title('Динамика зарплат по годам', pad=20)
    plt.xlabel('Год')
    plt.ylabel('Зарплата (руб)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("данные/зарплата_абобы.png")


def plot_skills(df, top_n=15):
    skills = (
        df['key_skills']
        .str.lower()
        .str.split(r',\s*|[\n]|\s*/\s*', regex=True)
        .explode()
        .str.strip()
        .value_counts()
        .head(top_n)
    )

    plt.figure(figsize=(12, 8))
    skills.plot(kind='barh')
    plt.title(f'Топ-{top_n} ключевых навыков', pad=20)
    plt.xlabel('Количество упоминаний')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig("данные/навыки_абобы.png")

if __name__ == "__main__":
    keywords = ["Тестировщик", "QA-инженер", "QA-engineer"]
    analyze_vacancies('vacancies_2024.csv', keywords)