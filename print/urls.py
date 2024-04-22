


from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('import/', views.import_tickets, name='import_tickets'),
    path('select/', views.import_selected_tickets, name='select_tickets'),
    path('tickets/', views.ticket_list, name='ticket_list'),
    path('clear-session/', views.clear_session, name='clear_session'),
]

