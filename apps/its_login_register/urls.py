from django.urls import path
from . import views 
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.success),
    path('addJob', views.add),
    path('view/<int:job_id>',views.show),
    path('edit/<int:job_id>',views.edit),
    path('destroy/<int:job_id>', views.delete),
    path('record/<int:job_id>/<int:user_id>', views.record),
    
]
