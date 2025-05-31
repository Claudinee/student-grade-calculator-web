from flask import Blueprint, render_template, request, abort, send_file
from xhtml2pdf import pisa
import io

main = Blueprint('main', __name__)

def calculate_grade(avg):
    if not 0 <= avg <= 100:
        raise ValueError("Average score must be between 0 and 100")
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
    if request.method == 'POST':
        try:
            student_name = request.form.get("student_name")
            course = request.form.get("course")

            # Convert inputs to floats, default 0 if empty or missing
            assignment1 = float(request.form.get("assignment1", 0) or 0)
            assignment2 = float(request.form.get("assignment2", 0) or 0)
            cat1 = float(request.form.get("cat1", 0) or 0)
            cat2 = float(request.form.get("cat2", 0) or 0)
            lab = float(request.form.get("lab", 0) or 0)
            exam = float(request.form.get("exam", 0) or 0)

            # Validate score ranges
            scores_list = [assignment1, assignment2, cat1, cat2, lab, exam]
            if any(score < 0 or score > 100 for score in scores_list):
                raise ValueError("Each score must be between 0 and 100")

            total_score = sum(scores_list)
            average = total_score / len(scores_list)
            grade = calculate_grade(average)

            scores = {
                'Assignment 1': assignment1,
                'Assignment 2': assignment2,
                'CAT 1': cat1,
                'CAT 2': cat2,
                'Lab / Practique': lab,
                'Final Exam': exam
            }

            return render_template("results.html", 
                                   student_name=student_name,
                                   course=course,
                                   scores=scores,
                                   average=average,
                                   grade=grade)
        except ValueError as e:
            return render_template("index.html", error=str(e))
        except Exception:
            abort(500)
    return render_template("index.html")

@main.route('/download-pdf', methods=['POST'])
def download_pdf():
    student_name = request.form.get("student_name")
    course = request.form.get("course")
    total_score = request.form.get("total_score")
    grade = request.form.get("grade")

    rendered_html = render_template("pdf_template.html", 
                                    student_name=student_name,
                                    course=course,
                                    total_score=total_score,
                                    grade=grade)

    pdf = io.BytesIO()
    pisa.CreatePDF(io.StringIO(rendered_html), dest=pdf)
    pdf.seek(0)

    return send_file(pdf, as_attachment=True, download_name="grade_report.pdf")
