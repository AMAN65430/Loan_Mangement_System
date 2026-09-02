# Digital Loan Management System

A complete fintech-style **Digital Loan Management System** built with Flask, MySQL, Bootstrap 5, and vanilla JavaScript — inspired by digital lending platforms like Credeau. Customers can apply for loans through a public application form, and an admin can log in to a dashboard to review, approve, reject, search, filter, and delete applications.

Built as a portfolio / interview project for an **SDE R1 (Fresher) role**, demonstrating full-stack CRUD, business-rule logic, authentication, and clean UI design.

---

## Overview

The system has two user-facing surfaces:

1. **Customer-facing loan application form** (`/apply`) — no login required. A customer fills in personal, income, and credit details. The backend instantly evaluates eligibility using a rules-based engine and shows the decision.
2. **Admin panel** (`/login`, `/dashboard`, `/applications`) — a secured area where a bank admin can view statistics, search/filter applications, and approve, reject, or delete them.

---

## Features

- 🔐 **Secure admin login** with hashed passwords (Werkzeug `generate_password_hash` / `check_password_hash`) and session-based auth.
- 📊 **Dashboard** with live stat cards: total applications, approved, rejected, pending, and total loan amount requested.
- 📝 **Loan application form** with full server-side validation (name, email, mobile, age, income, employment type, loan amount, purpose, credit score).
- ⚖️ **Loan eligibility engine**:
  - Credit Score ≥ 750 **and** Income ≥ ₹40,000 → **Approved**
  - Credit Score 650–749 **and** Income ≥ ₹25,000 → **Pending Review**
  - Otherwise → **Rejected**
  - Also computes **Risk Level** (Low / Medium / High) and **Eligible Loan Amount** (Monthly Income × 10).
- 🗂️ **Admin panel**: search by customer name, filter by status, approve/reject pending applications, delete applications.
- 🎨 **Modern fintech UI**: blue gradient navbar, white cards, responsive Bootstrap 5 grid, hover-effect tables, color-coded status badges (green/red/orange).
- 🛡️ **Security**: parameterized SQL queries (SQL-injection safe), password hashing, server-side + client-side input validation, flash messages for feedback.
- 🧱 **Full CRUD**: Create loan applications, Read/list with search & filter, Update status, Delete records.

---

## Technologies Used

| Layer       | Technology                          |
|-------------|--------------------------------------|
| Backend     | Python 3, Flask                      |
| Database    | MySQL (via `mysql-connector-python`) |
| Frontend    | HTML5, CSS3, Bootstrap 5             |
| Scripting   | Vanilla JavaScript                   |
| Security    | Werkzeug password hashing            |

No React, Django, Node.js, or paid services are used.

---

## Project Structure

```
loan_management_system/
│
├── app.py                # Flask app: routes, auth, validation, eligibility logic
├── database.py            # MySQL connection + all CRUD functions
├── requirements.txt        # Python dependencies
├── schema.sql              # Database schema (run this first)
├── static/
│   ├── style.css           # Global fintech theme (login, forms, badges)
│   ├── dashboard.css        # Dashboard stat-card styles
│   └── script.js            # Client-side validation & UX
├── templates/
│   ├── navbar.html          # Shared admin navbar (included in dashboard/applications)
│   ├── login.html           # Admin login page
│   ├── dashboard.html        # Dashboard with stat cards
│   ├── apply_loan.html       # Public loan application form + result card
│   └── applications.html     # Admin panel: table, search, filter, actions
└── README.md
```

---

## Installation & Setup

### 1. Prerequisites
- Python 3.9+
- MySQL Server 8.x (running locally or remotely)
- pip

### 2. Clone / extract the project
```bash
cd loan_management_system
```

### 3. Create a virtual environment (recommended)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Set up the MySQL database
Open a MySQL client (e.g. MySQL Workbench, `mysql` CLI) and run:
```bash
mysql -u root -p < schema.sql
```
This creates the `loan_management_system` database along with the `admins` and `loan_applications` tables.

### 6. Configure database credentials
By default, `database.py` connects with:
```
host=localhost, user=root, password="", database=loan_management_system
```
If your MySQL setup is different, set environment variables before running the app:

```bash
# macOS / Linux
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=your_mysql_password
export DB_NAME=loan_management_system

# Windows (PowerShell)
$env:DB_HOST="localhost"
$env:DB_USER="root"
$env:DB_PASSWORD="your_mysql_password"
$env:DB_NAME="loan_management_system"
```

### 7. Run the application
```bash
python app.py
```
The app seeds a **default admin account** on first run:
- **Username:** `admin`
- **Password:** `admin123`

Visit **http://localhost:5000** in your browser.

- Customers: go to `http://localhost:5000/apply`
- Admin: go to `http://localhost:5000/login`

---

## Usage Walkthrough

1. A customer visits `/apply`, fills the loan form, and submits it.
2. The eligibility engine instantly evaluates the application and displays an **Approved / Pending / Rejected** result card with the risk level and eligible amount.
3. The admin logs in at `/login` using the default (or created) credentials.
4. The **Dashboard** shows live counts and total requested amount.
5. The admin opens **Applications**, searches by name or filters by status, and approves/rejects pending applications or deletes any record.

---

## Screenshots

> Add your own screenshots here after running the project locally.

- `screenshots/login.png` — Admin login page
- `screenshots/dashboard.png` — Dashboard with stat cards
- `screenshots/apply_loan.png` — Loan application form + result card
- `screenshots/applications.png` — Admin panel with search/filter and badges

---

## Security Notes

- Passwords are never stored in plain text — only Werkzeug password hashes.
- All SQL queries use parameterized placeholders (`%s`) via `mysql-connector-python`, preventing SQL injection.
- All routes that modify data (approve/reject/delete) require an active admin session (`@login_required`).
- Server-side validation is authoritative; JavaScript validation is a UX convenience layer only.

---

## Possible Future Enhancements

- Multi-admin roles (super admin vs. reviewer)
- Email/SMS notifications on status change
- Document upload (ID proof, income proof) with file storage
- Pagination for large application lists
- REST API endpoints for mobile integration
