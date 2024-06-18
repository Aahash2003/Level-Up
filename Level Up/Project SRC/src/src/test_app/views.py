from django.shortcuts import render, HttpResponse
from django.db import connections
from django.utils import timezone  
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from datetime import datetime
from django.db import connection


def create_user(request):
    if request.method == 'POST':
        # Collect form data
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        height = request.POST.get('height')
        weight = request.POST.get('weight')

        # Use raw SQL insert statement to create a new user
        with connections['default'].cursor() as cursor:
            try:
                cursor.execute("""
                    INSERT INTO User (username, password, name, email, gender, age, height, weight)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, [username, password, name, email, gender, age, height, weight])
            except Exception as e:
                return HttpResponse(f"Error creating user: {str(e)}", status=500)

            return HttpResponse(f"User {username} created successfully.")

    return HttpResponse("Invalid request method.")

def home(request):
    return render(request, "homepage.html")



def create_user_profile(request):
    return render(request, "create_user_profile.html")

def fitness_goals(request):
    return render(request, "fitnessGoals.html")

def calorie_intake(request):
    return render(request, "calorie_intake.html")

def workout_tracker(request):
    exercises = viewExercise(request)  # Call viewExercise to fetch exercises
    return render(request, "trackworkout.html", {'exercises': exercises})

def userProfile(request):
    return render(request, "create_user_profile.html")


def bmi_calculator(request):
    return render(request, "bmi.html")

def view_userUpdate(request):
    return render(request, "updateUser.html")
    
def viewExercise(request):
    with connections['default'].cursor() as cursor:
        cursor.execute("""
            SELECT * FROM Exercise
        """)
        exercises = cursor.fetchall()

    exercises_list = [
        {
            'exerciseName': exercise[0],
            'exerciseDescription': exercise[1],
            'duration': exercise[2],
            'burnedCalories': exercise[3],
            'targetMuscle': exercise[4],
            
        }
        for exercise in exercises
    ]

    return exercises_list

def get_goal_ids(request):
    if request.method == 'GET':
        username = request.GET.get('username', '')

        with connections['default'].cursor() as cursor:
            cursor.execute("SELECT goal_id FROM FitnessGoal WHERE Username = %s", [username])
            ids = cursor.fetchall()

        id_list = [goal_id[0] for goal_id in ids]

        return JsonResponse({'goal_ids': id_list})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def create_workout(request):
    if request.method == "POST":
        username = request.POST.get('username')
        workout_date = request.POST.get('workoutDate')
        exercise_name = request.POST.get('exerciseName')
        reps = request.POST.get('reps')
        sets = request.POST.get('sets')

        # Use raw SQL insert statements
        with connections['default'].cursor() as cursor:
            # Get the workout_ID for the new Workout
            cursor.execute("""
                SELECT COALESCE(MAX(workout_ID), 0) + 1 FROM Workout
            """)
            workout_id = cursor.fetchone()[0]

            # Create Workout
            cursor.execute("""
                INSERT INTO Workout (workout_ID, date, username)
                VALUES (%s, %s, %s)
            """, [workout_id, workout_date, username])

            # Create WorkoutComponent
            cursor.execute("""
                INSERT INTO WorkoutComponent (reps, sets, workout_ID, exerciseName)
                VALUES (%s, %s, %s, %s)
            """, [reps, sets, workout_id, exercise_name])

        return HttpResponse(f"Workout created for user {username} on {workout_date} with exercise {exercise_name}.")

    return HttpResponse("Invalid request method.")


def view_workouts(request):
    if request.method == "POST":
        username = request.POST.get('username')

        # Use raw SQL select statement with a JOIN
        with connections['default'].cursor() as cursor:
            cursor.execute("""
                SELECT w.workout_ID, w.date, w.username, wc.reps, wc.sets, wc.exerciseName
                FROM Workout w
                JOIN WorkoutComponent wc ON w.workout_ID = wc.workout_ID
                WHERE w.username = %s
            """, [username])

            workouts = cursor.fetchall()

        # Convert workouts to a list of dictionaries
        workouts_list = []
        current_workout = None

        for workout in workouts:
            if not current_workout or current_workout['workout_ID'] != workout[0]:
                # New workout entry
                current_workout = {
                    'workout_ID': workout[0],
                    'date': workout[1],
                    'username': workout[2],
                    'exercises': [],
                }
                workouts_list.append(current_workout)

            # Add exercise details to the current workout
            exercise_details = {
                'reps': workout[3],
                'sets': workout[4],
                'exerciseName': workout[5],
            }
            current_workout['exercises'].append(exercise_details)

        # Pass the workouts directly to the template
        return render(request, "trackworkout.html", {'workouts': workouts_list})

    return HttpResponse("Invalid request method.")



def delete_workout(request):
    if request.method == "POST":
        workout_id = request.POST.get('deleteWorkoutID')

        # Use raw SQL delete statements to handle cascading delete
        with connections['default'].cursor() as cursor:
            try:
                cursor.execute("""
                    DELETE FROM WorkoutComponent
                    WHERE workout_ID = %s
                """, [workout_id])

                cursor.execute("""
                    DELETE FROM Workout
                    WHERE workout_ID = %s
                """, [workout_id])

                return HttpResponse(f"Workout with ID {workout_id} deleted.")
            except Exception as e:
                return HttpResponse(f"Error deleting workout: {e}")

    return HttpResponse("Invalid request method.")

def calculate_average(request):
    if request.method == "POST":
        username = request.POST.get('username')

        # Use raw SQL aggregate function for average
        with connections['default'].cursor() as cursor:
            cursor.execute("""
                SELECT AVG(e.burnedCalories) as avg_calories
                FROM Workout w
                JOIN WorkoutComponent wc ON w.workout_ID = wc.workout_ID
                JOIN Exercise e ON wc.exerciseName = e.exerciseName
                WHERE w.username = %s
            """, [username])

            result = cursor.fetchone()

            if result and result[0] is not None:
                avg_calories = result[0]
                return HttpResponse(f"Average burned calories for user {username}: {avg_calories}.")
            else:
                return HttpResponse(f"No data found for user {username}.")

    return HttpResponse("Invalid request method.")


def create_goal(request):
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST.get('username')
        description = request.POST.get('description')
        desired_weight = request.POST.get('desired_weight')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Calculate duration based on start and end date
        start_date = timezone.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = timezone.datetime.strptime(end_date, "%Y-%m-%d").date()
        duration = (end_date - start_date).days

        with connections['default'].cursor() as cursor:
            # Get the goal_ID for the new FitnessGoal
            cursor.execute("""
                SELECT COALESCE(MAX(goal_ID), 0) + 1 FROM FitnessGoal
            """)
            goal_id = cursor.fetchone()[0]

            # Insert new FitnessGoal using raw SQL
            cursor.execute("""
                INSERT INTO FitnessGoal (goal_ID, username, description, weight, startDate, endDate, duration, succeeded)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, [goal_id, username, description, desired_weight, start_date, end_date, duration, False])

        return HttpResponse(f'Goal Created for {username}')

    else:
        return HttpResponse("Invalid request", status=400)
    


