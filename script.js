
document.addEventListener("DOMContentLoaded", function () {

  // ---------- 1. Loan application form validation ----------
  const loanForm = document.getElementById("loanForm");

  if (loanForm) {
    loanForm.addEventListener("submit", function (event) {
      let isValid = true;
      const errorMessages = [];

      const creditScore = parseInt(loanForm.credit_score.value, 10);
      if (isNaN(creditScore) || creditScore < 300 || creditScore > 900) {
        isValid = false;
        errorMessages.push("Credit score must be between 300 and 900.");
      }

      const mobile = loanForm.mobile_number.value.trim();
      const mobilePattern = /^[6-9]\d{9}$/;
      if (!mobilePattern.test(mobile)) {
        isValid = false;
        errorMessages.push("Enter a valid 10-digit mobile number.");
      }

      const age = parseInt(loanForm.age.value, 10);
      if (isNaN(age) || age < 21 || age > 65) {
        isValid = false;
        errorMessages.push("Age must be between 21 and 65.");
      }

      const monthlyIncome = parseFloat(loanForm.monthly_income.value);
      if (isNaN(monthlyIncome) || monthlyIncome <= 0) {
        isValid = false;
        errorMessages.push("Monthly income must be greater than zero.");
      }

      const loanAmount = parseFloat(loanForm.loan_amount.value);
      if (isNaN(loanAmount) || loanAmount <= 0) {
        isValid = false;
        errorMessages.push("Loan amount must be greater than zero.");
      }

      if (!isValid) {
        event.preventDefault();
        alert("Please fix the following before submitting:\n\n- " + errorMessages.join("\n- "));
      }
    });
  }

  // ---------- 2. Confirm before deleting an application ----------
  document.querySelectorAll(".js-confirm-delete").forEach(function (form) {
    form.addEventListener("submit", function (event) {
      const confirmed = confirm("Are you sure you want to permanently delete this application?");
      if (!confirmed) {
        event.preventDefault();
      }
    });
  });

  // ---------- 3. Auto-dismiss flash messages after 5 seconds ----------
  document.querySelectorAll(".alert").forEach(function (alertEl) {
    setTimeout(function () {
      alertEl.classList.remove("show");
      alertEl.classList.add("fade");
      setTimeout(function () {
        alertEl.remove();
      }, 300);
    }, 5000);
  });

});
