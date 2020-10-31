from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signUp, name='signup'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('listCourses',views.listCourses,name='listCourses'),
    path('statistics/', views.statistics, name='statistics'),
    path('evaluation/', views.evaluation, name='evaluation'),
    path('predictAll', views.predict_all_view, name='predictAll'),
    path('list_first',views.list_first, name='list_first'),
    path('recommend', views.recommend, name='recommend'),
]