def update_user(request):
    if request.method == 'POST':
        # Collect form data
        username = request.POST.get('username')
        new_weight = request.POST.get('weight')
        new_height = request.POST.get('height')

        if not username:
            return HttpResponse('Username is required', status=400)

        with connections['default'].cursor() as cursor:
            # Check if the user exists in the User table
            cursor.execute("SELECT username FROM user WHERE username = %s", [username])
            if cursor.fetchone() is None:
                # Return an error if the user doesn't exist
                return HttpResponse('User not found', status=404)

            # Update the user's weight and height
            try:
                cursor.execute("""
                    UPDATE User
                    SET weight = %s, height = %s
                    WHERE username = %s
                """, [new_weight, new_height, username])
            except Exception as e:
                return HttpResponse(f'Error updating user: {str(e)}', status=500)

            return HttpResponse('User updated successfully')

    return HttpResponse('Invalid request method', status=405)


def get_workout_ids(request):
    if request.method == 'GET':
        username = request.GET.get('username', '')

        # Fetch workout IDs based on the username
        query = """
            SELECT DISTINCT workout_ID
            FROM Workout
            WHERE username = %s
        """
        params = [username]

        with connections['default'].cursor() as cursor:
            cursor.execute(query, params)
            workout_ids = cursor.fetchall()

        # Convert workout IDs to a list
        ids_list = [workout_id[0] for workout_id in workout_ids]

        # Return JSON response
        return JsonResponse({'workout_ids': ids_list})

    return HttpResponse('Internal Error')


