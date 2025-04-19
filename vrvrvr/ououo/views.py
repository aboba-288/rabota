from django.shortcuts import render


def title(request):
    return render(request, 'title.html', {'title':title})

def salary(request):
    pass

def geography(request):
    pass

def skills(request):
    pass
