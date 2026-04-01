import random

# ---------- Exercise Database ----------
exercises_db = {

    "chest": [
        "Bench Press",
        "Incline Dumbbell Press",
        "Cable Fly"
    ],

    "back": [
        "Pull Ups",
        "Barbell Row",
        "Lat Pulldown"
    ],

    "legs": [
        "Squats",
        "Leg Press",
        "Hamstring Curl"
    ],

    "shoulders": [
        "Overhead Press",
        "Lateral Raise",
        "Rear Delt Fly"
    ],

    "arms": [
        "Barbell Curl",
        "Tricep Pushdown",
        "Hammer Curl"
    ],

    "core": [
        "Plank",
        "Crunches",
        "Leg Raises"
    ]
}


# ---------- MAIN FUNCTION ----------
def generate_plan(data):

    # -------- INPUT --------
    age = int(data["age"])
    weight = float(data["weight"])
    height = float(data["height"])
    gender = data["gender"]
    goal = data["goal"]
    bodypart = data["bodypart"].strip().lower()

    # -------- BMI --------
    height_m = height / 100
    bmi = weight / (height_m ** 2)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    # -------- BMR --------
    if gender == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # -------- Calories --------
    if goal == "bulking":
        calories = bmr + 400
    elif goal == "cutting":
        calories = bmr - 400
    else:
        calories = bmr

    # -------- WORKOUT PLAN --------
    workout = []

    # 🎯 Goal-based reps
    if goal == "bulking":
        reps = "4x8"
    elif goal == "cutting":
        reps = "3x15"
    else:
        reps = "3x12"

    # 🔥 FULL BODY MODE
    if bodypart == "full":

        all_parts = list(exercises_db.keys())

        for i in range(14):

            # 🛌 Rest Day
            if i % 7 == 6:
                workout.append({
                    "day": f"Day {i+1}",
                    "bodypart": "Rest",
                    "exercises": ["Rest and Recovery 🛌"]
                })
                continue

            part = all_parts[i % len(all_parts)]

            exercises = [
                ex + " " + reps
                for ex in exercises_db[part]
            ]

            workout.append({
                "day": f"Day {i+1}",
                "bodypart": part.capitalize(),
                "exercises": exercises
            })

    else:

        if bodypart not in exercises_db:
            bodypart = "chest"

        for i in range(14):

            if i % 7 == 6:
                workout.append({
                    "day": f"Day {i+1}",
                    "bodypart": "Rest",
                    "exercises": ["Rest 🛌"]
                })
                continue

            exercises = [
                ex + " " + reps
                for ex in exercises_db[bodypart]
            ]

            workout.append({
                "day": f"Day {i+1}",
                "bodypart": bodypart.capitalize(),
                "exercises": exercises
            })

    # -------- DIET PLAN --------
    if goal == "bulking":
        diet = {
            "Breakfast": ["Oats", "Milk", "Banana", "Peanut Butter"],
            "Lunch": ["Rice", "Chicken", "Eggs"],
            "Dinner": ["Chapati", "Paneer", "Vegetables"]
        }

    elif goal == "cutting":
        diet = {
            "Breakfast": ["Oats", "Egg Whites"],
            "Lunch": ["Brown Rice", "Chicken", "Salad"],
            "Dinner": ["Soup", "Vegetables"]
        }

    else:
        diet = {
            "Breakfast": ["Oats", "Milk"],
            "Lunch": ["Rice", "Dal", "Salad"],
            "Dinner": ["Chapati", "Vegetables"]
        }

    # -------- AI SMART TIPS --------
    if bmi < 18.5:
        ai_tip = "You are underweight. Focus on high-calorie diet and strength training."
    elif bmi > 25:
        ai_tip = "You are overweight. Focus on cardio and calorie deficit diet."
    else:
        ai_tip = "You are in good shape. Maintain balanced diet and regular training."

    # -------- FINAL OUTPUT --------
    return {
        "bmi": round(bmi, 2),
        "category": category,
        "bmr": int(bmr),
        "calories": int(calories),
        "workout": workout,
        "diet": diet,
        "ai_tip": ai_tip
    }