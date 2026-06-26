def calculate_bmi(height_cm, weight):

    if height_cm is None or weight is None:
        return 0

    if height_cm == 0:
        return 0

    height = height_cm / 100

    bmi = weight / (height * height)

    return round(bmi, 1)


def bmi_status(bmi):

    if bmi == 0:
        return "Unknown"

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal"

    elif bmi < 30:
        return "Overweight"

    return "Obese"


def calories(weight, goal):

    if weight is None:
        return 0

    maintenance = weight * 33

    if goal == "Weight Gain":
        maintenance += 350

    elif goal == "Weight Loss":
        maintenance -= 400

    return int(maintenance)


def protein(weight):

    if weight is None:
        return 0

    return round(weight * 1.8)


def water(weight):

    if weight is None:
        return 0

    return round(weight * 0.04, 1)