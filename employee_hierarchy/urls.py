from django.contrib import admin
from django.urls import path
from employees.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('', employee_hierarchy, name='employee_hierarchy'),
    path('employee-list/', employee_list, name='employee_list'),
    path('search/', employee_search, name='employee_search'),
    path('sort-employees/', sort_employees, name='sort_employees'),
    path('employee_create/', employee_create, name='employee_create'),
    path('employee_detail/<int:pk>/', employee_detail, name='employee_detail'),
    path('employee_update/<int:pk>/', employee_update, name='employee_update'),
    path('employee_delete/<int:pk>/', employee_delete, name='employee_delete'),
    path('load-subordinates/', load_subordinates, name='load_subordinates'),
    path('load-more-employees/', load_more_employees, name='load_more_employees'),
]
