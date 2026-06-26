from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()


def create_pdf(filename, user, plan, analytics):

    pdf = SimpleDocTemplate(filename)

    story = []

    story.append(Paragraph("<b>FitGen AI Report</b>", styles["Heading1"]))

    story.append(Paragraph(f"Name : {user.name}", styles["BodyText"]))
    story.append(Paragraph(f"Age : {user.age}", styles["BodyText"]))
    story.append(Paragraph(f"Height : {user.height} cm", styles["BodyText"]))
    story.append(Paragraph(f"Weight : {analytics['weight']} kg", styles["BodyText"]))
    story.append(Paragraph(f"Goal : {user.goal}", styles["BodyText"]))

    story.append(Paragraph("<br/>", styles["BodyText"]))

    story.append(Paragraph("<b>Fitness Analytics</b>", styles["Heading2"]))

    story.append(Paragraph(f"BMI : {analytics['bmi']}", styles["BodyText"]))
    story.append(Paragraph(f"Calories : {analytics['calories']}", styles["BodyText"]))
    story.append(Paragraph(f"Protein : {analytics['protein']} g", styles["BodyText"]))
    story.append(Paragraph(f"Water : {analytics['water']} L", styles["BodyText"]))

    story.append(Paragraph("<br/>", styles["BodyText"]))

    story.append(Paragraph("<b>Workout Plan</b>", styles["Heading2"]))

    for day, exercises in plan["workout"].items():

        story.append(Paragraph(f"<b>{day}</b>", styles["Heading3"]))

        for exercise in exercises:
            story.append(Paragraph("• " + exercise, styles["BodyText"]))

    story.append(Paragraph("<br/>", styles["BodyText"]))

    story.append(Paragraph("<b>Diet Plan</b>", styles["Heading2"]))

    for meal, food in plan["diet"].items():

        story.append(Paragraph(f"<b>{meal}</b>", styles["Heading3"]))
        story.append(Paragraph(food, styles["BodyText"]))

    pdf.build(story)