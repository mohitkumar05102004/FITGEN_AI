def calculate_calories(weight, height, age, gender, activity):
    """
    Mifflin-St Jeor Formula
    """

    if gender == "Male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    activity_factor = {
        "Sedentary": 1.2,
        "Light": 1.375,
        "Moderate": 1.55,
        "Active": 1.725,
        "Very Active": 1.9
    }

    calories = bmr * activity_factor.get(activity, 1.2)

    return round(calories)