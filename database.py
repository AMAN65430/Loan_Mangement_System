"""
database.py
------------
Handles the MySQL connection and all CRUD (Create, Read, Update,
Delete) database operations for the Digital Loan Management System.

All queries use parameterized statements (%s placeholders) to
prevent SQL injection.
"""

import os
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash


# ----------------------------------------------------------------
# Database configuration
# Reads from environment variables when available, otherwise falls
# back to sensible local-development defaults.
# ----------------------------------------------------------------
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", "Miet@123"),
    "database": os.environ.get("DB_NAME", "loan_management_system"),
}


def get_db_connection():
    """
    Opens and returns a new MySQL connection using the settings in
    DB_CONFIG. Raises an Error if the connection cannot be made.
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"[DB ERROR] Could not connect to MySQL: {e}")
        raise


# ==================================================================
# ADMIN OPERATIONS
# ==================================================================

def seed_default_admin():
    """
    Creates a default admin account (admin / admin123) the first
    time the application runs, if the admins table is empty.
    This guarantees there is always a way to log in on a fresh
    database without ever storing a plain-text password.
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM admins")
        count = cursor.fetchone()[0]
        if count == 0:
            default_hash = generate_password_hash("admin123")
            cursor.execute(
                "INSERT INTO admins (username, password_hash) VALUES (%s, %s)",
                ("admin", default_hash),
            )
            connection.commit()
            print("[INFO] Default admin created -> username: admin | password: admin123")
    finally:
        cursor.close()
        connection.close()


def get_admin_by_username(username):
    """Fetches a single admin row by username. Returns a dict or None."""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM admins WHERE username = %s", (username,))
        return cursor.fetchone()
    finally:
        cursor.close()
        connection.close()


# ==================================================================
# LOAN APPLICATION OPERATIONS (CRUD)
# ==================================================================

def create_loan_application(data):
    """
    Inserts a new loan application record.
    `data` is a dict containing all the required fields, already
    validated and with the eligibility decision computed.
    Returns the newly inserted row's id.
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = """
            INSERT INTO loan_applications
            (full_name, email, mobile_number, age, monthly_income,
             employment_type, loan_amount, loan_purpose, credit_score,
             eligible_amount, risk_level, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data["full_name"],
            data["email"],
            data["mobile_number"],
            data["age"],
            data["monthly_income"],
            data["employment_type"],
            data["loan_amount"],
            data["loan_purpose"],
            data["credit_score"],
            data["eligible_amount"],
            data["risk_level"],
            data["status"],
        )
        cursor.execute(query, values)
        connection.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        connection.close()


def get_all_loan_applications(search=None, status=None):
    """
    Reads loan applications from the database.
    Optionally filters by customer name (partial match) and/or
    exact status. Results are ordered by newest first.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT * FROM loan_applications WHERE 1=1"
        params = []

        if search:
            query += " AND full_name LIKE %s"
            params.append(f"%{search}%")

        if status and status != "All":
            query += " AND status = %s"
            params.append(status)

        query += " ORDER BY created_at DESC"
        cursor.execute(query, tuple(params))
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def get_loan_application_by_id(application_id):
    """Fetches a single loan application by its primary key."""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM loan_applications WHERE id = %s", (application_id,)
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        connection.close()


def update_loan_status(application_id, new_status):
    """
    Updates the status of a loan application (Approved / Rejected).
    Used by the admin panel to act on pending applications.
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "UPDATE loan_applications SET status = %s WHERE id = %s",
            (new_status, application_id),
        )
        connection.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()
        connection.close()


def delete_loan_application(application_id):
    """Deletes a loan application permanently."""
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "DELETE FROM loan_applications WHERE id = %s", (application_id,)
        )
        connection.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()
        connection.close()


def get_dashboard_stats():
    """
    Aggregates the key numbers shown on the dashboard:
    total applications, approved/rejected/pending counts, and the
    total loan amount requested across all applications.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        stats = {}

        cursor.execute("SELECT COUNT(*) AS total FROM loan_applications")
        stats["total_applications"] = cursor.fetchone()["total"]

        cursor.execute(
            "SELECT COUNT(*) AS c FROM loan_applications WHERE status = 'Approved'"
        )
        stats["approved"] = cursor.fetchone()["c"]

        cursor.execute(
            "SELECT COUNT(*) AS c FROM loan_applications WHERE status = 'Rejected'"
        )
        stats["rejected"] = cursor.fetchone()["c"]

        cursor.execute(
            "SELECT COUNT(*) AS c FROM loan_applications WHERE status = 'Pending'"
        )
        stats["pending"] = cursor.fetchone()["c"]

        cursor.execute(
            "SELECT COALESCE(SUM(loan_amount), 0) AS total_amount FROM loan_applications"
        )
        stats["total_amount"] = float(cursor.fetchone()["total_amount"])

        return stats
    finally:
        cursor.close()
        connection.close()
