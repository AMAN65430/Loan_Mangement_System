
import re
from functools import wraps
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
)
from werkzeug.security import check_password_hash

import database as db

app = Flask(__name__)
app.secret_key = "change-this-secret-key-in-production"  # used to sign session cookies


# ==================================================================
# AUTH DECORATOR
# ==================================================================

def login_required(view_func):
    """Redirects to the login page if no admin is logged in."""
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if "admin_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)
    return wrapped_view


# ==================================================================
# VALIDATION HELPERS
# ==================================================================

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MOBILE_REGEX = re.compile(r"^[6-9]\d{9}$")  # 10-digit mobile number


def validate_loan_form(form):
    """
    Validates every field of the loan application form.
    Returns a tuple: (errors_list, cleaned_data_dict)
    cleaned_data_dict is only reliable when errors_list is empty.
    """
    errors = []
    cleaned = {}

    # --- Full Name ---
    full_name = form.get("full_name", "").strip()
    if not full_name or len(full_name) < 3:
        errors.append("Full name must be at least 3 characters long.")
    cleaned["full_name"] = full_name

    # --- Email ---
    email = form.get("email", "").strip()
    if not EMAIL_REGEX.match(email):
        errors.append("Please enter a valid email address.")
    cleaned["email"] = email

    # --- Mobile Number ---
    mobile_number = form.get("mobile_number", "").strip()
    if not MOBILE_REGEX.match(mobile_number):
        errors.append("Mobile number must be a valid 10-digit Indian number.")
    cleaned["mobile_number"] = mobile_number

    # --- Age ---
    try:
        age = int(form.get("age", ""))
        if age < 21 or age > 65:
            errors.append("Age must be between 21 and 65 to be eligible for a loan.")
    except ValueError:
        age = None
        errors.append("Age must be a valid number.")
    cleaned["age"] = age

    # --- Monthly Income ---
    try:
        monthly_income = float(form.get("monthly_income", ""))
        if monthly_income <= 0:
            errors.append("Monthly income must be greater than zero.")
    except ValueError:
        monthly_income = None
        errors.append("Monthly income must be a valid number.")
    cleaned["monthly_income"] = monthly_income

    # --- Employment Type ---
    employment_type = form.get("employment_type", "").strip()
    if employment_type not in ("Salaried", "Self-Employed"):
        errors.append("Please select a valid employment type.")
    cleaned["employment_type"] = employment_type

    # --- Loan Amount ---
    try:
        loan_amount = float(form.get("loan_amount", ""))
        if loan_amount <= 0:
            errors.append("Loan amount must be greater than zero.")
    except ValueError:
        loan_amount = None
        errors.append("Loan amount must be a valid number.")
    cleaned["loan_amount"] = loan_amount

    # --- Loan Purpose ---
    loan_purpose = form.get("loan_purpose", "").strip()
    if not loan_purpose:
        errors.append("Please provide a loan purpose.")
    cleaned["loan_purpose"] = loan_purpose

    # --- Credit Score ---
    try:
        credit_score = int(form.get("credit_score", ""))
        if credit_score < 300 or credit_score > 900:
            errors.append("Credit score must be between 300 and 900.")
    except ValueError:
        credit_score = None
        errors.append("Credit score must be a valid number.")
    cleaned["credit_score"] = credit_score

    return errors, cleaned


def evaluate_loan_eligibility(credit_score, monthly_income):
    """
    Core business logic for the loan eligibility engine.

    Rules:
        * Credit Score >= 750 AND Income >= 40000  -> Approved
        * Credit Score 650-749 AND Income >= 25000 -> Pending (manual review)
        * Otherwise                                -> Rejected

    Also computes:
        * Risk Level   -> Low / Medium / High
        * Eligible Amount -> Monthly Income x 10

    Returns a dict with keys: status, risk_level, eligible_amount
    """
    if credit_score >= 750 and monthly_income >= 40000:
        status = "Approved"
        risk_level = "Low"
    elif 650 <= credit_score <= 749 and monthly_income >= 25000:
        status = "Pending"
        risk_level = "Medium"
    else:
        status = "Rejected"
        risk_level = "High"

    eligible_amount = monthly_income * 10

    return {
        "status": status,
        "risk_level": risk_level,
        "eligible_amount": eligible_amount,
    }


