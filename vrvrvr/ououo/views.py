from django.shortcuts import render


def title(request):
    return render(request, 'title.html', {'title':title})

def salary(request):
    return render(request, 'salary.html')

def geography(request):
    return render(request, 'geography.html')

def skills(request):
    return render(request, 'skills.html')