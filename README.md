# 💰 Digital Loan Management System

A full-stack **Digital Loan Management System** built with **Python, Flask, MySQL, Bootstrap 5, and JavaScript**.

This application allows customers to submit loan applications and provides an admin dashboard for reviewing, searching, filtering, approving, rejecting, and deleting applications.

> 🎯 A portfolio project demonstrating backend development, database management, CRUD operations, authentication, validation, and business-rule logic.

---

## 🚀 Features

### 👤 Customer

- 📝 Submit loan applications
- 📋 Enter personal, income, employment, and credit details
- ⚡ Instant eligibility evaluation
- ✅ Approved / Pending / Rejected result
- ⚠️ Risk-level calculation
- 💰 Eligible loan amount calculation

### 🔐 Admin

- Secure admin login
- 📊 Dashboard statistics
- 🔎 Search applications by customer name
- 🏷️ Filter applications by status
- ✅ Approve applications
- ❌ Reject applications
- 🗑️ Delete applications
- 💰 View total requested loan amount

---

## ⚖️ Loan Eligibility Logic

| Credit Score | Monthly Income | Decision |
|---|---:|---|
| ≥ 750 | ≥ ₹40,000 | ✅ Approved |
| 650–749 | ≥ ₹25,000 | 🟠 Pending Review |
| Other cases | — | ❌ Rejected |

The system also calculates:

- **Risk Level:** Low / Medium / High
- **Eligible Loan Amount:** Monthly Income × 10

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Backend | Python, Flask |
| Database | MySQL |
| Database Driver | mysql-connector-python |
| Frontend | HTML5, CSS3 |
| UI Framework | Bootstrap 5 |
| Scripting | JavaScript |
| Security | Werkzeug Password Hashing |
| Tools | Git, GitHub, VS Code |

---

## 📂 Project Structure

```text
Loan_Mangement_System/
│
├── app.py
├── database.py
├── requirements.txt
├── schema.sql
│
├── static/
│   ├── style.css
│   ├── dashboard.css
│   └── script.js
│
├── templates/
│   ├── navbar.html
│   ├── login.html
│   ├── dashboard.html
│   ├── apply_loan.html
│   └── applications.html
│
└── README.md