def calculate_bmi(request):
    if request.method == 'POST':
        # Collect form data
        username = request.POST.get('username')

        # Use raw SQL to calculate BMI
        with connections['default'].cursor() as cursor:
            cursor.execute("""
                SELECT username, weight, height, weight / POWER(height / 100, 2) AS bmi
                FROM User
                WHERE username = %s
            """, [username])

            result = cursor.fetchone()

            if result:
                username = result[0]
                weight = result[1]
                height = result[2]
                bmi = result[3]

                # Determine BMI category
                if bmi < 18.5:
                    bmi_category = 'Low body weight. You need to gain weight by eating moderately.'
                elif bmi < 24.9:
                    bmi_category = 'The standard of good health.'
                elif bmi < 29.9:
                    bmi_category = 'Excess body weight. Exercise needs to reduce excess weight.'
                elif bmi < 34.9:
                    bmi_category = 'The first stage of obesity. It is necessary to choose food and exercise.'
                elif bmi < 39.9:
                    bmi_category = 'The second stage of obesity. Moderate diet and exercise are required.'
                else:
                    bmi_category = 'Excess fat. Fear of death. Need a doctor\'s advice.'

                return JsonResponse({
                    'status': 'success',
                    'message': f'Calculated BMI for {username}: {bmi:.2f}',
                    'bmi_category': bmi_category
                })
            else:
                return JsonResponse({'status': 'error', 'message': f'User {username} not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


def view_goals(request):
    if request.method == 'GET':
        # Get the username from the query parameters
        username = request.GET.get('username', '')

        # Fetch goals based on the username
        query = """
            SELECT description, weight, startDate, endDate, succeeded
            FROM FitnessGoal
            WHERE username = %s
        """
        params = [username]

        with connections['default'].cursor() as cursor:
            cursor.execute(query, params)
            goals = cursor.fetchall()

        # Convert goals to a list of dictionaries
        goals_list = [
            {
                'description': goal[0],
                'weight': goal[1],
                'startDate': goal[2].strftime('%Y-%m-%d'),
                'endDate': goal[3].strftime('%Y-%m-%d'),
                'succeeded': goal[4],
            }
            for goal in goals
        ]

        # Return JSON response
        return JsonResponse({'goals': goals_list})

    # If the request method is not GET, render the empty form
    return HttpResponse('Internal Error')


def execute_query(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return data



def modify_goal(request):
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST['username']
        goal_id = request.POST.get('goal_id', '')
        succeeded_str = request.POST['succeeded']

        # Convert 'succeeded' to a string ('yes' or 'no')
        succeeded = succeeded_str.lower() == 'true'

        # Debugging output
        print(f"Request data - username: {username}, goal_id: {goal_id}, succeeded: {succeeded}")

        # Perform the database update using raw SQL
        query = """
            UPDATE FitnessGoal
            SET succeeded = %s
            WHERE username = %s AND goal_ID = %s
        """
        params = [succeeded, username, goal_id]

        with connections['default'].cursor() as cursor:
            cursor.execute(query, params)

        # Debugging output
        print(f"Rows affected: {cursor.rowcount}")

        # Redirect to a success page or another appropriate location
        return JsonResponse({'message': f'Fitness goal is now {succeeded}'})

    # Handle other HTTP methods if needed
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def add_entry(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Extract data from the request
            username = data['username']
            entry_date = datetime.strptime(data['date'], '%Y-%m-%d')
            calories = data['calories']
            carbs = data['carbs']
            protein = data['protein']
            fats = data['fats']

            with connection.cursor() as cursor:
                # Check if user exists in User table
                cursor.execute("SELECT username FROM user WHERE username = %s", [username])
                if cursor.fetchone() is None:
                    # Return an error if the user doesn't exist
                    return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

                # Insert the CalorieIntake entry
                insert_sql = """
                    INSERT INTO CalorieIntake (username, date, calories, carbsConsumed, proteinConsumed, fatsConsumed) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_sql, [username, entry_date, calories, carbs, protein, fats])

            return JsonResponse({'status': 'success', 'message': 'Entry added successfully'})

        except KeyError as e:
            return JsonResponse({'status': 'error', 'message': f'Missing data: {e}'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)


@csrf_exempt
def get_entries(request):
    if request.method == 'GET':
        try:
            username = request.GET.get('username', None)

            if username is not None:
                # Raw SQL to fetch CalorieIntake entries for a specific username
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT username, date, calories, carbsConsumed, proteinConsumed, fatsConsumed "
                        "FROM CalorieIntake WHERE username = %s",
                        [username]
                    )
                    entries = cursor.fetchall()

                # Convert the result to a list of dictionaries
                entries_list = [
                    {
                        "username": entry[0],
                        "date": entry[1].strftime('%Y-%m-%d'),
                        "calories": entry[2],
                        "carbsConsumed": entry[3],
                        "proteinConsumed": entry[4],
                        "fatsConsumed": entry[5]
                    } for entry in entries
                ]

                return JsonResponse({'status': 'success', 'data': entries_list})
            else:
                return JsonResponse({'status': 'error', 'message': 'Username parameter is missing'}, status=400)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)
