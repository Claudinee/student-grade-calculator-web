from flask import Blueprint, render_template, request, abort

main = Blueprint('main', __name__)

def calculate_grade(avg):
    """
    Calculates the grade based on the average score.

    Args:
        avg (float): The average score.

    Returns:
        str: The corresponding grade (A, B, C, D, or F).
    """
    if not 0 <= avg <= 100:
        raise ValueError("Average score must be between 0 and 100")  # Added validation here
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

@main.route('/', methods=['GET', 'POST'])
def index():
    """
    Handles the input of student scores and displays the results.
    """
    if request.method == 'POST':
        try:
            scores = [float(request.form.get(f"score{i}")) for i in range(1, 6)]
            if any(not 0 <= score <= 100 for score in scores):
                raise ValueError("Each score must be between 0 and 100")
            average = sum(scores) / len(scores)
            grade = calculate_grade(average)  # Use the function for calculation
            return render_template("results.html", scores=scores, average=average, grade=grade)
        except ValueError as e:
            return render_template("index.html", error=str(e))  # Return the error message
        except Exception:
            abort(500) # Internal Server Error for unexpected errors
    return render_template("index.html")
