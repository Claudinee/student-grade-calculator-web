from flask import Blueprint, render_template, request

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            scores = [float(request.form.get(f"score{i}")) for i in range(1, 6)]
            average = sum(scores) / len(scores)
            grade = calculate_grade(average)
            return render_template("results.html", scores=scores, average=average, grade=grade)
        except Exception as e:
            return render_template("index.html", error="Please enter valid numeric scores.")
    return render_template("index.html")

def calculate_grade(avg):
    if avg >= 90:
        return 'A'
    elif avg >= 80:
        return 'B'
    elif avg >= 70:
        return 'C'
    elif avg >= 60:
        return 'D'
    else:
        return 'F'
