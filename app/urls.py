from django.urls import path
from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('reg/', views.registration, name='reg'),
    path('login/', views.user_login, name='login'),
    path('', views.search, name='search'),
    path('logout/', views.getlogout, name='logout'),
    path('api/', views.get_input_data, name='api'),

]
