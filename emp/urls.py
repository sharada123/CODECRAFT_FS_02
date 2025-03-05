from django.urls import path
from .import views
from .views import employee_list,employee_create,employee_delete,employee_update,login_view,logout_view,register,employee_dashboard
urlpatterns = [
   path('',employee_list,name='employee_list'),
   path('employee_dashboard',employee_dashboard, name='employee_dashboard'),
   path('create/',employee_create,name='employee_create'),
   path('delete/<int:id>',employee_delete,name='employee_delete'),
   path('update/<int:id>',employee_update,name='employee_update'),  # add this line
   path('register',register,name='register'),
   path('login',login_view,name='login'),
   path('logout',logout_view,name='logout'),
]
