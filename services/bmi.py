def calculate_bmi(weight, height):
    """
    weight -> kg
    height -> cm
    """

    if not weight or not height:
        return 0, "Unknown"

    bmi = weight / ((height / 100) ** 2)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    return round(bmi, 2), category