# ==================================================================
# AUTH ROUTES
# ==================================================================

@app.route("/", methods=["GET"])
def index():
    """Root route redirects to the login page."""
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Admin login page with hashed-password verification."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        admin = db.get_admin_by_username(username)

        if admin and check_password_hash(admin["password_hash"], password):
            session["admin_id"] = admin["id"]
            session["admin_username"] = admin["username"]
            flash(f"Welcome back, {admin['username']}!", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid username or password.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Clears the session and logs the admin out."""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


# ==================================================================
# DASHBOARD
# ==================================================================

@app.route("/dashboard")
@login_required
def dashboard():
    """Shows aggregated loan statistics as cards."""
    stats = db.get_dashboard_stats()
    return render_template("dashboard.html", stats=stats)


# ==================================================================
# LOAN APPLICATION (public-facing form)
# ==================================================================

@app.route("/apply", methods=["GET", "POST"])
def apply_loan():
    """
    Public loan application form.
    On POST: validates input, runs the eligibility engine, saves the
    record, then renders the result back on the same page.
    """
    result = None
    form_data = {}

    if request.method == "POST":
        errors, cleaned = validate_loan_form(request.form)
        form_data = cleaned

        if errors:
            for error in errors:
                flash(error, "danger")
        else:
            decision = evaluate_loan_eligibility(
                cleaned["credit_score"], cleaned["monthly_income"]
            )

            record = {**cleaned, **decision}
            new_id = db.create_loan_application(record)

            result = {
                "id": new_id,
                "status": decision["status"],
                "risk_level": decision["risk_level"],
                "eligible_amount": decision["eligible_amount"],
                "full_name": cleaned["full_name"],
                "loan_amount": cleaned["loan_amount"],
            }
            flash("Loan application submitted successfully!", "success")
            form_data = {}  # reset form after a successful submission

    return render_template("apply_loan.html", result=result, form_data=form_data)


# ==================================================================
# ADMIN PANEL - MANAGE APPLICATIONS
# ==================================================================

@app.route("/applications")
@login_required
def applications():
    """
    Lists all loan applications for the admin, with optional
    search-by-name and filter-by-status query parameters.
    """
    search = request.args.get("search", "").strip()
    status = request.args.get("status", "All").strip()

    records = db.get_all_loan_applications(search=search or None, status=status)

    return render_template(
        "applications.html",
        applications=records,
        search=search,
        status=status,
    )


@app.route("/applications/<int:application_id>/approve", methods=["POST"])
@login_required
def approve_application(application_id):
    """Admin action: approve a pending loan application."""
    if db.update_loan_status(application_id, "Approved"):
        flash(f"Application #{application_id} approved.", "success")
    else:
        flash("Could not find that application.", "danger")
    return redirect(url_for("applications"))


@app.route("/applications/<int:application_id>/reject", methods=["POST"])
@login_required
def reject_application(application_id):
    """Admin action: reject a pending loan application."""
    if db.update_loan_status(application_id, "Rejected"):
        flash(f"Application #{application_id} rejected.", "info")
    else:
        flash("Could not find that application.", "danger")
    return redirect(url_for("applications"))


@app.route("/applications/<int:application_id>/delete", methods=["POST"])
@login_required
def delete_application(application_id):
    """Admin action: permanently delete a loan application."""
    if db.delete_loan_application(application_id):
        flash(f"Application #{application_id} deleted.", "info")
    else:
        flash("Could not find that application.", "danger")
    return redirect(url_for("applications"))


# ==================================================================
# ERROR HANDLERS
# ==================================================================

@app.errorhandler(404)
def not_found(e):
    return render_template("login.html"), 404


@app.errorhandler(500)
def server_error(e):
    flash("Something went wrong on our end. Please try again.", "danger")
    return redirect(url_for("login"))


# ==================================================================
# APPLICATION ENTRY POINT
# ==================================================================

if __name__ == "__main__":
    # Seed a default admin (admin / admin123) on first run.
    try:
        db.seed_default_admin()
    except Exception as e:
        print(f"[WARNING] Could not seed default admin. Is MySQL running "
              f"and schema.sql imported? Error: {e}")

    app.run(debug=True, host="0.0.0.0", port=5000)
