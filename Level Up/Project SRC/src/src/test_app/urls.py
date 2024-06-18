from django.urls import path
from . import views

urlpatterns = [
    #Home
    path('', views.home, name='home'),  
    
    #Workout Tracker
    path('workout_tracker/', views.workout_tracker, name='workout_tracker'),  
    path('create_workout/', views.create_workout, name='create_workout'),
    path('view_workouts/', views.view_workouts, name='view_workouts'),
    path('delete_workout/', views.delete_workout, name='delete_workout'),
    path('calculate_average/', views.calculate_average, name='calculate_average'),

    #Create User
    path('create_user_profile/', views.create_user_profile, name='create_user_profile'), 
    path('create-profile/', views.create_user, name='create_profile'),

    #Create Fitness Goal
    path('fitness_goals/', views.fitness_goals, name='fitness_goals'), 
    path('create_goal/', views.create_goal, name='create_goal'),
    path('view_goals/', views.view_goals, name='view_goals'),
    path('modify_goal/', views.modify_goal, name='modify_goal'),
    path('get_goal_ids/', views.get_goal_ids, name='get_goal_ids'),



    #Calorie Intake
    path('calorie_intake/', views.calorie_intake, name='calorie_intake') ,
    path('add_entry/', views.add_entry, name='add_entry'),
    path('get_entries/', views.get_entries, name='get_entries'),

    #BMI Intake
    path('bmi_calculator/', views.bmi_calculator, name='bmi_calculator') ,
    path('calculate_bmi/',views.calculate_bmi, name='calculate_bmi' ),

    #update user
    path('view_userUpdate/', views.view_userUpdate, name='view_userUpdate') ,
    path('update_user', views.update_user, name='update_user')



]