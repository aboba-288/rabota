from django.urls import path

from .views import *

urlpatterns = [
    path('', title, name='title'),
    path('salary/', salary, name='salary'),
    path('geography/', geography, name='geography'),
    path('skills/', skills, name='skills'),
]