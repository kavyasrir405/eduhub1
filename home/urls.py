from django.contrib import admin
from django.urls import path,include

from home import views
from .views import teaching

urlpatterns = [
   
    path('',views.login_user,name="login" ),
    path('home',views.home,name="home" ),
    path('register',views.register,name="register" ),
    path('teaching/<str:course_idee>/', teaching, name='teaching'),

    path('teaching/', teaching, name='teaching_no_id'),

    path('upload',views.upload,name='upload'),
path('profile',views.profile,name='profile'),


     path('course_details/<str:course_idee>/', views.course_details, name='course_details'),
     path('payment', views.payment, name='payment'),

    path('learning',views.learning,name='learning'),
    path('instruct_feedback',views.instruct_feedback,name="instruct_feedback"),
    path('cart',views.cart,name='cart'),
path('question',views.question,name='question'),
    path('add_to_cart/<str:course_idee>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<str:course_idee>/', views.remove_from_cart, name='remove_from_cart'),
  
    path('feedback/<str:courses_id>/', views.feedback, name='feedback'),
    path('feedback', views.feedback, name='feedbackno'),
    
   
    path('signout',views.signout,name='signout'),
    path('development/<str:cat>/',views.category,name='development'),
    path('finance/<str:cat>/',views.category,name='finance'),
    path('fitness/<str:cat>/',views.category,name='fitness'),
    path('lifestyle/<str:cat>/',views.category,name='lifestyle'),
    path('design/<str:cat>/',views.category,name='design'),
    path('music/<str:cat>/',views.category,name='music'),
    path('buisness/<str:cat>/',views.category,name='buisness'),


    path('photography/<str:cat>/',views.category,name='photography'),
    path('answer/<str:ques_id>/', views.answer, name='answer'),


   



]