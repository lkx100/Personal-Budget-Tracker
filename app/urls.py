# app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page for viewing expenses
    path('login_page/', views.login_page, name="login_page"),
    path('signup_page/', views.signup_page, name="signup_page"),
    path('graphs/', views.graphs, name="graphs"),
    path('logout_page/', views.logout_page, name="logout_page"),
    path('add-expense/', views.add_expense, name='add_expense'),  # Page for adding an expense
    path('set-weekly-goal/', views.set_weekly_goal, name='set_weekly_goal'),  # Set weekly goal
]
